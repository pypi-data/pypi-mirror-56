from pvHelpers.crypto.utils import CryptoException
from pvHelpers.logger import g_log
from pvHelpers.mail.email import EmailException, PROTOCOL_VERSION
from pvHelpers.utils import b64dec, EncodingException


ACCEPTED_PROTOCOL_VERSIONS = [PROTOCOL_VERSION.V4, PROTOCOL_VERSION.V5, PROTOCOL_VERSION.V6]


def reconstruct_content_blocks(block_ids, blocks, symm_key):
    part = ''
    for block_id in block_ids:
        encrypted_block = blocks.get(block_id)
        if encrypted_block is None:
            return None, KeyError('missing block with block_id {}'.format(block_id))

        encrypted_block = encrypted_block.get('data')
        if encrypted_block is None:
            return None, KeyError('data missing')

        try:
            p = symm_key.decrypt(b64dec(encrypted_block))
        except (CryptoException, EncodingException) as e:
            return None, e
        part += p

    return part, None


def load_content(email, blocks, decrypt_key):
    content_ref_ids = [
        email.body.reference_id] + map(lambda att: att.content.reference_id, email.attachments)

    contents = {}
    for reference_id in content_ref_ids:
        raw_content, err = reconstruct_content_blocks(reference_id.split(','), blocks, decrypt_key)
        if err is not None:
            g_log.exception(err)
            continue
        contents[reference_id] = raw_content

    if not all(map(lambda ref_id: ref_id in contents, content_ref_ids)):
        raise EmailException('Failed to reconstuct email contents, missing blocks')

    body_content = contents[email.body.reference_id]
    email.load_body(body_content)
    for att in email.attachments:
        if att.content.reference_id in contents:
            att.load_content(contents[att.content.reference_id])

    return email


def wrap_for_export(mime):
    # add header
    return mime
