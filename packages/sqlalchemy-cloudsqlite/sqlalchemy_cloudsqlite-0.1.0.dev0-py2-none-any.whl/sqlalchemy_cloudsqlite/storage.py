import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

import boto3
import botocore


def datetime_to_epoch(d1):
    d2 = datetime(1970, 1, 1, tzinfo=d1.tzinfo)
    time_delta = d1 - d2
    ts = int(time_delta.total_seconds())
    return ts


class StorageFactory(object):
    @staticmethod
    def create(file_name, connect_args=None):
        if connect_args is None:
            raise ValueError("Invalid Cloud Storage.")

        if connect_args.get("S3"):
            # Prepare Clients
            bucket_name = connect_args.get('S3').get('bucket_name')
            if not bucket_name:
                raise ValueError("No S3 bucket configured.")

            return S3StorageClient(bucket_name=bucket_name, key=file_name)

        return ValueError("Storage not supported.")


class StorageClient(ABC):
    @abstractmethod
    def download(self, file_path, file_hash):
        raise NotImplementedError

    @abstractmethod
    def upload(self, file_path):
        raise NotImplementedError


class S3StorageClient(StorageClient):
    def __init__(self, bucket_name, key):
        self.client = self.s3_client.Object(bucket_name, key)

    @property
    def s3_client(self):
        """ Get S3 client. """
        return boto3.resource('s3')

    def download(self, file_path, file_hash):

        result = self.get(file_hash=file_hash)

        if result:
            # Write new version to filesystem
            with open(file_path, 'wb') as fb:
                fb.write(result['Body'].read())

            # Set last modified attribute
            last_modified = datetime_to_epoch(result['LastModified'])
            os.utime(file_path, (last_modified, last_modified))

    def upload(self, file_path):
        with open(file_path, 'rb') as fb:
            self.client.put('rb', Body=fb)
            logging.debug("Database uploaded to S3.")

    def get(self, file_hash):
        try:
            if file_hash:
                return self.client.get(IfNoneMatch=file_hash)
            return self.client.get()
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '304':
                # Remote file has the same hash - no download necessary.
                logging.debug("No new database version available - using the existing one.")
            else:
                logging.debug("Could not download database: %s" % error_code)
                raise FileNotFoundError("File not found in S3 bucket.")
