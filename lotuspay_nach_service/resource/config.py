
from pydantic import BaseSettings



class Settings(BaseSettings):
    # lotuspay_url: str = 'http://api-test.lotuspay.com/v1'
    lotuspay_url: str = None

    class Config:
        env_file = "resource/.env"
        env_file_encoding = 'utf-8'


settings = Settings()
