from mail_relay.store.buckets import ExporterBucket, ExportStateBucket
from pvHelpers.store import GetDBSession


def write_exporter(user_id, account_version, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT OR REPLACE INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': ExporterBucket.NAME,
                    'version': ExporterBucket.CURRENT_VERSION,
                    'key': ExporterBucket.key(),
                    'value': ExporterBucket.serialize(user_id, account_version, ExporterBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def read_exporter(store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key = :key
            ''', {
                'bucket': ExporterBucket.NAME,
                'key': ExporterBucket.key()
            }
        )
        r = result.fetchone()
    if r is not None:
        (_, blob, b_v) = r
        return ExporterBucket.deserialize(blob, b_v)
    return (None, None)


def add_or_update_export_state(export_state, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            res = session.execute(
                '''
                INSERT OR REPLACE INTO Store (bucket, bucket_version, key, value)
                VALUES (:bucket, :version, :key, :value)
                ''', {
                    'bucket': ExportStateBucket.NAME,
                    'version': ExportStateBucket.CURRENT_VERSION,
                    'key': ExportStateBucket.key(),
                    'value': ExportStateBucket.serialize(export_state, ExportStateBucket.CURRENT_VERSION)
                }
            )
            session.commit()
            return res.lastrowid
        except Exception:
            session.rollback()
            raise


def read_export_state(store_path):
    with GetDBSession(store_path) as session:
        result = session.execute(
            '''
            SELECT id, value, bucket_version FROM Store
            WHERE bucket = :bucket AND key = :key
            ''', {
                'bucket': ExportStateBucket.NAME,
                'key': ExportStateBucket.key()
            }
        )
        r = result.fetchone()
    if r is not None:
        (_, blob, b_v) = r
        return ExportStateBucket.deserialize(blob, b_v)

    return None
