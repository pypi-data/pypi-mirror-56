import datetime
import time

from mail_relay.mail.mail_state import MailState
from mail_relay.mail.smtp import send_mail
from mail_relay.store.handlers import (add_or_update_export_state, read_config,
                                       read_export_state, read_exporter, read_user_mail_state,
                                       read_users, remove_records, update_user_info,
                                       update_user_mail_state, write_temp_device_key)
from pvHelpers.approval_group import ApprovalGroup
from pvHelpers.crypto import CryptoException, PVKeyFactory
from pvHelpers.crypto.asymm_key import AsymmKeyBase
from pvHelpers.cs_client import BackendClient
from pvHelpers.logger import g_log
from pvHelpers.request import ExportRequest
from pvHelpers.utils import b64enc, CaseInsensitiveDict, utf8Encode

from .export_state import ExportState
from .helpers import (approve_and_sign_request, decrypt_export_shards, deserialize_user,
                      export_groups_equal, export_has_all_members_keys,
                      fetch_approvers_export_shards, get_check_valid_approvers,
                      get_required_pks_for_decryption, write_mime_to_disk)


ATTEMPT_RECONSTRUCTION_DELAY = 30


# handles in applications state, caching
class State(object):
    def __init__(self, store_path):
        self.store_path = store_path

        self.config = read_config(store_path)

        exporter_a_v, exporrer_id = read_exporter(store_path)
        self.exporter = self.local_users[(exporter_a_v, exporrer_id)]

        self.cs_client = BackendClient()
        self.cs_client.init(self.config.cs.http)

        self.members = CaseInsensitiveDict()
        self.export_group = None

        # (key_version, member_id) => EncryptionKey/last-check-time
        # last time check to avoid reconstruction sooner than ATTEMPT_RECONSTRUCTION_DELAY
        self._members_keys = CaseInsensitiveDict()

    @property
    def local_users(self):
        return read_users(self.store_path)

    def rotate_device_key(self, user_id, account_version):
        user = self.local_users[(account_version, user_id)]
        new_device_key = PVKeyFactory.newUserKey(user.device.key.key_version + 1)
        record_id = write_temp_device_key(
            user.user_id, user.account_version, new_device_key, self.store_path)

        self.cs_client.rotate_device_key(user, new_device_key)
        user.device.key = new_device_key
        update_user_info(user, self.store_path)
        remove_records([record_id], self.store_path)

    def relay_mime(self, user_id, account_version, server_id, rev_id, mime):
        if self.get_members_last_rev_id(user_id, account_version) >= rev_id:
            return ValueError(
                '{} less that users `last_rev_id` for ({}, {}).'.format(rev_id, user_id, account_version))

        err = None
        if self.config.volume:
            err = write_mime_to_disk(self.config.volume.path, user_id, server_id, mime)
        elif self.config.smtp:
            err = send_mail(self.config.smtp, mime)
        else:
            return ValueError('Unknown relaying configuration')

        if err is None:
            update_user_mail_state(user_id, account_version, MailState(rev_id), self.store_path)

        return err

    def get_member(self, member_id, account_version):
        # NOTE: Unfortunately backend keeps track of export requests by key_version
        member_versions = [m for (a_v, id_), m in self.members.iteritems() if member_id.lower() == id_.lower()]
        assert len(member_versions) == 1
        return member_versions[0]

    def get_members_last_rev_id(self, user_id, account_version):
        mail_state = read_user_mail_state(user_id, account_version, self.store_path)
        return 0 if mail_state is None else mail_state.rev_id

    def get_set_member_encryption_key(self, user_id, key_version):
        k_t = self._members_keys.get((key_version, user_id))

        if k_t is None or (not isinstance(k_t, AsymmKeyBase) and (time.time() - k_t > ATTEMPT_RECONSTRUCTION_DELAY)):
            # re-fetch shards and update newly uploaded keys
            self.fetch_shards_and_update_keys()

        k_t = self._members_keys.get((key_version, user_id))
        if not isinstance(k_t, AsymmKeyBase):
            self._members_keys[(key_version, user_id)] = time.time()
            return None

        return k_t

    def get_set_export_state(self):
        (export_group, members), err = self.get_set_org_current_export_info()
        if err is not None:
            return None, err

        export_state = read_export_state(self.store_path)

        # create new export request
        if export_state is None or any([
            not export_groups_equal(export_state.group_info, export_group),
            not export_has_all_members_keys(export_state.request, members),
            export_state.valid_for < 60 * 60
        ]):
            expiry = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            export_req = self.cs_client.create_user_request(
                self.exporter, ExportRequest.new(self.exporter, {
                    'until': unicode(expiry.isoformat()),
                    'include_emails': True,
                    'include_files': False,
                    'users': map(
                        lambda u: {'user_id': u.user_id, 'key_version': u.public_user_key.key_version},
                        [m for m in members if m.is_claimed()]
                    ),
                    'from': None
                }))['request']

            export_state = ExportState(
                ExportRequest(export_req['payload'], export_req['signature'], export_req['request_id']),
                export_group, {})

            add_or_update_export_state(export_state, self.store_path)

        # set approver info if enough approvers available
        if len(export_state.approver_signatures) < export_group['optionals_required']:
            valid_approvers, err = get_check_valid_approvers(self.local_users, export_group, self.cs_client)
            if err is not None:
                return None, err

            approve_and_sign_request(valid_approvers, export_state.request.request_id, self.cs_client)

            approvers_info = CaseInsensitiveDict()
            for approver in valid_approvers:
                approvers_info[approver.user_id] = {
                    'approver_shards': {},
                    'approver_signature': b64enc(
                        approver.user_key.signing_key.sign(utf8Encode(export_state.request.signature)))
                }
            export_state = ExportState(export_state.request, export_group, approvers_info)

        return export_state, None

    def get_set_org_current_export_info(self):
        org_info = self.cs_client.get_org_info(
            self.exporter, self.exporter.org_info.org_id)

        if org_info['roled_approval_groups'].get('export_approval_group') is None:
            return (None, None), 'export group not configured'

        group_id = org_info['roled_approval_groups']['export_approval_group']['group_id']
        version = org_info['roled_approval_groups']['export_approval_group']['version']
        export_group = self.cs_client.get_org_apg_info(
            self.exporter, self.exporter.org_info.org_id, group_id, version)

        members = [deserialize_user(u) for u in org_info['users']]
        self.members = CaseInsensitiveDict({(m.account_version, m.user_id): m for m in members})
        self.export_group = export_group
        return (export_group, members), None

    def fetch_shards_and_update_keys(self):
        export_state, err = self.get_set_export_state()
        if err is not None:
            raise RuntimeError(err)

        approvers = [(a['account_version'], a['user_id']) for a in self.export_group['approvers']]
        existing_approvers = [a for a in [self.local_users.get((av, i)) for (av, i) in approvers] if a is not None]

        export_shards = fetch_approvers_export_shards(
            existing_approvers, export_state.request.request_id, self.cs_client)
        members_required_pks = get_required_pks_for_decryption(export_shards)

        # TODO: check existing and only fetch missing keys, then update `ctx.members`
        members = self.cs_client.fetch_users(self.exporter, list(set(members_required_pks)))

        decrypted_shards = decrypt_export_shards(export_shards, members)

        # reconstruct and update state
        for (kv, member_id), available_shards in decrypted_shards.iteritems():
            curr_key = self._members_keys.get((kv, member_id))
            if curr_key is None or curr_key:
                if len(available_shards) < self.export_group['optionals_required']:
                    g_log.error('Not enough shards to reconstructing key: ({}, {})'.format(member_id, kv))
                    continue

                ag = ApprovalGroup.new(
                    member_id, [],
                    [{'user_id': u['user_id'], 'display_name': u'dummy'} for u in self.export_group['approvers']],
                    self.export_group['optionals_required'])

                try:
                    user_key = PVKeyFactory.deserializeUserKey(ag.reconstruct_secret([], available_shards))
                    # this is bad user input
                    assert kv == user_key.key_version
                    self._members_keys[(kv, member_id)] = user_key.encryption_key
                except CryptoException as e:
                    g_log.error('Error reconstructing key: ({}, {})'.format(member_id, kv))
                    g_log.exception(e)
                    continue

            # TODO: check for possible bad shards or unmatching key_version , server against wrapped
