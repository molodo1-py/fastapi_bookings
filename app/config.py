from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["INFO", "DEBUG"]
    
    DB_URL: str
    TEST_DB_URL: str
    
    ACCESS_KEY: str
    ACCESS_ALGORITHM: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_URL: str
        
    class Config:
        env_file=".env"
        
settings = Settings()