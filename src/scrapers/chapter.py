"""
Chapter image scraper for Mangapill.
Refactored from chapterimage.py with retry logic.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional

from ..constants import HEADERS, DEFAULT_REQUEST_TIMEOUT
from ..downloader.retry import retry_request
from ..config import get_config


def scrape_chapter_images(url: str) -> list[str]:
    """
    Scrape all image URLs from a Mangapill chapter page.
    
    Args:
        url: Full URL to the chapter page
        
    Returns:
        List of image URLs in order
    """
    config = get_config()
    
    @retry_request(max_retries=config.retry_count, base_delay=config.retry_base_delay)
    def fetch_page(page_url: str) -> str:
        response = requests.get(page_url, headers=HEADERS, timeout=DEFAULT_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    
    images = []
    for img in soup.select("img.js-page"):
        src = img.get("data-src") or img.get("src")
        if src:
            images.append(src)
    
    return images


def get_chapter_title_from_url(url: str) -> Optional[str]:
    """
    Extract chapter title from URL for folder naming.
    
    Args:
        url: Chapter URL
        
    Returns:
        Chapter title or None
    """
    import re
    # Extract chapter number from URL
    # e.g., "solo-leveling-ragnarok-chapter-1" -> "Chapter 1"
    match = re.search(r'chapter-(\d+(?:\.\d+)?)', url, re.IGNORECASE)
    if match:
        return f"Chapter {match.group(1)}"
    return None
