from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI Movies"
    admin_email: str = "lestatuk@gmail.com"
    database_url: str
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str
    actor_api: str
    movie_api: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
