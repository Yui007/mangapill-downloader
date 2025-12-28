"""
Rich display components for Mangapill Downloader CLI.
Handles banners, panels, tables, and progress bars.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
from typing import Optional

from ..constants import BANNER, APP_NAME, APP_VERSION, STYLE_TITLE
from ..scrapers.manga import MangaInfo, Chapter
from ..config import Config

console = Console()


def show_banner():
    """Display the application banner."""
    console.print(BANNER, style="bold cyan")


def show_manga_info(manga: MangaInfo):
    """
    Display manga information in a beautiful Rich panel.
    
    Args:
        manga: MangaInfo object to display
    """
    # Create info table
    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Label", style="bold cyan")
    info_table.add_column("Value", style="white")
    
    info_table.add_row("📖 Title", manga.title)
    if manga.manga_type:
        info_table.add_row("📘 Type", manga.manga_type)
    if manga.status:
        status_style = "green" if manga.status.lower() == "completed" else "yellow"
        info_table.add_row("📊 Status", f"[{status_style}]{manga.status}[/{status_style}]")
    if manga.year:
        info_table.add_row("📅 Year", manga.year)
    if manga.genres:
        info_table.add_row("🏷️  Genres", ", ".join(manga.genres[:5]))
    info_table.add_row("📚 Chapters", str(manga.chapters_count))
    
    # Create panel
    panel = Panel(
        info_table,
        title="[bold magenta]📚 Manga Information[/bold magenta]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    
    console.print(panel)
    
    # Show description if available
    if manga.description:
        desc_text = manga.description[:300] + "..." if len(manga.description) > 300 else manga.description
        desc_panel = Panel(
            Text(desc_text, style="italic"),
            title="[bold cyan]📝 Description[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
        console.print(desc_panel)


def show_chapters_table(chapters: list[Chapter], show_all: bool = False):
    """
    Display chapters in a formatted table.
    
    Args:
        chapters: List of Chapter objects
        show_all: If False, show only first and last 5 chapters
    """
    table = Table(
        title="[bold green]📑 Chapters[/bold green]",
        box=box.ROUNDED,
        border_style="green",
        header_style="bold white",
        show_lines=False,
    )
    
    table.add_column("#", justify="right", style="dim", width=6)
    table.add_column("Chapter", style="cyan", min_width=30)
    
    if show_all or len(chapters) <= 15:
        # Show all chapters
        for i, chapter in enumerate(chapters, 1):
            table.add_row(str(i), chapter.title)
    else:
        # Show first 5 and last 5
        for i, chapter in enumerate(chapters[:5], 1):
            table.add_row(str(i), chapter.title)
        
        table.add_row("...", f"[dim]... {len(chapters) - 10} more chapters ...[/dim]")
        
        for i, chapter in enumerate(chapters[-5:], len(chapters) - 4):
            table.add_row(str(i), chapter.title)
    
    console.print(table)


def show_settings(config: Config):
    """
    Display current settings in a panel.
    
    Args:
        config: Current configuration
    """
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Setting", style="bold cyan")
    table.add_column("Value", style="white")
    
    table.add_row("📁 Output Directory", config.output_dir)
    table.add_row("📄 Output Format", config.output_format.upper())
    table.add_row("🖼️  Keep Images", "Yes" if config.keep_images else "No")
    table.add_row("📚 Chapter Workers", str(config.max_chapter_workers))
    table.add_row("🖼️  Image Workers", str(config.max_image_workers))
    table.add_row("🔄 Retry Count", str(config.retry_count))
    table.add_row("⏱️  Retry Delay", f"{config.retry_base_delay}s")
    
    panel = Panel(
        table,
        title="[bold magenta]⚙️  Current Settings[/bold magenta]",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    
    console.print(panel)


def show_success(message: str):
    """Display a success message."""
    console.print(f"[bold green]✓ {message}[/bold green]")


def show_error(message: str):
    """Display an error message."""
    console.print(f"[bold red]✗ {message}[/bold red]")


def show_warning(message: str):
    """Display a warning message."""
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def show_info(message: str):
    """Display an info message."""
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")


def show_download_summary(successful: int, failed: int, output_dir: str):
    """
    Display download summary.
    
    Args:
        successful: Number of successful downloads
        failed: Number of failed downloads
        output_dir: Output directory path
    """
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Stat", style="bold")
    table.add_column("Value")
    
    table.add_row("[green]✓ Successful[/green]", str(successful))
    if failed > 0:
        table.add_row("[red]✗ Failed[/red]", str(failed))
    table.add_row("[cyan]📁 Location[/cyan]", output_dir)
    
    panel = Panel(
        table,
        title="[bold green]📊 Download Summary[/bold green]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    
    console.print(panel)
