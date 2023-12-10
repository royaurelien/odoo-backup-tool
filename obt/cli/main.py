import sys

import click

from obt.core.settings import get_settings

settings = get_settings()  # pylint: disable=C0413

from obt.core.tools import backup_database, clean_files, upload_blob  # noqa: E402


@click.group()
def cli():
    """Odoo Backup Tool"""


@click.command()
@click.argument("dbname")
@click.option(
    "--format",
    "-f",
    required=True,
    type=str,
    help="Format: zip, dump, folder.",
)
@click.option(
    "--no-filestore",
    "-n",
    is_flag=True,
    default=False,
    type=bool,
    help="Do not include filestore.",
)
@click.option("--prefix", "-p", required=False, type=str, help="Use prefix")
def backup(dbname, no_filestore, **kwargs):
    options = {
        "filestore": not no_filestore,
        "ttype": kwargs.get("format"),
        "prefix": kwargs.get("prefix", False),
    }

    res, _, filepath = backup_database(dbname, **options)
    if not res:
        sys.exit(1)

    print(filepath)


@click.command()
@click.option(
    "--dbname",
    "-d",
    required=False,
    default=None,
    type=str,
    help="Database name.",
)
@click.option(
    "--format",
    "-f",
    required=True,
    type=str,
    help="Format: zip, dump, folder.",
)
@click.option(
    "--no-filestore",
    "-n",
    is_flag=True,
    default=False,
    type=bool,
    help="Do not include filestore.",
)
@click.option(
    "--prefix",
    "-p",
    required=False,
    type=str,
    help="Use prefix in filename.",
)
@click.option(
    "--keep",
    "-k",
    is_flag=True,
    default=False,
    type=bool,
    help="Do not delete files after backup.",
)
@click.option(
    "--auth",
    "-a",
    required=False,
    type=str,
    help="Bucket authentication.",
)
@click.option(
    "--bucket",
    "-b",
    required=False,
    type=str,
    help="Bucket name.",
)
def backup_and_push(dbname, no_filestore, **kwargs):
    options = {
        "filestore": not no_filestore,
        "ttype": kwargs.get("format"),
        "prefix": kwargs.get("prefix", False),
    }
    delete = True if not kwargs.get("keep", False) else True
    bucket = kwargs.get("bucket", False)
    auth = kwargs.get("auth", False)

    if auth:
        auth = eval(auth)

    res, filename, filepath = backup_database(
        dbname or settings.default_database, **options
    )
    if not res:
        sys.exit(1)

    upload_blob(
        bucket or settings.bucket_name,
        filepath,
        filename,
        auth or settings.json_auth,
    )

    if delete:
        clean_files(filepath)


cli.add_command(backup_and_push)
cli.add_command(backup)
