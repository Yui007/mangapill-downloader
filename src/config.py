"""
Configuration management for Mangapill Downloader.
Handles loading/saving user settings from config.json.
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from .constants import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_KEEP_IMAGES,
    DEFAULT_MAX_CHAPTER_WORKERS,
    DEFAULT_MAX_IMAGE_WORKERS,
    DEFAULT_RETRY_COUNT,
    DEFAULT_RETRY_BASE_DELAY,
)

# Config file path (in project root)
CONFIG_FILE = Path(__file__).parent.parent / "config.json"


@dataclass
class Config:
    """User configuration settings."""
    
    output_dir: str = DEFAULT_OUTPUT_DIR
    output_format: str = DEFAULT_OUTPUT_FORMAT
    keep_images: bool = DEFAULT_KEEP_IMAGES
    max_chapter_workers: int = DEFAULT_MAX_CHAPTER_WORKERS
    max_image_workers: int = DEFAULT_MAX_IMAGE_WORKERS
    retry_count: int = DEFAULT_RETRY_COUNT
    retry_base_delay: float = DEFAULT_RETRY_BASE_DELAY
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create config from dictionary."""
        return cls(
            output_dir=data.get("output_dir", DEFAULT_OUTPUT_DIR),
            output_format=data.get("output_format", DEFAULT_OUTPUT_FORMAT),
            keep_images=data.get("keep_images", DEFAULT_KEEP_IMAGES),
            max_chapter_workers=data.get("max_chapter_workers", DEFAULT_MAX_CHAPTER_WORKERS),
            max_image_workers=data.get("max_image_workers", DEFAULT_MAX_IMAGE_WORKERS),
            retry_count=data.get("retry_count", DEFAULT_RETRY_COUNT),
            retry_base_delay=data.get("retry_base_delay", DEFAULT_RETRY_BASE_DELAY),
        )


def load_config() -> Config:
    """Load configuration from file, or create default if not exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Config.from_dict(data)
        except (json.JSONDecodeError, IOError):
            # Return default config if file is corrupted
            return Config()
    return Config()


def save_config(config: Config) -> bool:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config.to_dict(), f, indent=2)
        return True
    except IOError:
        return False


def get_config() -> Config:
    """Get the current configuration (singleton-like access)."""
    return load_config()
