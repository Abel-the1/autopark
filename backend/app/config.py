from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    postgres_user: str = "fleet_user"
    postgres_password: str = "fleet_pass"
    postgres_db: str = "fleet_db"
    postgres_host: str = "db"
    postgres_port: int = 5432

    secret_key: str = "change_me"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    bot_token: str = ""
    allowed_users: str = ""

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
