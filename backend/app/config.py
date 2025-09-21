import os
from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str 
    VERSION: str 
    DEBUG: bool 
    DATABASE_URL: str 
    HOST: str
    PORT: int
    DOCS_URL: str
    REDOCS_URL : str


    class Config:
        env_file = ".env"

settings = Settings()