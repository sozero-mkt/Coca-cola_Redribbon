"""
Red Ribbon Restaurant Scraper - bluer.co.kr
Scrapes all Red Ribbon award restaurants and saves to CSV.

Usage:
    python red_ribbon_scraper.py
    python red_ribbon_scraper.py --output results.csv --delay 1.5
"""

import argparse
import logging
import time
import sys

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://www.bluer.co.kr"
SEARCH_PATH = "/search"
DEFAULT_PARAMS = {"ribbonType": "RED_RIBBON"}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

# ---------------------------------------------------------------------------
# NOTE: These selectors must be verified against the live site.
# Open DevTools (F12) on bluer.co.kr and inspect a restaurant card to find
# the actual class names, then update the constants below.
# ---------------------------------------------------------------------------

# Selector for each restaurant card/item in the list
RESTAURANT_ITEM_SEL = ".restaurant-item"

# Selectors within each card
NAME_SEL = ".name"
ADDRESS_SEL = ".address"
CATEGORY_SEL = ".category"      # optional – set to None to skip
PHONE_SEL = ".phone"            # optional – set to None to skip
DETAIL_LINK_SEL = "a"           # href to the detail page

# Pagination: selector for the "next page" link/button
NEXT_PAGE_SEL = "a.next, .pagination .next > a, [aria-label='다음']"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get(url: str, params: dict | None = None, retries: int = 3) -> requests.Response:
    """GET with retry logic and basic rate-limit handling."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 10))
                log.warning("Rate-limited. Waiting %ds before retry…", wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            log.warning("Attempt %d/%d failed for %s: %s", attempt, retries, url, exc)
            if attempt < retries:
                time.sleep(2 ** attempt)
    log.error("All retries exhausted for %s", url)
    sys.exit(1)


def _text(tag, selector: str | None) -> str:
    """Safely extract stripped text from a CSS selector within a tag."""
    if selector is None:
        return ""
    el = tag.select_one(selector)
    return el.get_text(strip=True) if el else ""


def _href(tag, selector: str) -> str:
    """Safely extract an href from a CSS selector within a tag."""
    el = tag.select_one(selector)
    if el and el.get("href"):
        href = el["href"]
        return href if href.startswith("http") else BASE_URL + href
    return ""


# ---------------------------------------------------------------------------
# Scraping logic
# ---------------------------------------------------------------------------

def parse_page(soup: BeautifulSoup) -> list[dict]:
    """Extract restaurant records from a single search-results page."""
    items = soup.select(RESTAURANT_ITEM_SEL)
    if not items:
        log.warning(
            "No elements matched selector '%s'. "
            "The site structure may have changed – update RESTAURANT_ITEM_SEL.",
            RESTAURANT_ITEM_SEL,
        )
    records = []
    for item in items:
        records.append(
            {
                "이름": _text(item, NAME_SEL),
                "주소": _text(item, ADDRESS_SEL),
                "카테고리": _text(item, CATEGORY_SEL),
                "전화번호": _text(item, PHONE_SEL),
                "상세 URL": _href(item, DETAIL_LINK_SEL),
            }
        )
    return records


def next_page_url(soup: BeautifulSoup) -> str | None:
    """Return the absolute URL of the next page, or None if on the last page."""
    el = soup.select_one(NEXT_PAGE_SEL)
    if el and el.get("href"):
        href = el["href"]
        return href if href.startswith("http") else BASE_URL + href
    return None


def scrape_all(delay: float = 1.0) -> list[dict]:
    """
    Iterate through all paginated search result pages and collect every
    Red Ribbon restaurant.

    Args:
        delay: Seconds to wait between page requests (be polite to the server).

    Returns:
        List of restaurant dicts.
    """
    url = BASE_URL + SEARCH_PATH
    params: dict | None = dict(DEFAULT_PARAMS)
    all_records: list[dict] = []
    page_num = 1

    while url:
        log.info("Fetching page %d: %s  params=%s", page_num, url, params)
        resp = _get(url, params=params)
        soup = BeautifulSoup(resp.text, "html.parser")

        records = parse_page(soup)
        log.info("  → %d restaurants found on page %d", len(records), page_num)
        all_records.extend(records)

        # After page 1 the params are encoded in the next-page URL itself.
        params = None
        url = next_page_url(soup)
        page_num += 1

        if url:
            time.sleep(delay)

    log.info("Total restaurants collected: %d", len(all_records))
    return all_records


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Red Ribbon restaurants from bluer.co.kr")
    parser.add_argument(
        "--output", default="red_ribbon_list.csv",
        help="Output CSV file path (default: red_ribbon_list.csv)",
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Seconds to wait between page requests (default: 1.0)",
    )
    args = parser.parse_args()

    records = scrape_all(delay=args.delay)

    if not records:
        log.error("No data collected. Check the selector constants at the top of the script.")
        sys.exit(1)

    df = pd.DataFrame(records)

    # Drop rows where the name is empty (malformed cards)
    df = df[df["이름"].str.strip() != ""]

    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    log.info("Data saved to %s  (%d rows)", args.output, len(df))
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
