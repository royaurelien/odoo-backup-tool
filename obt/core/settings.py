import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

CONFIG_PATH = Path(".obt")
CONFIG_FILEPATH = Path(".obt", "config.json")


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding")
        file_content_json = json.loads(CONFIG_FILEPATH.read_text(encoding))
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        encoding = self.config.get("env_file_encoding")

        if not CONFIG_PATH.exists():
            CONFIG_PATH.mkdir()

        if not CONFIG_FILEPATH.exists():
            with open(CONFIG_FILEPATH, "w", encoding=encoding) as f:
                default_values = {
                    key: os.getenv(key.upper()) or ""
                    for key in self.settings_cls.model_fields.keys()
                    if key != "auth"
                }
                f.write(json.dumps(default_values))

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")
    version: str = "0.1.0"

    bucket_name: str
    env_json_auth: str
    default_database: str
    auth: Optional[dict] = {}

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )

    @property
    def json_auth(self) -> dict:
        if self.auth:
            return self.auth
        elif self.env_json_auth:
            json.loads(self.env_json_auth)
        return {}


# @lru_cache()
def get_settings():
    return Settings()
