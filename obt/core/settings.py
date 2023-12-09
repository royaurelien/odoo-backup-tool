import os
from functools import lru_cache
import json

# from pydantic import ValidationError
from pydantic_settings import BaseSettings


# from obt.core.tools import ROOT_DIR


class Settings(BaseSettings):
    version: str = "0.1.0"

    bucket_name: str = os.getenv("BUCKET_NAME", "")
    env_json_auth: str = os.getenv("JSON_AUTH", "")
    default_database: str = os.getenv("DATABASE", "")

    @classmethod
    def new_file(cls, save=False):
        """Get defaults settings and save"""
        self = cls()
        if save:
            self.save()

        return self

    def save(self, clear=False):
        """Save settings to JSON file"""
        pass

    @property
    def json_auth(self):
        # return eval(self.env_json_auth) if self.env_json_auth else {}
        return json.loads(self.env_json_auth) if self.env_json_auth else {}


@lru_cache()
def get_settings():
    return Settings.new_file(False)
