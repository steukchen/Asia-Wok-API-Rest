from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API Asia Wok"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str 
    ALGORITHM: str 
    SECRET_KEY: str
    PROJECT_DESCRIPTION: str = "API REST to Asia Wok"
    PROJECT_VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
