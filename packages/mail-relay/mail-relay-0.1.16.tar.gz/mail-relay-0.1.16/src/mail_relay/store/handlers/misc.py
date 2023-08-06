from pvHelpers.store import GetDBSession


def remove_records(record_ids, store_path):
    with GetDBSession(store_path) as session:
        try:
            session.begin()
            session.connection().execute(
                '''
                DELETE FROM Store
                WHERE id IN ({})
                '''.format(', '.join('?' for _ in record_ids)),
                record_ids
            )
            session.commit()
        except Exception:
            session.rollback()
            raise
