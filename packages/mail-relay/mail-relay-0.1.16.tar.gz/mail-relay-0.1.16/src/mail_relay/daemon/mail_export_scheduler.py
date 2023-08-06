from mail_relay.mail.helpers import ACCEPTED_PROTOCOL_VERSIONS, load_content, wrap_for_export
from pvHelpers.crypto import CryptoException, PVKeyFactory
from pvHelpers.logger import g_log
from pvHelpers.mail import EmailFactory
from pvHelpers.mail.email.helpers import EmailException
from pvHelpers.mail.helpers import decrypt_server_message, get_sender, get_wrapped_key
from pvHelpers.utils import b64dec, CaseInsensitiveDict


class MailExportScheduler():
    def __init__(self, ctx):
        self.ctx = ctx

    def run(self):
        export_state, err = self.ctx.get_set_export_state()
        if err is not None:
            return err

        for member_id in export_state.members:
            member = self.ctx.get_member(member_id, -1)
            err = self.export_user_mails(member, export_state)
            if err is not None:
                g_log.error(err)

    def download_blocks(self, collection_id, block_ids):
        downloaded_server_blocks = CaseInsensitiveDict()
        chunk_size = 50
        for i in range(0, len(block_ids), chunk_size):
            downloaded_server_blocks.update(
                self.ctx.cs_client.get_blocks(self.ctx.exporter, block_ids[i:i+chunk_size], collection_id))

        return downloaded_server_blocks

    def export_user_mails(self, member, export_state):  # noqa: C901
        has_more = True

        while has_more:
            email_updates = self.ctx.cs_client.get_mail_history_for_export(
                self.ctx.exporter, self.ctx.get_members_last_rev_id(member.user_id, member.account_version),
                member.user_id, member.mail_cid, export_state.request.request_id)
            has_more = email_updates['has_more']
            if len(email_updates['messages']) == 0:
                continue

            for m in email_updates['messages']:
                if m['protocol_version'] not in ACCEPTED_PROTOCOL_VERSIONS:
                    g_log.info('unsupported protocol version {} for {} for user ({}, {})'.format(
                        m['protocol_version'], m['id'], member.user_id, member.account_version))
                    continue
                key_version, wrapped_key = get_wrapped_key(m)
                member_encryption_key = self.ctx.get_set_member_encryption_key(
                    member.user_id, key_version)
                if not member_encryption_key:
                    g_log.error(
                        'Decryption key for ({}, {}) not found in'
                        'export req {}.'.format(member.user_id, key_version, export_state.request.request_id))
                    continue

                try:
                    wrapped_raw_key = b64dec(wrapped_key)
                    raw_key = member_encryption_key.unseal(wrapped_raw_key)
                    decrypt_key = PVKeyFactory.deserializeSymmKey(raw_key)

                    decrypted_message = decrypt_server_message(m, member_encryption_key, decrypt_key)

                    if decrypted_message['protocol_version'] <= 4:
                        decrypted_message['collection_id'] = member.mail_cid
                    else:
                        sender_id, key_version = get_sender(decrypted_message)
                        decrypted_message['collection_id'] = self.ctx.cs_client.fetch_users(
                            self.ctx.exporter, [(sender_id, -1)])[sender_id].mail_cid

                    email = EmailFactory.from_server_message(
                        member.user_id, decrypted_message, wrapped_key, key_version, None)

                    blocks = self.download_blocks(
                        decrypted_message['collection_id'],
                        reduce(lambda acc, att: acc + att.content.block_ids, email.attachments, email.body.block_ids))

                    email = load_content(email, blocks, decrypt_key)
                    mime_string = email.to_mime().to_string()
                except CryptoException as e:
                    g_log.error(
                        'error decryption email {} for user ({}, {})'.format(
                            m['id'], member.user_id, member.account_version))

                    g_log.exception(e)
                    continue
                except EmailException as e:
                    g_log.error('error reconstructing email {}'.format(m['id']))
                    g_log.exception(e)
                    continue

                # catch wrapping errors ?
                export_mime = wrap_for_export(mime_string)
                err = self.ctx.relay_mime(
                    member.user_id, member.account_version, m['id'], m['rev_id'], export_mime)
                if err is not None:
                    return 'failed to relay message {} for user ({}, {}): {}'.format(
                        m['id'], member.user_id, member.account_version, err)
