from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env_file: ClassVar[str] = '.env'
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"
    DATABASE_URL: str
    
settings = Settings()
