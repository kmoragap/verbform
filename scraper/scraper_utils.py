import time
import random
import requests
from urllib.parse import urlparse


# Session cache to reuse requests sessions across requests
# This preserves cookies and TCP connections for better performance
_session_cache = {}


def get_scraper_for_domain(domain):
    """
    Get or create a requests Session for a specific domain.
    Sessions are cached to preserve cookies and TCP connections.
    """
    if domain not in _session_cache:
        _session_cache[domain] = requests.Session()
    return _session_cache[domain]


def fetch_with_retry(url, config, max_retries=3):
    """
    Fetch URL with rate limiting and retry logic using requests.Session.

    Args:
        url: The URL to fetch
        config: Configuration object with REQUEST_DELAY attribute
        max_retries: Maximum number of retry attempts (default: 3)

    Returns:
        Tuple of (response, error_message):
        - On success: (response, None)
        - On failure: (None, error_message)
    """
    delay = getattr(config, 'REQUEST_DELAY', 1)

    # Extract domain for session caching
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Get or create a cached session for this domain
    session = get_scraper_for_domain(domain)

    for attempt in range(max_retries):
        try:
            # Add random jitter to delay for more human-like behavior
            jitter = random.uniform(0.8, 1.2)
            sleep_time = delay * jitter

            # Apply exponential backoff on retries
            if attempt > 0:
                sleep_time = delay * (2 ** attempt) * jitter
                print(f"Rate limited. Waiting {sleep_time:.1f}s before retry...")

            # Sleep before every request (including retries)
            time.sleep(sleep_time)

            response = session.get(url, timeout=10)

            if response.status_code == 200:
                return response, None

            # Retry on rate limit (429) and server errors (500-525)
            if response.status_code == 429 or 500 <= response.status_code <= 525:
                if attempt < max_retries - 1:
                    continue
                else:
                    if response.status_code == 429:
                        return None, (
                            f"HTTP 429: Rate limited. Try increasing REQUEST_DELAY in config.py "
                            f"or wait a while before trying again."
                        )
                    else:
                        return None, (
                            f"HTTP {response.status_code}: Server error after {max_retries} retries. "
                            f"Please try again later."
                        )

            # Client errors (4xx except 429) are not retried
            return None, f"HTTP {response.status_code}: Could not access page"

        except Exception as e:
            if attempt < max_retries - 1:
                continue
            return None, f"Request error: {str(e)}"

    return None, "Max retries exceeded"
