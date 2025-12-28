"""
Constants for Mangapill Downloader.
Contains HTTP headers, default values, and app branding.
"""

# HTTP Headers for requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://mangapill.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Base URL
BASE_URL = "https://mangapill.com"

# Default configuration values
DEFAULT_OUTPUT_DIR = "./downloads"
DEFAULT_OUTPUT_FORMAT = "images"  # images, pdf, cbz
DEFAULT_KEEP_IMAGES = True
DEFAULT_MAX_CHAPTER_WORKERS = 3
DEFAULT_MAX_IMAGE_WORKERS = 5
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_BASE_DELAY = 2.0
DEFAULT_REQUEST_TIMEOUT = 30

# Output format options
OUTPUT_FORMATS = ["images", "pdf", "cbz"]

# App branding
APP_NAME = "Mangapill Downloader"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Rich console styles
STYLE_SUCCESS = "bold green"
STYLE_ERROR = "bold red"
STYLE_WARNING = "bold yellow"
STYLE_INFO = "bold cyan"
STYLE_TITLE = "bold magenta"

# Banner art
BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║   ███╗   ███╗ █████╗ ███╗   ██╗ ██████╗  █████╗ ██████╗ ██╗ ██      ██       ║
║   ████╗ ████║██╔══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗██║ ██      ██       ║
║   ██╔████╔██║███████║██╔██╗ ██║██║  ███╗███████║██████╔╝██║ ██      ██       ║
║   ██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██╔═══╝ ██║ ██      ██       ║
║   ██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║     ██║ ██████  ██████   ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝                  ║
║                   ██████╗  ██████╗ ██╗    ██╗███╗   ██╗                      ║
║                   ██╔══██╗██╔═══██╗██║    ██║████╗  ██║                      ║
║                   ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║                      ║
║                   ██║  ██║██║   ██║██║███╗██║██║╚██╗██║                      ║
║                   ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║                      ║
║                   ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝                      ║
║                    Version 1.0.0                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
