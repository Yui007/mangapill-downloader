"""
Manga information scraper for Mangapill.
Refactored from mangainfo.py with dataclass and retry logic.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dataclasses import dataclass, field
from typing import Optional

from ..constants import HEADERS, BASE_URL, DEFAULT_REQUEST_TIMEOUT
from ..downloader.retry import retry_request
from ..config import get_config


@dataclass
class Chapter:
    """Chapter information."""
    title: str
    url: str
    number: Optional[str] = None
    
    def __post_init__(self):
        """Extract chapter number from title."""
        if self.number is None:
            # Try to extract chapter number from title
            # e.g., "Chapter 1" -> "1", "Chapter 10.5" -> "10.5"
            import re
            match = re.search(r'Chapter\s*([\d.]+)', self.title, re.IGNORECASE)
            if match:
                self.number = match.group(1)
            else:
                self.number = self.title


@dataclass
class MangaInfo:
    """Complete manga information."""
    title: str
    url: str
    cover_url: Optional[str] = None
    description: Optional[str] = None
    manga_type: Optional[str] = None
    status: Optional[str] = None
    year: Optional[str] = None
    genres: list[str] = field(default_factory=list)
    chapters: list[Chapter] = field(default_factory=list)
    
    @property
    def chapters_count(self) -> int:
        """Get total number of chapters."""
        return len(self.chapters)
    
    @property
    def safe_title(self) -> str:
        """Get filesystem-safe title."""
        import re
        # Remove invalid characters for Windows filesystem
        safe = re.sub(r'[<>:"/\\|?*]', '', self.title)
        safe = safe.strip('. ')
        return safe if safe else "Untitled"


def scrape_manga(url: str) -> MangaInfo:
    """
    Scrape manga information from a Mangapill manga page.
    
    Args:
        url: Full URL to the manga page
        
    Returns:
        MangaInfo dataclass with all manga details
    """
    config = get_config()
    
    @retry_request(max_retries=config.retry_count, base_delay=config.retry_base_delay)
    def fetch_page(page_url: str) -> str:
        response = requests.get(page_url, headers=HEADERS, timeout=DEFAULT_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    
    html = fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    
    # ---------- Title ----------
    title_elem = soup.select_one("h1.font-bold")
    title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
    
    # ---------- Cover Image ----------
    cover_elem = soup.select_one("div.w-60 img")
    cover_url = None
    if cover_elem:
        cover_url = cover_elem.get("data-src") or cover_elem.get("src")
    
    # ---------- Description ----------
    desc_p = soup.select_one("p.text-sm.text--secondary")
    description = None
    
    if desc_p:
        html_content = desc_p.decode_contents()
        
        # Remove everything before actual synopsis (after promo)
        if "<br><br>" in html_content:
            html_content = html_content.split("<br><br>", 1)[1]
        
        clean_soup = BeautifulSoup(html_content, "html.parser")
        text = clean_soup.get_text("\n", strip=True)
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Keep only lines starting from the real story
        for i, line in enumerate(lines):
            if line.startswith("The "):
                lines = lines[i:]
                break
        
        description = "\n\n".join(lines) if lines else None
    
    # ---------- Info Grid (Type / Status / Year) ----------
    info = {}
    for block in soup.select("div.grid > div"):
        label = block.select_one("label")
        value = label.find_next_sibling("div") if label else None
        if label and value:
            info[label.get_text(strip=True)] = value.get_text(strip=True)
    
    # ---------- Genres ----------
    genres = [
        a.get_text(strip=True)
        for a in soup.select("a[href^='/search?genre=']")
    ]
    
    # ---------- Chapters ----------
    chapters = []
    for a in soup.select("#chapters a[href^='/chapters/']"):
        chapter_title = a.get_text(strip=True)
        chapter_url = urljoin(BASE_URL, a["href"])
        chapters.append(Chapter(title=chapter_title, url=chapter_url))
    
    return MangaInfo(
        title=title,
        url=url,
        cover_url=cover_url,
        description=description,
        manga_type=info.get("Type"),
        status=info.get("Status"),
        year=info.get("Year"),
        genres=genres,
        chapters=chapters,
    )


def validate_manga_url(url: str) -> bool:
    """
    Validate if a URL is a valid Mangapill manga URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^https?://(?:www\.)?mangapill\.com/manga/\d+/[\w-]+$'
    return bool(re.match(pattern, url))
