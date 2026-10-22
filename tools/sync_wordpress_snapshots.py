#!/usr/bin/env python3
"""Refresh the public Gamblee Article snapshots from live WordPress REST endpoints."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE = os.environ.get("GAMBLEE_SOURCE_URL", "https://www.gamblee.com").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "GambleeArticleSnapshotSync/1.0 (+https://github.com/Gambleee/gamblee-article-contract)"
TIMEOUT = 30


def fetch_json(path: str, params: dict[str, object] | None = None):
    url = SOURCE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return json.load(response)


def write_json(relative_path: str, payload) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_contract() -> None:
    payload = fetch_json("/wp-json/gamblee-core/v1/articles/authoring-contract")
    write_json("authoring-contract.json", payload)


def sync_vocabularies() -> None:
    index = fetch_json("/wp-json/gamblee-core/v1/articles/vocabulary")
    write_json("vocabulary/index.json", index)

    dimensions = index.get("dimensions", []) if isinstance(index, dict) else []
    for row in dimensions:
        dimension = row.get("dimension") if isinstance(row, dict) else None
        if not isinstance(dimension, str) or not dimension:
            raise RuntimeError("Vocabulary index contains an invalid dimension.")

        endpoint = f"/wp-json/gamblee-core/v1/articles/vocabulary/{urllib.parse.quote(dimension)}"
        first = fetch_json(endpoint, {"page": 1, "per_page": 200})
        pages = int(first.get("total_pages", 1) or 1)
        total = int(first.get("total", 0) or 0)
        items = list(first.get("items", []))

        for page in range(2, pages + 1):
            payload = fetch_json(endpoint, {"page": page, "per_page": 200})
            items.extend(payload.get("items", []))

        if len(items) != total:
            raise RuntimeError(f"Vocabulary {dimension}: expected {total} items, fetched {len(items)}.")

        write_json(
            f"vocabulary/{dimension}.json",
            {
                "contract": "gamblee-article-vocabulary-snapshot",
                "schema_version": first.get("schema_version"),
                "dimension": dimension,
                "total": total,
                "source": SOURCE + endpoint,
                "items": items,
            },
        )


def sync_coverage() -> bool:
    endpoint = "/wp-json/gamblee-core/v1/articles/coverage-index"
    try:
        first = fetch_json(endpoint, {"page": 1, "per_page": 200})
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print("Coverage endpoint not installed yet; leaving coverage-index.json unchanged.")
            return False
        raise

    pages = int(first.get("pages", 1) or 1)
    total = int(first.get("total", 0) or 0)
    articles = list(first.get("items", []))
    for page in range(2, pages + 1):
        payload = fetch_json(endpoint, {"page": page, "per_page": 200})
        articles.extend(payload.get("items", []))

    if len(articles) != total:
        raise RuntimeError(f"Coverage index: expected {total} articles, fetched {len(articles)}.")

    write_json(
        "coverage-index.json",
        {
            "contract": first.get("contract", "gamblee-article-coverage-index"),
            "schema_version": first.get("schema_version", 1),
            "source": SOURCE + endpoint,
            "total": total,
            "articles": articles,
        },
    )
    return True


def main() -> int:
    sync_contract()
    sync_vocabularies()
    sync_coverage()
    print("Gamblee Article snapshots refreshed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
