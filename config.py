from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class PostgresConnectionSettings(BaseModel):
    host: str = 'localhost'
    port: int = 5432
    database: str = 'test_task'
    password: str
    user: str


class Settings(BaseSettings):
    db: PostgresConnectionSettings

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False
    )


settings = Settings()
