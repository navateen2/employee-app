# import os
# from dotenv import load_dotenv
# load_dotenv()

# DATABASE_URL:str=os.environ["DATABASE_URL"]
# APP_ENV:str= os.getenv("APP_ENV","development")

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    app_env: str = "development"
    debug: bool = False
    model_config = SettingsConfigDict(env_file=".env")
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiry_minutes: int


settings = Settings()
