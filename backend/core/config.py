# Act as setting for backend 
from pydantic_settings import BaseSettings  # for reading the environment variables

from typing import List

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BetMasterX"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # MCP Configuration
    MCP_SERVER_URL: str = "http://localhost:8080"
    
    # Database
    DATABASE_URL: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()