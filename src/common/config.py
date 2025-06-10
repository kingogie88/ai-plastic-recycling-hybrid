"""
Configuration settings for AI Circo Recycling System.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    """System configuration settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Circo Recycling"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SSL_KEYFILE: Optional[Path] = None
    SSL_CERTFILE: Optional[Path] = None
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recycling.db")

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"

    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS: List[str] = ["localhost:9092"]

    # Vision System
    MODEL_PATH: Path = Path("models/plastic_yolo11.pt")
    CONFIDENCE_THRESHOLD: float = 0.85

    # Robot Control
    ROBOT_CONTROL_PORT: int = 50051
    EMERGENCY_STOP_TIMEOUT: float = 1.0  # seconds

    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    METRICS_EXPORT_INTERVAL: int = 15  # seconds

    # Blockchain
    BLOCKCHAIN_NETWORK: str = "testnet"
    BLOCKCHAIN_RPC_URL: str = "http://localhost:8545"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Performance
    BATCH_SIZE: int = 32
    MAX_WORKERS: int = os.cpu_count() or 4
    PROCESSING_TIMEOUT: int = 30  # seconds

    class Config:
        """Pydantic config"""

        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Example usage
if __name__ == "__main__":
    print("Current configuration:")
    print(f"API Version: {settings.API_V1_PREFIX}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Model Path: {settings.MODEL_PATH}")
    print(f"Log Level: {settings.LOG_LEVEL}")
