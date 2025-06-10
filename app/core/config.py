from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Asia Wok"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PROJECT_DESCRIPTION: str = "API REST to Asia Wok"
    PROJECT_VERSION: str = "0.1.0"

settings = Settings()