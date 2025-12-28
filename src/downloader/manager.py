"""
Download manager with threading support for Mangapill Downloader.
Handles concurrent chapter and image downloads.
"""

import os
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from typing import Callable, Optional
from dataclasses import dataclass

from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.console import Console

from ..constants import HEADERS, DEFAULT_REQUEST_TIMEOUT
from ..config import get_config, Config
from ..scrapers.manga import MangaInfo, Chapter
from ..scrapers.chapter import scrape_chapter_images
from .retry import retry_request

console = Console()


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    path: Optional[Path] = None
    error: Optional[str] = None
    images_count: int = 0


class DownloadManager:
    """
    Manages concurrent downloads of chapters and images.
    Uses ThreadPoolExecutor for parallel downloads.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the download manager.
        
        Args:
            config: Configuration object (loads from file if not provided)
        """
        self.config = config or get_config()
        self.output_dir = Path(self.config.output_dir)
    
    def download_image(
        self,
        url: str,
        save_path: Path,
        progress: Optional[Progress] = None,
        task_id: Optional[int] = None,
    ) -> bool:
        """
        Download a single image with retry logic.
        
        Args:
            url: Image URL
            save_path: Path to save the image
            progress: Optional Rich progress bar
            task_id: Optional task ID for progress update
            
        Returns:
            True if successful, False otherwise
        """
        @retry_request(
            max_retries=self.config.retry_count,
            base_delay=self.config.retry_base_delay
        )
        def fetch_image(image_url: str) -> bytes:
            response = requests.get(
                image_url,
                headers=HEADERS,
                timeout=DEFAULT_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.content
        
        try:
            content = fetch_image(url)
            
            # Ensure directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, "wb") as f:
                f.write(content)
            
            if progress and task_id is not None:
                progress.update(task_id, advance=1)
            
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to download image: {e}[/red]")
            return False
    
    def download_chapter_images(
        self,
        chapter: Chapter,
        manga_title: str,
        progress: Optional[Progress] = None,
    ) -> DownloadResult:
        """
        Download all images for a single chapter.
        
        Args:
            chapter: Chapter to download
            manga_title: Manga title for folder naming
            progress: Optional Rich progress bar
            
        Returns:
            DownloadResult with success status and path
        """
        try:
            # Scrape image URLs
            image_urls = scrape_chapter_images(chapter.url)
            
            if not image_urls:
                return DownloadResult(
                    success=False,
                    error="No images found in chapter"
                )
            
            # Create chapter folder
            safe_title = "".join(c for c in manga_title if c.isalnum() or c in (' ', '-', '_')).strip()
            chapter_folder = chapter.number or chapter.title
            chapter_folder = "".join(c for c in chapter_folder if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            
            chapter_path = self.output_dir / safe_title / f"Chapter {chapter_folder}"
            chapter_path.mkdir(parents=True, exist_ok=True)
            
            # Create progress task for images
            image_task = None
            if progress:
                image_task = progress.add_task(
                    f"[cyan]  ↳ {chapter.title}",
                    total=len(image_urls)
                )
            
            # Download images concurrently
            successful_downloads = 0
            
            with ThreadPoolExecutor(max_workers=self.config.max_image_workers) as executor:
                futures = {}
                
                for i, url in enumerate(image_urls, start=1):
                    ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
                    filename = f"{i:03d}{ext}"
                    save_path = chapter_path / filename
                    
                    future = executor.submit(
                        self.download_image,
                        url,
                        save_path,
                        progress,
                        image_task
                    )
                    futures[future] = filename
                
                for future in as_completed(futures):
                    try:
                        if future.result():
                            successful_downloads += 1
                    except Exception:
                        pass
            
            # Mark image task as complete
            if progress and image_task is not None:
                progress.update(image_task, visible=False)
            
            return DownloadResult(
                success=successful_downloads == len(image_urls),
                path=chapter_path,
                images_count=successful_downloads
            )
            
        except Exception as e:
            return DownloadResult(success=False, error=str(e))
    
    def download_chapters(
        self,
        manga: MangaInfo,
        chapters: list[Chapter],
        on_chapter_complete: Optional[Callable[[Chapter, DownloadResult], None]] = None,
    ) -> list[DownloadResult]:
        """
        Download multiple chapters concurrently.
        
        Args:
            manga: MangaInfo object
            chapters: List of chapters to download
            on_chapter_complete: Optional callback for each completed chapter
            
        Returns:
            List of DownloadResults
        """
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            
            main_task = progress.add_task(
                f"[bold green]Downloading {manga.safe_title}",
                total=len(chapters)
            )
            
            # Download chapters with limited concurrency
            with ThreadPoolExecutor(max_workers=self.config.max_chapter_workers) as executor:
                futures = {}
                
                for chapter in chapters:
                    future = executor.submit(
                        self.download_chapter_images,
                        chapter,
                        manga.safe_title,
                        progress
                    )
                    futures[future] = chapter
                
                for future in as_completed(futures):
                    chapter = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if on_chapter_complete:
                            on_chapter_complete(chapter, result)
                        
                    except Exception as e:
                        results.append(DownloadResult(success=False, error=str(e)))
                    
                    progress.update(main_task, advance=1)
        
        return results


def create_progress() -> Progress:
    """Create a Rich progress bar for downloads."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    )
