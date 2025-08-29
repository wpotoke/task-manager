from functools import lru_cache

import decouple

from app.config.settings.base import BackendBaseSettings
from app.config.settings.development import BackendDevSettings
from app.config.settings.invironment import Environment


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self, *args, **kwds):
        if self.environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        return "return prod settings"


@lru_cache()
def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory(
        environment=decouple.config("ENVIRONMENT", default="DEV", cast=str)
    )


settings: BackendBaseSettings = get_settings()
