import os
from functools import lru_cache

from appdirs import AppDirs
from pydantic import ValidationError
from pydantic_settings import BaseSettings

from ota.core.console import console
from ota.core.tools import ROOT_DIR, save_to

CONFIG_FILENAME = "config.json"
DIRS = AppDirs("obt", "Aurelien ROY")


def init_dirs():
    os.makedirs(DIRS.user_data_dir, exist_ok=True)
    console.log(ROOT_DIR)


def get_config_path():
    return DIRS.user_data_dir


def get_config_filepath():
    return os.path.join(get_config_path(), CONFIG_FILENAME)


init_dirs()


class Settings(BaseSettings):
    version: str = "0.1.0"

    url: str = "http://127.0.0.1:8080"
    local_url: str = "http://0.0.0.0:8080"
    bucket_name: str = os.getenv("BUCKET_NAME", "")
    json_auth: str = os.getenv("JSON_AUTH", "")

    @classmethod
    def new_file(cls, save=True):
        """Get defaults settings and save"""
        self = cls()
        if save:
            self.save()

        return self

    def save(self, clear=False):
        """Save settings to JSON file"""
        pass


@lru_cache()
def get_settings():
    return Settings.new_file(False)
