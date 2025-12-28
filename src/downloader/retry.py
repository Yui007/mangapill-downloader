"""
Retry decorator with exponential backoff for Mangapill Downloader.
Used for both chapter page fetching and image downloads.
"""

import time
import functools
from typing import Callable, TypeVar, Any
from rich.console import Console

console = Console()

T = TypeVar("T")


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""
    pass


def with_retry(
    max_retries: int = 3,
    base_delay: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
):
    """
    Decorator that retries a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (doubles each retry)
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Optional callback function(attempt, exception) called on each retry
    
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        
                        if on_retry:
                            on_retry(attempt + 1, e)
                        else:
                            console.print(
                                f"[yellow]⚠ Attempt {attempt + 1}/{max_retries + 1} failed: {e}[/yellow]"
                            )
                            console.print(
                                f"[yellow]  Retrying in {delay:.1f}s...[/yellow]"
                            )
                        
                        time.sleep(delay)
                    else:
                        console.print(
                            f"[red]✗ All {max_retries + 1} attempts failed[/red]"
                        )
            
            raise RetryError(
                f"Failed after {max_retries + 1} attempts. Last error: {last_exception}"
            ) from last_exception
        
        return wrapper
    return decorator


def retry_request(
    max_retries: int = 3,
    base_delay: float = 2.0,
):
    """
    Simplified retry decorator specifically for HTTP requests.
    Catches common request exceptions.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
    """
    import requests
    
    return with_retry(
        max_retries=max_retries,
        base_delay=base_delay,
        exceptions=(
            requests.RequestException,
            requests.Timeout,
            requests.ConnectionError,
            ConnectionError,
            TimeoutError,
        ),
    )
