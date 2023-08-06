from mail_relay.store.buckets import ConfigBucket, UserBucket
from pvHelpers.store import GetDBSession


def update_config(config, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT OR REPLACE INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': ConfigBucket.NAME,
                    'version': ConfigBucket.CURRENT_VERSION,
                    'key': ConfigBucket.key(),
                    'value': ConfigBucket.serialize(config, UserBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def read_config(store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key = :key
            ''', {
                'bucket': ConfigBucket.NAME,
                'key': ConfigBucket.key()
            }
        )
        results = result.fetchall()

    if len(results) == 1:
        (_, blob, b_v) = results[0]
        return ConfigBucket.deserialize(blob, b_v)

    return None
