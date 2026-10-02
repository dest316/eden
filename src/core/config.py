from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, SecretStr


class EdenSettings(BaseModel):
    api_key: SecretStr = Field(default=SecretStr("sixseven"))


class ChatSettings(BaseModel):
    secret_key: SecretStr
    jwt_access_ttl: int
    jwt_refresh_ttl: int


class CoreSettings(BaseModel):
    database_dsn: SecretStr


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", extra="ignore"
    )

    chat: ChatSettings
    core: CoreSettings
    eden: EdenSettings
