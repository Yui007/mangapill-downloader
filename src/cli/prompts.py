"""
Interactive prompts for Mangapill Downloader CLI.
Uses Rich for beautiful input prompts.
"""

import re
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich import box

from ..constants import OUTPUT_FORMATS
from ..scrapers.manga import Chapter, validate_manga_url
from ..config import Config, save_config

console = Console()


def prompt_manga_url() -> str:
    """
    Prompt user for a Mangapill manga URL.
    
    Returns:
        Valid manga URL
    """
    while True:
        console.print()
        url = Prompt.ask(
            "[bold cyan]🔗 Enter Mangapill manga URL[/bold cyan]",
            default="",
        )
        
        if not url:
            console.print("[yellow]⚠ URL cannot be empty[/yellow]")
            continue
        
        # Validate URL format
        if validate_manga_url(url):
            return url
        
        # Try to fix common issues
        if "mangapill.com/manga/" in url:
            console.print("[yellow]⚠ URL format seems off, but will try anyway[/yellow]")
            return url
        
        console.print("[red]✗ Invalid Mangapill URL format[/red]")
        console.print("[dim]  Expected: https://mangapill.com/manga/ID/manga-name[/dim]")


def prompt_chapter_selection(chapters: list[Chapter]) -> list[Chapter]:
    """
    Prompt user to select chapters for download.
    
    Args:
        chapters: List of all available chapters
        
    Returns:
        List of selected Chapter objects
    """
    console.print()
    console.print(Panel(
        "[bold]Chapter Selection Options:[/bold]\n\n"
        "  • [cyan]all[/cyan]     - Download all chapters\n"
        "  • [cyan]5[/cyan]       - Download chapter 5 only\n"
        "  • [cyan]1-10[/cyan]    - Download chapters 1 through 10\n"
        "  • [cyan]1,3,5-7[/cyan] - Download chapters 1, 3, 5, 6, and 7",
        title="[bold magenta]📖 How to Select[/bold magenta]",
        border_style="magenta",
        box=box.ROUNDED,
    ))
    
    while True:
        selection = Prompt.ask(
            "\n[bold cyan]📑 Select chapters[/bold cyan]",
            default="all",
        ).strip().lower()
        
        if selection == "all":
            return chapters
        
        try:
            selected_indices = parse_chapter_selection(selection, len(chapters))
            if not selected_indices:
                console.print("[yellow]⚠ No chapters selected, try again[/yellow]")
                continue
            
            selected = [chapters[i] for i in selected_indices]
            
            # Show confirmation
            if len(selected) == 1:
                console.print(f"[green]✓ Selected: {selected[0].title}[/green]")
            else:
                console.print(f"[green]✓ Selected {len(selected)} chapters[/green]")
            
            return selected
            
        except ValueError as e:
            console.print(f"[red]✗ Invalid selection: {e}[/red]")
            continue


def parse_chapter_selection(selection: str, total: int) -> list[int]:
    """
    Parse chapter selection string into list of indices.
    
    Args:
        selection: User input string (e.g., "1,3,5-7")
        total: Total number of chapters
        
    Returns:
        List of 0-based chapter indices
    """
    indices = set()
    
    # Split by comma
    parts = selection.split(",")
    
    for part in parts:
        part = part.strip()
        
        if "-" in part:
            # Range (e.g., "1-10")
            match = re.match(r"(\d+)\s*-\s*(\d+)", part)
            if not match:
                raise ValueError(f"Invalid range: {part}")
            
            start = int(match.group(1))
            end = int(match.group(2))
            
            if start < 1 or end > total:
                raise ValueError(f"Range {start}-{end} out of bounds (1-{total})")
            if start > end:
                raise ValueError(f"Invalid range: {start} > {end}")
            
            indices.update(range(start - 1, end))
        else:
            # Single chapter
            try:
                num = int(part)
                if num < 1 or num > total:
                    raise ValueError(f"Chapter {num} out of bounds (1-{total})")
                indices.add(num - 1)
            except ValueError:
                raise ValueError(f"Invalid chapter number: {part}")
    
    return sorted(indices)


