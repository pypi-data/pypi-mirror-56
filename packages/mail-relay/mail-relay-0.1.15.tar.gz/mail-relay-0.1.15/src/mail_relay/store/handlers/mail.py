from mail_relay.store.buckets import MailStateBucket
from pvHelpers.store import GetDBSession


def read_user_mail_state(user_id, account_version, store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key = :key
            ''', {
                'bucket': MailStateBucket.NAME,
                'key': MailStateBucket.key(user_id, account_version)
            }
        )
        r = result.fetchone()

    if r is not None:
        (_, blob, b_v) = r
        return MailStateBucket.deserialize(blob, b_v)

    return None


def update_user_mail_state(user_id, account_version, state, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT OR REPLACE INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': MailStateBucket.NAME,
                    'version': MailStateBucket.CURRENT_VERSION,
                    'key': MailStateBucket.key(user_id, account_version),
                    'value': MailStateBucket.serialize(state, MailStateBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise
