from setuptools import find_packages, setup

setup(
    name="odoo-backup-tool",
    version="0.0.3",
    description="Odoo Backup Tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/royaurelien/odoo-backup-tool",
    author="Aurelien ROY",
    author_email="roy.aurelien@gmail.com",
    license="BSD 2-clause",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "click-odoo-contrib",
        "google",
    ],
    entry_points={
        "console_scripts": [
            "obt = obt.cli.main:cli",
        ],
    },
)
