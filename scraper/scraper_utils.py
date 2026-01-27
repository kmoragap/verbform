import time
import random
import cloudscraper
from urllib.parse import urlparse


# Session cache to reuse cloudscraper sessions across requests
# This avoids solving Cloudflare challenges repeatedly
_session_cache = {}


def get_scraper_for_domain(domain):
    """
    Get or create a cloudscraper session for a specific domain.
    Sessions are cached to preserve cookies and avoid re-solving challenges.
    """
    if domain not in _session_cache:
        _session_cache[domain] = cloudscraper.create_scraper(
            browser='chrome',
            delay=10,  # Delay for Cloudflare challenge solving (first request only)
        )
    return _session_cache[domain]


def fetch_with_retry(url, headers, config, max_retries=3, base_delay=2):
    """
    Fetch URL with rate limiting and Cloudflare bypass using cloudscraper.

    Args:
        url: The URL to fetch
        headers: HTTP headers for the request
        config: Configuration object with REQUEST_DELAY attribute
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay in seconds (default: 2)

    Returns:
        Tuple of (response, error_message):
        - On success: (response, None)
        - On failure: (None, error_message)
    """
    delay = getattr(config, 'REQUEST_DELAY', base_delay)

    # Extract domain for session caching
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Get or create a cached session for this domain
    scraper = get_scraper_for_domain(domain)

    for attempt in range(max_retries):
        try:
            # Add random jitter to delay for more human-like behavior
            jitter = random.uniform(0.8, 1.2)
            sleep_time = delay * jitter

            if attempt > 0:
                sleep_time = delay * (2 ** attempt) * jitter
                print(f"Rate limited. Waiting {sleep_time:.1f}s before retry...")
            else:
                time.sleep(sleep_time)

            response = scraper.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response, None

            if response.status_code == 429:
                if attempt < max_retries - 1:
                    continue
                else:
                    return None, (
                        f"HTTP 429: Rate limited. Try increasing REQUEST_DELAY in config.py "
                        f"or wait a while before trying again."
                    )

            return None, f"HTTP {response.status_code}: Could not access page"

        except Exception as e:
            if attempt < max_retries - 1:
                continue
            return None, f"Request error: {str(e)}"

    return None, "Max retries exceeded"
