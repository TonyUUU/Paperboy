from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import socket

import feedparser
import requests
from langchain_core.tools import tool

_TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "gclid",
    "fbclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
}


@tool("fetch_rss")
def fetch_rss(feed_urls: List[str], max_items_per_feed: int = 10, timeout_s: int = 15) -> List[Dict[str, Any]]:
    """
    Fetch and parse RSS/Atom feeds.

    Args:
      feed_urls: list of RSS/Atom feed URLs
      max_items_per_feed: max entries to return per feed
      timeout_s: HTTP timeout seconds

    Returns:
      List of items with keys: title, url, published, source, summary
    """
    socket.setdefaulttimeout(timeout_s)

    headers = {
        # TODO: Replace with actual contact email
        "User-Agent": "paperboy-rss-fetcher/0.1 (+https://example.invalid)"
    }

    all_items: List[Dict[str, Any]] = []

    for feed_url in feed_urls:
        try:
            resp = requests.get(feed_url, headers=headers, timeout=timeout_s)
            resp.raise_for_status()
            parsed = feedparser.parse(resp.content)

            try:
                feed_title = parsed.feed.get("title")
            except Exception:
                feed_title = None

            for entry in (parsed.entries or [])[: max_items_per_feed]:
                title = _safe_get(entry, "title") or ""
                link = _safe_get(entry, "link", "id") or ""
                link = _strip_tracking(link)

                published = (
                    _safe_get(entry, "published", "updated")
                    or _safe_get(entry, "publishedDate", "date")
                )

                summary = _safe_get(entry, "summary", "description") or ""

                all_items.append(
                    {
                        "title": title.strip(),
                        "url": link.strip(),
                        "published": published,
                        "source": feed_title or feed_url,
                        "summary": summary.strip(),
                    }
                )
        except Exception as e:
            # Don’t hard-fail the whole tool on one broken feed; include an error item if you want.
            all_items.append(
                {
                    "title": "",
                    "url": "",
                    "published": None,
                    "source": feed_url,
                    "summary": f"[feed error] {type(e).__name__}: {e}",
                }
            )

    # light cleanup: drop empty URL items
    all_items = [it for it in all_items if it.get("url")]

    return all_items

def _strip_tracking(url: str) -> str:
    """Remove common tracking query params and fragments."""
    try:
        parts = urlsplit(url)
        qs = parse_qsl(parts.query, keep_blank_values=True)
        filtered = [(k, v) for (k, v) in qs if k.lower() not in _TRACKING_PARAMS]
        new_query = urlencode(filtered, doseq=True)
        # keep path, remove fragment
        return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, ""))
    except Exception:
        return url


def _safe_get(entry: Any, *keys: str) -> Optional[str]:
    for k in keys:
        v = entry.get(k) if isinstance(entry, dict) else getattr(entry, k, None)
        if v:
            return str(v)
    return None