def prompt_output_format() -> str:
    """
    Prompt user to select output format.
    
    Returns:
        Selected format string ('images', 'pdf', 'cbz')
    """
    console.print()
    console.print("[bold cyan]📄 Select output format:[/bold cyan]")
    console.print("  [1] 🖼️  Images (raw image files)")
    console.print("  [2] 📕 PDF (single PDF per chapter)")
    console.print("  [3] 📦 CBZ (comic book archive with metadata)")
    
    while True:
        choice = Prompt.ask(
            "\n[bold cyan]Enter choice[/bold cyan]",
            choices=["1", "2", "3", "images", "pdf", "cbz"],
            default="1",
        ).strip().lower()
        
        format_map = {
            "1": "images",
            "2": "pdf",
            "3": "cbz",
            "images": "images",
            "pdf": "pdf",
            "cbz": "cbz",
        }
        
        selected = format_map.get(choice, "images")
        console.print(f"[green]✓ Format: {selected.upper()}[/green]")
        return selected


def prompt_keep_images() -> bool:
    """
    Prompt whether to keep images after conversion.
    
    Returns:
        True to keep images, False to delete
    """
    return Confirm.ask(
        "\n[bold cyan]🖼️  Keep original images after conversion?[/bold cyan]",
        default=True,
    )


def prompt_settings_menu(config: Config) -> Config:
    """
    Interactive settings menu to modify configuration.
    
    Args:
        config: Current configuration
        
    Returns:
        Modified configuration
    """
    while True:
        console.print()
        console.print("[bold magenta]⚙️  Settings Menu[/bold magenta]")
        console.print("  [1] 📁 Output directory")
        console.print("  [2] 📄 Default output format")
        console.print("  [3] 🖼️  Keep images after conversion")
        console.print("  [4] 📚 Max chapter workers")
        console.print("  [5] 🖼️  Max image workers")
        console.print("  [6] 🔄 Retry count")
        console.print("  [7] ⏱️  Retry base delay")
        console.print("  [0] 💾 Save and exit")
        
        choice = Prompt.ask(
            "\n[bold cyan]Select option[/bold cyan]",
            choices=["0", "1", "2", "3", "4", "5", "6", "7"],
            default="0",
        )
        
        if choice == "0":
            if save_config(config):
                console.print("[green]✓ Settings saved![/green]")
            else:
                console.print("[red]✗ Failed to save settings[/red]")
            break
        
        elif choice == "1":
            config.output_dir = Prompt.ask(
                "📁 Output directory",
                default=config.output_dir,
            )
        
        elif choice == "2":
            config.output_format = prompt_output_format()
        
        elif choice == "3":
            config.keep_images = Confirm.ask(
                "🖼️  Keep images after conversion?",
                default=config.keep_images,
            )
        
        elif choice == "4":
            config.max_chapter_workers = IntPrompt.ask(
                "📚 Max chapter workers (1-10)",
                default=config.max_chapter_workers,
            )
            config.max_chapter_workers = max(1, min(10, config.max_chapter_workers))
        
        elif choice == "5":
            config.max_image_workers = IntPrompt.ask(
                "🖼️  Max image workers (1-20)",
                default=config.max_image_workers,
            )
            config.max_image_workers = max(1, min(20, config.max_image_workers))
        
        elif choice == "6":
            config.retry_count = IntPrompt.ask(
                "🔄 Retry count (1-10)",
                default=config.retry_count,
            )
            config.retry_count = max(1, min(10, config.retry_count))
        
        elif choice == "7":
            delay = Prompt.ask(
                "⏱️  Retry base delay (seconds)",
                default=str(config.retry_base_delay),
            )
            try:
                config.retry_base_delay = float(delay)
            except ValueError:
                console.print("[yellow]⚠ Invalid delay, keeping current value[/yellow]")
    
    return config
