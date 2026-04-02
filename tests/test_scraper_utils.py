"""
Unit tests for scraper_utils.py retry and backoff logic.

Tests mock requests.Session.get and time.sleep to avoid real HTTP calls and delays.
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add scraper directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper'))

from scraper_utils import fetch_with_retry, get_scraper_for_domain, _session_cache


class MockConfig:
    """Mock config object for testing."""
    REQUEST_DELAY = 1


class TestSuccessfulResponse:
    """Test successful 200 response returns correctly on first attempt."""

    def test_200_response_returns_on_first_attempt(self):
        """Successful 200 response should return correctly on first attempt."""
        mock_response = Mock()
        mock_response.status_code = 200

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep'):
                response, error = fetch_with_retry('https://example.com', MockConfig())

            assert response is not None
            assert error is None
            assert response.status_code == 200
            mock_session.get.assert_called_once()


class TestRateLimitRetry:
    """Test 429 response triggers retry with actual delay."""

    def test_429_triggers_retry_with_sleep(self):
        """429 response should trigger retry and sleep should be called."""
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_200 = Mock()
        mock_response_200.status_code = 200

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.side_effect = [mock_response_429, mock_response_200]
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep') as mock_sleep:
                response, error = fetch_with_retry('https://example.com', MockConfig())

            assert response is not None
            assert error is None
            # Should be called twice: first attempt + retry
            assert mock_session.get.call_count == 2
            # Sleep should be called twice (once before each attempt)
            assert mock_sleep.call_count == 2


class TestServerErrorRetry:
    """Test 5xx response triggers retry."""

    @pytest.mark.parametrize("status_code", [500, 502, 503, 520, 525])
    def test_5xx_triggers_retry(self, status_code):
        """5xx response should trigger retry."""
        mock_response_5xx = Mock()
        mock_response_5xx.status_code = status_code
        mock_response_200 = Mock()
        mock_response_200.status_code = 200

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.side_effect = [mock_response_5xx, mock_response_200]
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep'):
                response, error = fetch_with_retry('https://example.com', MockConfig())

            assert response is not None
            assert error is None
            assert mock_session.get.call_count == 2


class TestClientErrorNoRetry:
    """Test 4xx (non-429) response returns error immediately without retry."""

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 422])
    def test_4xx_returns_error_immediately(self, status_code):
        """4xx (non-429) response should return error immediately without retry."""
        mock_response = Mock()
        mock_response.status_code = status_code

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.return_value = mock_response
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep'):
                response, error = fetch_with_retry('https://example.com', MockConfig())

            assert response is None
            assert error is not None
            assert f"HTTP {status_code}" in error
            # Should only be called once (no retries)
            mock_session.get.assert_called_once()


class TestExponentialBackoff:
    """Test exponential backoff increases delay on successive retries."""

    def test_exponential_backoff_increases_delay(self):
        """Sleep time should increase exponentially on successive retries."""
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_200 = Mock()
        mock_response_200.status_code = 200

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            # First 2 attempts fail with 429, 3rd succeeds
            # With max_retries=3, we get attempts 0, 1, 2 (3 total)
            mock_session.get.side_effect = [
                mock_response_429,
                mock_response_429,
                mock_response_200
            ]
            mock_get_session.return_value = mock_session

            # Track sleep times to verify exponential increase
            sleep_times = []

            with patch('scraper_utils.random.uniform', return_value=1.0):
                with patch('scraper_utils.time.sleep') as mock_sleep:
                    def capture_sleep(time):
                        sleep_times.append(time)

                    mock_sleep.side_effect = capture_sleep

                    response, error = fetch_with_retry('https://example.com', MockConfig())

            assert response is not None
            assert error is None
            assert len(sleep_times) == 3  # 3 attempts = 3 sleeps

            # With base_delay=1 and uniform=1.0:
            # attempt 0: 1 * 1 = 1
            # attempt 1: 1 * 2^1 * 1 = 2
            # attempt 2: 1 * 2^2 * 1 = 4
            assert sleep_times[0] == 1
            assert sleep_times[1] == 2
            assert sleep_times[2] == 4


class TestMaxRetriesExhausted:
    """Test max retries exhausted returns appropriate error message."""

    def test_max_retries_exhausted_429(self):
        """Max retries exhausted for 429 should return appropriate error message."""
        mock_response_429 = Mock()
        mock_response_429.status_code = 429

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.return_value = mock_response_429
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep'):
                response, error = fetch_with_retry('https://example.com', MockConfig(), max_retries=3)

            assert response is None
            assert error is not None
            assert "HTTP 429" in error
            assert "Rate limited" in error
            assert "REQUEST_DELAY" in error

    def test_max_retries_exhausted_5xx(self):
        """Max retries exhausted for 5xx should return appropriate error message."""
        mock_response_500 = Mock()
        mock_response_500.status_code = 500

        with patch('scraper_utils.get_scraper_for_domain') as mock_get_session:
            mock_session = Mock()
            mock_session.get.return_value = mock_response_500
            mock_get_session.return_value = mock_session

            with patch('scraper_utils.time.sleep'):
                response, error = fetch_with_retry('https://example.com', MockConfig(), max_retries=3)

            assert response is None
            assert error is not None
            assert "HTTP 500" in error
            assert "Server error" in error
            assert "3 retries" in error


class TestSessionCaching:
    """Test session caching behavior."""

    def test_same_session_for_same_domain(self):
        """Session caching should return the same session for the same domain."""
        # Clear the cache first
        _session_cache.clear()

        with patch('scraper_utils.requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session

            session1 = get_scraper_for_domain('example.com')
            session2 = get_scraper_for_domain('example.com')

            # Should only create one session
            mock_session_class.assert_called_once()
            # Should return the same session instance
            assert session1 is session2

    def test_different_sessions_for_different_domains(self):
        """Session caching should return different sessions for different domains."""
        # Clear the cache first
        _session_cache.clear()

        with patch('scraper_utils.requests.Session') as mock_session_class:
            # Return a new Mock instance each time Session() is called
            mock_session_class.side_effect = [Mock(), Mock()]

            session1 = get_scraper_for_domain('example.com')
            session2 = get_scraper_for_domain('other.com')

            # Should create two sessions
            assert mock_session_class.call_count == 2
            # Should return different session instances
            assert session1 is not session2
