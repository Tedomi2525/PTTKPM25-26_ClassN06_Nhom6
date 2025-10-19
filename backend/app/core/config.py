from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Xác định BASE_DIR = thư mục gốc dự án (nơi chứa file .env)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(f"📁 BASE_DIR: {BASE_DIR}")

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:Quanopo123+@localhost:5432/PTTK"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    KMP_DUPLICATE_LIB_OK: str = "TRUE"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),   # Đọc từ file .env
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

# Khởi tạo config
settings = Settings()

# In ra các giá trị đã load được
print("✅ Đã load cấu hình từ .env:")
for key, value in settings.model_dump().items():
    print(f"{key} = {value}") 
   