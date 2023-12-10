import logging
import os
import subprocess
from datetime import datetime

from google.cloud import storage
from google.oauth2 import service_account

_logger = logging.getLogger(__name__)


def get_storage(json_account_info):
    credentials = service_account.Credentials.from_service_account_info(
        json_account_info
    )
    return storage.Client(credentials=credentials)


def get_bucket(storage_client, name):
    return storage_client.bucket(name)


def upload_blob(
    bucket_name, source_file_name, destination_blob_name, json_account_info
):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    _logger.error(json_account_info)

    storage_client = get_storage(json_account_info)
    bucket = get_bucket(storage_client, bucket_name)

    # storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(
        source_file_name, if_generation_match=generation_match_precondition
    )

    _logger.warning("File %s uploaded to %s.", source_file_name, destination_blob_name)


def backup_database(dbname, **kwargs):
    if not dbname:
        raise ValueError("Database name is mandatory.")

    filestore = kwargs.get("filestore", True)
    ttype = kwargs.get("ttype", "zip")
    prefix = kwargs.pop("prefix", False)
    path = kwargs.pop("path", "/tmp")
    args = ["click-odoo-backupdb"]

    if not filestore:
        args.append("--no-filestore")

    if ttype:
        args += ["--format", ttype]

    args.append(dbname)
    suffix = "obt_no_fs" if not filestore else "obt"

    filename = get_name(dbname, ttype, prefix, suffix)
    filepath = os.path.join(path, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    args.append(filepath)

    _logger.debug(args)

    try:
        subprocess.run(args)
        res = True
    except Exception as error:
        res = False
        _logger.error(error)

    return res, filename, filepath


def get_name(dbname, ttype, prefix=None, suffix=None):
    now = datetime.now()
    string_date = now.strftime("%Y-%m-%d_%H%M")

    if not suffix:
        suffix = "obt"

    res = f"{prefix or dbname}_{dbname}_{string_date}_{suffix}"

    if ttype == "zip":
        res += ".zip"
    elif ttype == "dump":
        res += ".dump"

    return res


def clean_files(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
