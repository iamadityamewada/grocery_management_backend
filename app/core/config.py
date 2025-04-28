import os
from pydantic_settings import BaseSettings
# from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Settings(BaseSettings):
    PROJECT_NAME: str = "GroceryWise API"
    API_V1_STR: str = "/api/v1"

    # Database
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key") # Provide a default or ensure it's in .env
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10000))

    class Config:
        case_sensitive = True
        # env_file = ".env" # Already handled by load_dotenv


settings = Settings()
