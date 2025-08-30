from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # Database settings (granular)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "fastapi_db"
    # Legacy single URL (optional, if set overrides granular parts)
    DB_URL: str | None = None
    
    # Security settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Application settings
    LOG_LEVEL: str = "INFO"
    WORKERS_COUNT: int = 4
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL unless legacy DB_URL provided."""
        if self.DB_URL:
            return self.DB_URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Backwards compatibility accessor
    @property
    def effective_db_url(self) -> str:  # alias if other code imported differently
        return self.DATABASE_URL
    
    @property
    def CORS_ORIGIN_LIST(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.CORS_ORIGINS, str):
            return json.loads(self.CORS_ORIGINS)
        return self.CORS_ORIGINS
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
