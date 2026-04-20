#!/usr/bin/env python3
"""Fetch Hacker News top stories + Reddit front pages of curated subs.
Writes stories.json next to this script. Designed to be fast and dependency-free."""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = Path(__file__).resolve().parent
OUT = HERE / "stories.json"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) MorningEdition/1.0 (+https://github.com/henryblanchard/morning-edition)"

HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

# Subs chosen to match Henry's taste brief.
SUBS = [
    "MachineLearning",
    "LocalLLaMA",
    "artificial",
    "science",
    "Physics",
    "math",
    "programming",
    "webdev",
    "InternetIsBeautiful",
    "Futurology",
]


def _get_json(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_hn(limit: int = 30):
    ids = _get_json(HN_TOP)[:limit]
    results = [None] * len(ids)

    def _one(i, item_id):
        try:
            data = _get_json(HN_ITEM.format(id=item_id))
            if not data or data.get("type") != "story":
                return i, None
            return i, {
                "source": "hn",
                "id": str(item_id),
                "title": data.get("title", ""),
                "url": data.get("url") or f"https://news.ycombinator.com/item?id={item_id}",
                "comments_url": f"https://news.ycombinator.com/item?id={item_id}",
                "score": data.get("score", 0),
                "comments": data.get("descendants", 0),
                "by": data.get("by", ""),
                "text": (data.get("text") or "")[:1200],
            }
        except Exception as e:
            return i, {"error": str(e), "id": str(item_id), "source": "hn"}

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(_one, i, iid) for i, iid in enumerate(ids)]
        for f in as_completed(futures):
            i, val = f.result()
            results[i] = val

    return [r for r in results if r and "error" not in r]


def fetch_subreddit(sub: str, limit: int = 10):
    url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
    try:
        data = _get_json(url, timeout=15)
    except Exception as e:
        return [{"error": str(e), "source": f"reddit/{sub}"}]

    out = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {}) or {}
        if d.get("stickied") or d.get("pinned"):
            continue
        permalink = d.get("permalink", "")
        out.append({
            "source": f"reddit/{sub}",
            "id": d.get("id", ""),
            "title": d.get("title", ""),
            "url": d.get("url_overridden_by_dest") or f"https://reddit.com{permalink}",
            "comments_url": f"https://reddit.com{permalink}",
            "score": d.get("score", 0),
            "comments": d.get("num_comments", 0),
            "by": d.get("author", ""),
            "text": (d.get("selftext") or "")[:1200],
        })
    return out


def main():
    started = time.time()
    print("Fetching HN top 30...", flush=True)
    hn = fetch_hn(30)
    print(f"  got {len(hn)} HN stories", flush=True)

    reddit = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(fetch_subreddit, s, 10): s for s in SUBS}
        for f in as_completed(futures):
            sub = futures[f]
            try:
                items = f.result()
                reddit.extend([i for i in items if "error" not in i])
                print(f"  r/{sub}: {len(items)}", flush=True)
            except Exception as e:
                print(f"  r/{sub} FAILED: {e}", flush=True)

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "hn": hn,
        "reddit": reddit,
        "stats": {"hn": len(hn), "reddit": len(reddit), "took_seconds": round(time.time() - started, 1)},
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"\nWrote {OUT} ({len(hn)} HN + {len(reddit)} reddit in {payload['stats']['took_seconds']}s)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
