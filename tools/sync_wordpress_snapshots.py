#!/usr/bin/env python3
"""Refresh public Gamblee contract snapshots from live WordPress REST endpoints."""

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
USER_AGENT = "GambleeContractSnapshotSync/1.2 (+https://github.com/Gambleee/gamblee-article-contract)"
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


def preserve_authoring_guidance(relative_path: str, incoming):
    """Keep newer editorial/research instructions until the live Core exporter catches up.

    Only guidance fields are preserved. WordPress remains authoritative for schemas,
    vocabularies, item shapes, enums and all other importer-facing contract fields.
    """
    local_path = ROOT / relative_path
    if not local_path.exists() or not isinstance(incoming, dict):
        return incoming
    try:
        previous = json.loads(local_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return incoming
    if not isinstance(previous, dict):
        return incoming

    if relative_path == "authoring-contract.json":
        if "editorial_style" in previous and "editorial_style" not in incoming:
            incoming["editorial_style"] = previous["editorial_style"]
            incoming.setdefault("rules", {})["reader_facing_prose_is_direct_and_fact_led"] = True
            print("Retained Article editorial style guidance from GitHub snapshot.")
        return incoming

    key = "rules" if relative_path.startswith("bonuses/") else "principles"
    old_rules = previous.get(key, [])
    current_rules = incoming.get(key, [])
    if not isinstance(old_rules, list) or not isinstance(current_rules, list):
        return incoming
    prefixes = ["Research output gate BEFORE serialization:"]
    if relative_path.startswith("promotions/"):
        prefixes.append("Write the public-facing article directly and factually.")
    for prefix in prefixes:
        old = next((r for r in old_rules if isinstance(r, str) and r.startswith(prefix)), None)
        if old and not any(isinstance(r, str) and r.startswith(prefix) for r in current_rules):
            current_rules.append(old)
            print(f"Retained {relative_path} guidance: {prefix}")
    incoming[key] = current_rules

    if relative_path.startswith("promotions/"):
        old_sections = previous.get("editorial_content_requirements", {}).get("content_html", {}).get("minimum_structure", [])
        content = incoming.get("editorial_content_requirements", {}).get("content_html", {})
        target_sections = content.get("minimum_structure", [])
        if isinstance(old_sections, list) and isinstance(target_sections, list):
            prefix = "Use direct fact-led prose in content_html"
            old = next((r for r in old_sections if isinstance(r, str) and r.startswith(prefix)), None)
            if old and not any(isinstance(r, str) and r.startswith(prefix) for r in target_sections):
                target_sections.append(old)
                print("Retained Promotion editorial style guidance from GitHub snapshot.")
    return incoming


def sync_contract() -> None:
    payload = fetch_json("/wp-json/gamblee-core/v1/articles/authoring-contract")
    write_json("authoring-contract.json", preserve_authoring_guidance("authoring-contract.json", payload))


def sync_offer_contract(kind: str, relative_path: str) -> bool:
    endpoint = f"/wp-json/gamblee-core/v1/{kind}/authoring-contract"
    try:
        payload = fetch_json(endpoint)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(f"{kind.title()} contract endpoint not installed on the source site yet; retaining the last GitHub snapshot.")
            return False
        raise

    write_json(relative_path, preserve_authoring_guidance(relative_path, payload))
    return True


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
    sync_offer_contract("bonuses", "bonuses/authoring-contract.json")
    sync_offer_contract("promotions", "promotions/authoring-contract.json")
    sync_offer_contract("events", "events/authoring-contract.json")
    sync_vocabularies()
    sync_coverage()
    print("Gamblee contract snapshots refreshed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
