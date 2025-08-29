import enum


class Environment(str, enum.Enum):
    DEVELOPMENT: str = "DEV"
    PRODUCTION: str = "PROD"
