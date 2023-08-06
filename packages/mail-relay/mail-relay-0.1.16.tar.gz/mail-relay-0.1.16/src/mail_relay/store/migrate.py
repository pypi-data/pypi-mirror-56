from pvHelpers.store import GetDBSession


def migrate(wd):
    with GetDBSession(wd) as s:
        with s.begin():
            s.execute('DROP TABLE IF EXISTS Store')
            s.execute(
                '''
                CREATE TABLE Store
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bucket TEXT NOT NULL COLLATE NOCASE,
                    bucket_version INTEGER NOT NULL,
                    key TEXT NOT NULL COLLATE NOCASE,
                    value BLOB NOT NULL,
                    UNIQUE (bucket, key))
                '''
            )
            s.execute('CREATE INDEX bucket_idx ON Store(bucket)')
            s.execute('CREATE INDEX key_idx ON Store(key)')

            s.execute('DROP TABLE IF EXISTS MailState')
            s.execute(
                '''
                CREATE TABLE MailState
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bucket TEXT NOT NULL COLLATE NOCASE,
                    bucket_version INTEGER NOT NULL,
                    key TEXT NOT NULL COLLATE NOCASE,
                    value BLOB NOT NULL,
                    UNIQUE (bucket, key))
                '''
            )
