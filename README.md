
# Odoo Backup Tool

_**ORH** Command Line Tool_

![PyPI](https://img.shields.io/pypi/v/odoo-backup-tool) ![PyPI](https://img.shields.io/pypi/pyversions/odoo-backup-tool)

## Requirements



## Installation

Install from PyPI:
```bash
pip install odoo-backup-tool
```

## Quickstart


### Backup local database
```bash
obt backup DBNAME
```

### Backup and upload
```bash
obt backup-and-push --format <format>
```

```bash
Options:
  -d, --dbname TEXT   Database name
  -f, --format TEXT   Format: zip, dump, folder  [required]
  -n, --no-filestore  Do not include filestore.
  -p, --prefix TEXT   Use prefix in filename.
  -k, --keep          Do not delete files after backup.
  -a, --auth TEXT     Bucket authentication.
  -b, --bucket TEXT   Bucket name.
  --help              Show this message and exit.
```
