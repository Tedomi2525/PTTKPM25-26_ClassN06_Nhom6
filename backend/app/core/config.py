from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Lấy đường dẫn tuyệt đối đến thư mục backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:123321@localhost:5432/qldt"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Other Configuration
    KMP_DUPLICATE_LIB_OK: str = "TRUE"

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False
    )


settings = Settings()
