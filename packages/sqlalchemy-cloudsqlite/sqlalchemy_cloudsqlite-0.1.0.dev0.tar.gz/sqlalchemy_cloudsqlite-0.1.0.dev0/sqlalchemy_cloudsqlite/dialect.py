import hashlib
import json
import logging
import os
from datetime import datetime
from tempfile import gettempdir

from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

from . import storage


class CloudSQLiteDialect(SQLiteDialect_pysqlite):

    def __init__(self, *args, **kw):
        super(CloudSQLiteDialect, self).__init__(*args, **kw)
        self.db_hash = None
        self.file_name = None
        self.cache_duration = 0
        self.last_sync = datetime.fromtimestamp(0)
        self.storage_client = None
        self.connect_args = None

    @staticmethod
    def get_etag(file_path):
        """" Generate etag hash from file. """
        if os.path.isfile(file_path):
            m = hashlib.md5()
            with open(file_path, 'rb') as f:
                m.update(f.read())
            return m.hexdigest()
        return None

    def configure_database(self, dbname):
        self.file_name = os.path.join(gettempdir(), os.path.basename(dbname))

        # Init custom attributes
        config = json.loads(os.environ.get('config', {}))
        self.cache_duration = int(config.get('cache_duration', 0))
        try:
            self.connect_args = config['storage']
        except ValueError:
            raise ValueError("No storage configuration provided.")

        # Configure storage client
        self.storage_client = storage.StorageFactory.create(file_name=os.path.basename(dbname),
                                                            connect_args=self.connect_args)

        return self.file_name

    def download_database(self):
        """
        Load database from S3 and return the new local path.
        """
        file_name = self.file_name
        etag = self.get_etag(file_name)
        now = datetime.now()
        try:
            # Get new version from s3 if available or raise 304/404
            time_diff = (now - self.last_sync).total_seconds()
            if not etag or time_diff > self.cache_duration:
                logging.debug("Cache expired - check for new version...")
                self.storage_client.download(file_hash=etag, file_path=file_name)
            else:
                logging.debug("Cache active - use current version.")
                return

            # Update hash and last sync
            self.db_hash = self.get_etag(file_name)
            self.last_sync = now

            logging.debug("New version of database downloaded.")
        except Exception as exc:
            logging.debug(exc)
            raise

        return

    def upload_database(self):
        """
        Upload database to S3 if changed.
        """
        try:
            etag = self.get_etag(self.file_name)

            if not etag:
                logging.error("No database available.")
                return

            if self.db_hash == etag:
                logging.debug("Database has not changed - no upload necessary.")
                return

            self.storage_client.upload(file_path=self.file_name)

            # This instance has now the newest database
            self.last_sync = datetime.now()

        except Exception as exc:
            logging.debug(exc)
            raise exc

    def connect(self, *args, **kw):
        # Prepare database and set path to tmp dir
        local_name = self.configure_database(dbname=args[0])
        self.download_database()

        # Open database regularly
        return super(CloudSQLiteDialect, self).connect(local_name, **kw)

    def do_close(self, *args, **kw):
        # Close connection first
        out = super(CloudSQLiteDialect, self).do_close(*args, **kw)

        # Proceed with closed database
        self.upload_database()

        return out

    # Writing to database
    def do_commit(self, connection):
        result = super(CloudSQLiteDialect, self).do_commit(connection)
        self.upload_database()
        return result

    # Reading from database
    def do_executemany(self, cursor, statement, parameters, context=None):
        self.download_database()
        return super(CloudSQLiteDialect, self).do_executemany(cursor, statement, parameters, context)

    def do_execute(self, cursor, statement, parameters, context=None):
        self.download_database()
        return super(CloudSQLiteDialect, self).do_execute(cursor, statement, parameters, context)

    def do_execute_no_params(self, cursor, statement, context=None):
        self.download_database()
        return super(CloudSQLiteDialect, self).do_execute_no_params(cursor, statement, context)


dialect = CloudSQLiteDialect
