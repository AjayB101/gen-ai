import requests
from bs4 import BeautifulSoup
from typing import Union
import urllib3
import ssl
import time
from urllib.parse import urlparse


def extract_page_details(url: str) -> str:
    """
    Extract text content from a web page URL using requests and BeautifulSoup.
    Handles SSL certificate issues and various website blocking mechanisms.

    Args:
        url (str): The URL to extract content from

    Returns:
        str: The extracted page content

    Raises:
        ValueError: If no content found at the URL
        Exception: If there's an error loading the page
    """
    # Disable SSL warnings (use with caution)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Enhanced headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

    # Create a session for better connection handling
    session = requests.Session()
    session.headers.update(headers)

    try:
        # Try multiple approaches in order of preference
        methods = [
            # Method 1: Standard request with SSL verification
            lambda: session.get(url, timeout=15, allow_redirects=True),

            # Method 2: Disable SSL verification (less secure but often works)
            lambda: session.get(
                url, timeout=15, verify=False, allow_redirects=True),

            # Method 3: Add delay and retry with different headers
            lambda: _retry_with_delay(session, url)
        ]

        response = None
        last_error = None

        for i, method in enumerate(methods, 1):
            try:
                print(f"Attempting method {i}...")
                response = method()
                response.raise_for_status()
                break
            except requests.exceptions.SSLError as e:
                last_error = e
                print(f"Method {i} failed with SSL error: {str(e)}")
                continue
            except requests.exceptions.RequestException as e:
                last_error = e
                print(f"Method {i} failed: {str(e)}")
                continue

        if response is None:
            raise Exception(
                f"All methods failed. Last error: {str(last_error)}")

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Try to find job-specific content first
        job_content = _extract_job_content(soup)
        if job_content:
            return job_content

        # Fallback to general text extraction
        text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        page_text = ' '.join(chunk for chunk in chunks if chunk)

        if not page_text.strip():
            raise ValueError(f"No readable content found at URL: {url}")

        return page_text

    except Exception as e:
        # Provide helpful error message
        domain = urlparse(url).netloc
        raise Exception(
            f"Error extracting content from {domain}: {str(e)}. Try copying the job description text manually.")


def _retry_with_delay(session, url):
    """Retry request with delay and modified headers"""
    time.sleep(2)  # Add delay
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session.get(url, timeout=20, verify=False, allow_redirects=True)


def _extract_job_content(soup):
    """Try to extract job-specific content using common selectors"""
    job_selectors = [
        # Common job description selectors
        '[data-automation-id="jobPostingDescription"]',
        '.job-description',
        '.job-content',
        '.job-details',
        '#job-description',
        '.posting-description',
        '[class*="job-desc"]',
        '[class*="description"]',
        'main',
        '.content'
    ]

    for selector in job_selectors:
        elements = soup.select(selector)
        if elements:
            # Get text from the first matching element
            text = elements[0].get_text(strip=True)
            if len(text) > 100:  # Only return if substantial content
                return text

    return None
