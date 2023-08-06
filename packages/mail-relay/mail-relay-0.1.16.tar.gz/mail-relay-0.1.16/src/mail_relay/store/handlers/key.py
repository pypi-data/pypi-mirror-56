from mail_relay.store.buckets import KeyBucket, TempDeviceKeyBycket
from pvHelpers.store import GetDBSession


def write_key(user_id, account_version, key, bucket, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': bucket.NAME,
                    'version': bucket.CURRENT_VERSION,
                    'key': bucket.key(user_id, account_version, key.key_version),
                    'value': bucket.serialize(key, bucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def write_user_key(user_id, account_version, user_key, store_path):
    return write_key(
        user_id, account_version, user_key, KeyBucket, store_path)


def write_temp_device_key(user_id, account_version, device_key, store_path):
    return write_key(
        user_id, account_version, device_key, TempDeviceKeyBycket, store_path)


def read_key(user_id, account_version, key_version, bucket, store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key = :key
            ''', {
                'bucket': bucket.NAME,
                'key': bucket.key(user_id, account_version, key_version)
            }
        )
        (_, blob, b_v) = result.fetchall()[0]

    return bucket.deserialize(blob, b_v)


def read_user_key(user_id, account_version, key_version, store_path):
    return read_key(
        user_id, account_version, key_version, KeyBucket, store_path)


def read_temp_device_key(user_id, account_version, store_path):
    return read_key(
        user_id, account_version, -5, TempDeviceKeyBycket, store_path)


def read_keys(user_id, account_version, bucket, store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key LIKE :key
            ''', {
                'bucket': bucket.NAME,
                'key': bucket.key(user_id, account_version, '%')
            }
        )
        results = result.fetchall()

    return [bucket.deserialize(blob, b_v) for (_, blob, b_v) in results]


def read_user_keys(user_id, account_version, store_path):
    return read_keys(
        user_id, account_version, KeyBucket, store_path)
