from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url

class Settings(BaseSettings):
    PROJECT_NAME: str = "GroceryWise API"
    API_V1_STR: str = "/api/v1"

    # Annotate the DATABASE_URL with the correct type
    DATABASE_URL: str = get_database_url()  # Ensure this is properly typed as a string

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        case_sensitive = True

settings = Settings()
