import os

import gevent
import pvHelpers.approval_group.export_shard as ExportShard
from pvHelpers.crypto import PVKeyFactory
from pvHelpers.cs_client.utils import ExpiredDeviceKey
from pvHelpers.logger import g_log
from pvHelpers.request import UserRequest
from pvHelpers.user import OrganizationInfo, User
from pvHelpers.utils import CaseInsensitiveDict, CaseInsensitiveSet, quiet_mkdir
import requests


def deserialize_user(u):
    organiztion_info = OrganizationInfo(
        u['entity_id'], u'', u['entity_metadata']['department'],
        u['entity_metadata']['role']) if u['entity_id'] else None

    public_user_keys = []
    if u['public_key']:
        public_user_keys = [
            PVKeyFactory.deserializePublicUserKey(u['public_key'])]

    user = User(
        u['user_id'], u['account_version'], u['display_name'],
        u['mail_collection_id'], public_user_keys, organiztion_info)

    return user


def gthread_value(g):
    if g.successful():
        return g.value, None
    else:
        return None, g.exception


def export_groups_equal(e1, e2):
    e1_set = CaseInsensitiveSet([(a['account_version'], a['user_id']) for a in e1['approvers']])
    e2_set = CaseInsensitiveSet([(a['account_version'], a['user_id']) for a in e1['approvers']])
    return e1['optionals_required'] == e2['optionals_required'] and e1_set == e2_set


# TODO: check if export requests has all the required members in its payload
def export_has_all_members_keys(export_request, members):
    return False


def write_mime_to_disk(path, member_id, server_id, mime):
    try:
        member_dir = os.path.join(path, member_id.lower())
        quiet_mkdir(member_dir)

        filename = os.path.join(member_dir, server_id.lower()) + '.eml'

        if os.environ.get('MODE', '').startswith('test'):  # assert for duplicates in tests
            assert not os.path.isfile(filename)

        with open(filename, 'w') as f:
            f.write(mime)
    except Exception as e:
        return e


def fetch_approvers_export_shards(approvers, request_id, cs_client):
    threads = []
    for a in approvers:
        threads.append(
            gevent.spawn(cs_client.get_export_shards, a, a.org_info.org_id, request_id))

    gevent.joinall(threads)

    approver_shards = []
    for (approver, (shards, err)) in zip(approvers, map(lambda t: gthread_value(t), threads)):
        if err is not None:
            if isinstance(err, ExpiredDeviceKey):
                raise err
            g_log.exception(err)

            continue

        approver_shards.append((approver, shards))

    return approver_shards


def decrypt_export_shards(export_shards, members):
    decrypted_shards = CaseInsensitiveDict()  # (key_version, member_id) => [shard*]
    for approver, approver_shards in export_shards:
        for member_id, member_key_shards in approver_shards.iteritems():
            if len(member_key_shards) > 0:
                for key_shard in member_key_shards:
                    # NOTE: these fields are missing in collection server's response
                    key_shard['user_id'] = approver.user_id
                    key_shard['required'] = False
                    # collection server just renames `secret` field to `shard`!
                    key_shard['secret'] = key_shard['shard']
                    key_version = key_shard['wrapped_key_version']

                    encrypted_shard = ExportShard.from_dict(key_shard)
                    decrypted_shard = encrypted_shard.decrypt_shard(
                        approver.get_key_with_version(encrypted_shard.sharee_key_version),
                        members[member_id].get_public_user_key_with_version(encrypted_shard.sharer_key_version)
                    )

                    decrypted_shards[(key_version, member_id)] = \
                        decrypted_shards.get((key_version, member_id), []) + [decrypted_shard]

    return decrypted_shards


def get_required_pks_for_decryption(export_shards):
    members_required_pks = []
    for (_, approver_shards) in export_shards:
        members_required_pks += reduce(
            lambda acc, (member_id, key_shards):
                acc + map(lambda x: (member_id.lower(), x['sharder_key_version']), key_shards),
            approver_shards.iteritems(), []
        )

    return members_required_pks


def approve_and_sign_request(approvers, request_id, cs_client):
    def _approve(approver):
        requests = cs_client.get_user_approvals(approver, u'pending', u'pending', True, 0, 10)
        for r in requests['approvals']:
            if r['request_id'] == request_id:
                cs_client.respond_to_org_approval(
                    approver, approver.org_info.org_id,
                    UserRequest(r['payload'], r['signature'], request_id), True, {})

    threads = []
    for a in approvers:
        threads.append(gevent.spawn(_approve, a))

    gevent.joinall(threads)

    for (approver, (res, err)) in zip(approvers, map(lambda t: gthread_value(t), threads)):
        if err is not None:
            if isinstance(err, ExpiredDeviceKey):
                raise err
            # accept re-approval failures
            if isinstance(err, requests.exceptions.HTTPError) and err.response.status_code == 409:
                continue
            g_log.exception(err)


def validate_approvers(approvers, cs_client):
    threads = []
    for a in approvers:
        threads.append(
            gevent.spawn(cs_client.get_user_devices, a))

    gevent.joinall(threads)

    valid_approvers = []
    for (approver, (res, err)) in zip(approvers, map(lambda t: gthread_value(t), threads)):
        if err is not None:
            if isinstance(err, ExpiredDeviceKey):
                raise err
            g_log.exception(err)
            continue

        valid_approvers.append(approver)

    return valid_approvers


def get_check_valid_approvers(users, export_group, cs_client):
    required_approvers = export_group['optionals_required']
    approvers = [(a['account_version'], a['user_id']) for a in export_group['approvers']]
    existing_approvers = [a for a in [users.get((av, i)) for (av, i) in approvers] if a is not None]
    valid_approvers = validate_approvers(existing_approvers, cs_client)
    if len(valid_approvers) < required_approvers:
        return None, 'missing required approvers'

    return valid_approvers, None
