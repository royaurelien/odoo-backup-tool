#!/bin/python3

import click
import numpy as np
import pandas as pd
from tabulate import tabulate

from obt.core.config import Config

settings = Config()


@click.command()
@click.argument("path")
@click.argument("output")
def parse(path, output):
    pass
