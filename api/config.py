"""
MEMBRA Configuration

Environment variables and application settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "MEMBRA"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/membra"
    
    # Redis (for caching and queues)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Geolocation
    DEFAULT_RADIUS_MILES: float = 2.0
    
    # Fees
    PLATFORM_FEE_PERCENTAGE: float = 10.0
    ALPHA_HUB_FEE_PERCENTAGE: float = 12.0
    
    # Credits
    SIGNUP_BONUS_CREDITS: int = 100
    REFERRAL_BONUS_CREDITS: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
