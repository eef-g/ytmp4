from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    download_dir: Path = Path("/app/downloads")
    cleanup_interval_minutes: int = 60
    max_concurrent_downloads: int = 3

    model_config = {"env_prefix": "YTMP4_"}


settings = Settings()
