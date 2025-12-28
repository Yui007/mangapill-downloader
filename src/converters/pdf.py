"""
PDF converter for Mangapill Downloader.
Converts chapter images to PDF format.
"""

import os
from pathlib import Path
from typing import Optional
import shutil

from rich.console import Console

console = Console()


def convert_to_pdf(
    image_folder: Path,
    output_path: Optional[Path] = None,
    keep_images: bool = True,
) -> Optional[Path]:
    """
    Convert images in a folder to a single PDF file.
    
    Args:
        image_folder: Path to folder containing images
        output_path: Optional custom output path (defaults to folder.pdf)
        keep_images: Whether to keep original images after conversion
        
    Returns:
        Path to the created PDF, or None if failed
    """
    try:
        import img2pdf
        from PIL import Image
    except ImportError:
        console.print("[red]✗ img2pdf and Pillow are required for PDF conversion[/red]")
        console.print("[yellow]  Install with: pip install img2pdf Pillow[/yellow]")
        return None
    
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
        output_path = image_folder.parent / f"{image_folder.name}.pdf"
    
    try:
        # Convert images to PDF-compatible format if needed
        processed_images = []
        temp_files = []
        
        for img_path in image_files:
            try:
                with Image.open(img_path) as img:
                    # Convert to RGB if necessary (PDF doesn't support RGBA well)
                    if img.mode in ("RGBA", "P"):
                        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                        
                        # Save as temp JPEG
                        temp_path = img_path.with_suffix(".temp.jpg")
                        rgb_img.save(temp_path, "JPEG", quality=95)
                        processed_images.append(str(temp_path))
                        temp_files.append(temp_path)
                    else:
                        processed_images.append(str(img_path))
            except Exception as e:
                console.print(f"[yellow]⚠ Skipping {img_path.name}: {e}[/yellow]")
        
        if not processed_images:
            console.print("[red]✗ No valid images to convert[/red]")
            return None
        
        # Create PDF
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(processed_images))
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                temp_file.unlink()
            except Exception:
                pass
        
        # Remove original images if requested
        if not keep_images:
            try:
                shutil.rmtree(image_folder)
            except Exception as e:
                console.print(f"[yellow]⚠ Could not remove images folder: {e}[/yellow]")
        
        return output_path
        
    except Exception as e:
        console.print(f"[red]✗ PDF conversion failed: {e}[/red]")
        return None


def batch_convert_to_pdf(
    folders: list[Path],
    keep_images: bool = True,
    progress_callback: Optional[callable] = None,
) -> list[Path]:
    """
    Convert multiple image folders to PDFs.
    
    Args:
        folders: List of folder paths
        keep_images: Whether to keep original images
        progress_callback: Optional callback(current, total) for progress
        
    Returns:
        List of created PDF paths
    """
    results = []
    
    for i, folder in enumerate(folders):
        pdf_path = convert_to_pdf(folder, keep_images=keep_images)
        if pdf_path:
            results.append(pdf_path)
        
        if progress_callback:
            progress_callback(i + 1, len(folders))
    
    return results
