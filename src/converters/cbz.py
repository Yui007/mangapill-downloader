"""
CBZ (Comic Book ZIP) converter for Mangapill Downloader.
Creates CBZ archives with ComicInfo.xml metadata.
"""

import zipfile
import shutil
from pathlib import Path
from typing import Optional

from rich.console import Console

from .comicinfo import generate_comicinfo_xml
from ..scrapers.manga import MangaInfo, Chapter

console = Console()


def convert_to_cbz(
    image_folder: Path,
    output_path: Optional[Path] = None,
    manga: Optional[MangaInfo] = None,
    chapter: Optional[Chapter] = None,
    keep_images: bool = True,
) -> Optional[Path]:
    """
    Convert images in a folder to a CBZ (Comic Book ZIP) file.
    
    Args:
        image_folder: Path to folder containing images
        output_path: Optional custom output path (defaults to folder.cbz)
        manga: Optional MangaInfo for ComicInfo.xml
        chapter: Optional Chapter for ComicInfo.xml
        keep_images: Whether to keep original images after conversion
        
    Returns:
        Path to the created CBZ, or None if failed
    """
    if not image_folder.exists() or not image_folder.is_dir():
        console.print(f"[red]✗ Image folder not found: {image_folder}[/red]")
        return None
    
    # Get all image files sorted by name
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
    image_files = sorted([
        f for f in image_folder.iterdir()
        if f.suffix.lower() in image_extensions
    ])
    
    if not image_files:
        console.print(f"[red]✗ No images found in {image_folder}[/red]")
        return None
    
    # Set output path
    if output_path is None:
        output_path = image_folder.parent / f"{image_folder.name}.cbz"
    
    try:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as cbz:
            # Add ComicInfo.xml if manga info is provided
            if manga:
                comicinfo_xml = generate_comicinfo_xml(
                    manga=manga,
                    chapter=chapter,
                    page_count=len(image_files)
                )
                cbz.writestr("ComicInfo.xml", comicinfo_xml)
            
            # Add all images
            for img_file in image_files:
                cbz.write(img_file, img_file.name)
        
        # Remove original images if requested
        if not keep_images:
            try:
                shutil.rmtree(image_folder)
            except Exception as e:
                console.print(f"[yellow]⚠ Could not remove images folder: {e}[/yellow]")
        
        return output_path
        
    except Exception as e:
        console.print(f"[red]✗ CBZ conversion failed: {e}[/red]")
        return None


def batch_convert_to_cbz(
    folders: list[Path],
    manga: Optional[MangaInfo] = None,
    chapters: Optional[list[Chapter]] = None,
    keep_images: bool = True,
    progress_callback: Optional[callable] = None,
) -> list[Path]:
    """
    Convert multiple image folders to CBZ files.
    
    Args:
        folders: List of folder paths
        manga: Optional MangaInfo for metadata
        chapters: Optional list of Chapter objects (matched by index)
        keep_images: Whether to keep original images
        progress_callback: Optional callback(current, total) for progress
        
    Returns:
        List of created CBZ paths
    """
    results = []
    
    for i, folder in enumerate(folders):
        chapter = chapters[i] if chapters and i < len(chapters) else None
        cbz_path = convert_to_cbz(
            folder,
            manga=manga,
            chapter=chapter,
            keep_images=keep_images
        )
        if cbz_path:
            results.append(cbz_path)
        
        if progress_callback:
            progress_callback(i + 1, len(folders))
    
    return results
