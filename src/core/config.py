from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Movies"
    admin_email: str = "lestatuk@gmail.com"
    database_url: PostgresDsn | None = None
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str
    actor_api: str
    movie_api: str

    model_config = SettingsConfigDict(env_file=".env")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.database_url:
            self.database_url = PostgresDsn.build(
                scheme="postgres+asyncpg",
                username=self.db_user,
                password=self.db_pass,
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )


settings = Settings()
