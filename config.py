# import os
# from dotenv import load_dotenv
# load_dotenv()

# DATABASE_URL:str=os.environ["DATABASE_URL"]
# APP_ENV:str= os.getenv("APP_ENV","development")

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    database_url: str
    app_env: str = "development"
    debug: bool = False
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiry_minutes:int
    jwt_refresh_token_expire_minutes: int
    OPENAI_API_KEY:str
    OPENAI_BASE_URL:str


settings = Settings()
