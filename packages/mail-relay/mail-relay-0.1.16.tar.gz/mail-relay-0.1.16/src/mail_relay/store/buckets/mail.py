from mail_relay.mail.mail_state import MailState
from pvHelpers.utils import jdumps, jloads


class MailStateBucket:
    NAME = u'mail_state'
    CURRENT_VERSION = 0

    @staticmethod
    def key(user_id, account_version):
        return '{};{}'.format(account_version, user_id.lower())

    @staticmethod
    def serialize(mail_state, bucket_version):
        if bucket_version == 0:
            return MailStateBucket._serialize_v0(mail_state)
        else:
            raise ValueError(u'unsupported bucket bucket_version {}'.format(bucket_version))

    @staticmethod
    def deserialize(blob, bucket_version):
        if bucket_version == 0:
            return MailStateBucket._deserialize_v0(blob)
        else:
            raise ValueError(u'unsupported bucket bucket_version {}'.format(bucket_version))

    @staticmethod
    def _serialize_v0(mail_state):
        return jdumps(mail_state.rev_id)

    @staticmethod
    def _deserialize_v0(blob):
        j = jloads(blob)
        return MailState(j)
