
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """
    Application settings from environment variables.
    
    Reads from .env file in project root.
    """
    
    # ===== DATABASE =====
    DATABASE_URL: str = "postgresql://postgres:QWERTY@localhost:5432/ecommerce"
    SQLALCHEMY_ECHO: bool = False
    
    # ===== REDIS =====
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    
    # ===== ELASTICSEARCH =====
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_INDEX: str = "products"
    
    # ===== API =====
    API_TITLE: str = "E-Commerce Search Engine"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # ===== LOGGING =====
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get settings instance (cached)."""
    return Settings()


settings = get_settings()


if __name__ == "__main__":
    print("=== Configuration ===")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"API Version: {settings.API_VERSION}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Redis: {settings.REDIS_URL}")
    print(f"Elasticsearch: {settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}")