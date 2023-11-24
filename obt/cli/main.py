import click


from obt.core.config import Config
from obt.core.tools import backup_database

settings = Config()


@click.group()
def cli():
    """Odoo Module Generator"""


@click.command()
@click.argument("dbname")
@click.option(
    "--format", "-f", required=True, type=str, help="Format: zip, dump, folder"
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

    backup_database(dbname, **options)


cli.add_command(backup)
