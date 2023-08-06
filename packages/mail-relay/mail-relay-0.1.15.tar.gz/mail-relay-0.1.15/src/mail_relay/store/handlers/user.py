from mail_relay.store.buckets import KeyBucket, UserBucket
from pvHelpers.store import GetDBSession
from pvHelpers.utils import CaseInsensitiveDict, MergeDicts

from .key import read_user_keys


def write_user(user, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': UserBucket.NAME,
                    'version': UserBucket.CURRENT_VERSION,
                    'key': UserBucket.key(user.user_id, user.account_version),
                    'value': UserBucket.serialize(user, UserBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def update_user_info(user, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                UPDATE Store
                SET value = :value
                WHERE bucket = :bucket
                AND key = :key
                ''', {
                    'bucket': UserBucket.NAME,
                    'key': UserBucket.key(user.user_id, user.account_version),
                    'value': UserBucket.serialize(user, UserBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def delete_user(user_id, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            session.execute(
                '''
                DELETE FROM Store
                WHERE bucket=:bucket
                AND key LIKE :key
                ''', {
                    'bucket': UserBucket.NAME,
                    'key': UserBucket.key(user_id, '%')
                }
            )
            session.execute(
                '''
                DELETE FROM Store
                WHERE bucket=:bucket
                AND key LIKE :key
                ''', {
                    'bucket': KeyBucket.NAME,
                    'key': KeyBucket.key(user_id, '%', '%')
                }
            )
            session.commit()
        except Exception:
            session.rollback()
            raise


# TODO: improve performance/memory adding single read handler
def read_user(user_id, account_version, store_path):
    pass


def read_users(store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket
            ''', {
                'bucket': UserBucket.NAME
            }
        )
        results = result.fetchall()

    users = [UserBucket.deserialize(blob, b_v) for (_, blob, b_v) in results]

    for u in users:
        u.user_keys = read_user_keys(u.user_id, u.account_version, store_path)

    latest_versions = CaseInsensitiveDict()
    for u in users:
        if (-1, u.user_id) in latest_versions and \
           latest_versions[(-1, u.user_id)].account_version < u.account_version:

            latest_versions[(-1, u.user_id)] = u

        else:
            latest_versions[(-1, u.user_id)] = u

    return CaseInsensitiveDict(MergeDicts(
        {(u.account_version, u.user_id): u for u in users},
        latest_versions
    ))
