#!/bin/python3

import click


from obt.core.config import Config
from obt.cli.parse import parse

settings = Config()


@click.group()
def cli():
    """Odoo Module Generator"""


cli.add_command(parse)
