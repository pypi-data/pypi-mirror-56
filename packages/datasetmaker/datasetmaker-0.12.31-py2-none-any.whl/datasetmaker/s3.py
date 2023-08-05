"""Collection of utilities for reading and writing to AWS S3."""

import gzip
import io
import json
import logging
import os
import sys
from pathlib import Path
from typing import Generator, Union

import boto3
import botocore
import pandas as pd

from datasetmaker.utils import CSV_DTYPES

log = logging.getLogger(__name__)


def download_file(bucket: str, local_path: Union[str, Path], remote_path: str) -> None:
    """
    Download a file from an S3 bucket.

    Parameters
    ----------
    bucket
        Bucket name.
    local_path
        Local save location.
    remote_path
        Path to remote file, i.e. S3 object key.
    """
    client = boto3.client('s3')
    client.download_file(Bucket=bucket, Key=remote_path, Filename=str(local_path))


def download_dir(bucket: str, local_path: Union[str, Path], remote_path: str) -> None:
    """
    Download a directory from an S3 bucket.

    Parameters
    ----------
    bucket
        Bucket name.
    local_path
        Local save location.
    remote_path
        Path to remote directory, i.e. S3 object key.
    """
    client = boto3.client('s3')
    local_path = Path(local_path)
    if not local_path.exists():
        local_path.mkdir()
    files = client.list_objects(Bucket=bucket, Prefix=remote_path)['Contents']
    for file in files:
        file_path = Path(file['Key'])
        download_file(bucket, local_path / file_path.name, file['Key'])


def upload_file(bucket: str, local_path: Union[str, Path], remote_path: str) -> None:
    """
    Upload a local file to an S3 bucket.

    Parameters
    ----------
    bucket
        Bucket name.
    local_path
        Local file location.
    remote_path
        Path to remote file, i.e. S3 object key.
    """
    client = boto3.client('s3')
    local_path = Path(local_path)
    if local_path.name.startswith('.'):  # exclude dotfiles
        return
    if local_path.is_file():
        client.upload_file(Bucket=bucket,
                           Filename=str(local_path),
                           Key=str(remote_path))


def upload_dir(bucket: str, local_path: Union[str, Path], remote_path: str) -> None:
    """
    Upload a local directory to an S3 bucket.

    Parameters
    ----------
    bucket
        Bucket name.
    local_path
        Local directory location.
    remote_path
        Path to remote directory, i.e. S3 object key.
    """
    local_path = Path(local_path)
    if local_path.is_dir():
        output = os.walk(local_path)
        for dirpath, dirnames, filenames in output:
            for filename in filenames:
                local_file_path = os.path.join(dirpath, filename)
                ldir = dirpath.replace(str(local_path), '')[1:]
                remote_file_path = os.path.join(ldir, filename)
                remote_file_path = os.path.join(remote_path, remote_file_path)
                upload_file(bucket, local_file_path, remote_file_path)
    else:
        log.error(f'No files to upload in {local_path}')
        sys.exit(1)


def list_files_in_s3_directory(bucket: str,
                               remote_path: str,
                               suffix: Union[str, None] = None) -> Generator:
    """
    List all files in `remote_path` on S3.

    Parameters
    ----------
    bucket
        Bucket name.
    remote_path
        Path to remote directory, i.e. S3 object key.
    suffix
        Optional suffix to filter by.
    """
    client = boto3.client('s3')
    for obj in client.list_objects(Bucket=bucket, Prefix=remote_path)['Contents']:
        path = Path(obj['Key'])
        if str(path) == remote_path:
            continue
        if not suffix:
            yield obj['Key']
        elif suffix and path.suffix[1:] == suffix:
            yield obj['Key']


def read_remote_csv(bucket: str, remote_path: str) -> pd.DataFrame:
    """
    Read a remote CSV file.

    Parameters
    ----------
    bucket
        Bucket name.
    remote_path
        Path to remote CSV file, i.e. S3 object key.
    """
    client = boto3.client('s3')
    log.info(f'Reading CSV file with key {remote_path}')
    obj = client.get_object(Bucket=bucket, Key=remote_path)
    text = io.BytesIO(obj['Body'].read())
    if 'gzip' in obj.get('ContentEncoding', ''):
        return pd.read_csv(text, compression='gzip', dtype=CSV_DTYPES)
    else:
        return pd.read_csv(text, dtype=CSV_DTYPES)


def read_remote_json(bucket: str, remote_path: str) -> pd.DataFrame:
    """
    Read a remote JSON file.

    Parameters
    ----------
    bucket
        Bucket name.
    remote_path
        Path to remote CSV file, i.e. S3 object key.
    """
    client = boto3.client('s3')
    log.info(f'Reading JSON file with key {remote_path}')
    obj = client.get_object(Bucket=bucket, Key=remote_path)
    bytes_ = io.BytesIO(obj['Body'].read())
    return json.loads(bytes_.read())


def write_remote_csv(frame: pd.DataFrame, bucket: str, remote_path: str) -> None:
    """
    Write and upload a CSV file remotely.

    Parameters
    ----------
    frame
        Dataframe to write as CSV.
    bucket
        Bucket name.
    remote_path
        Remote key to write to.
    """
    csv_buffer = io.BytesIO()
    with gzip.GzipFile(mode='w', fileobj=csv_buffer) as gz_file:
        frame.to_csv(io.TextIOWrapper(gz_file, 'utf8'), index=False)  # type: ignore
    obj = boto3.resource('s3').Object(bucket, remote_path)
    obj.put(Body=csv_buffer.getvalue(), ContentEncoding='gzip', ContentType='text/csv')


def obj_exists(bucket: str, remote_path: str) -> bool:
    """
    Check whether remote object exists.

    Parameters
    ----------
    bucket
        Bucket name.
    remote_path
        Object key.
    """
    client = boto3.client('s3')
    try:
        client.get_object(Bucket=bucket, Key=remote_path)
    except botocore.exceptions.ClientError:
        return False
    return True
