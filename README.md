# Gamblee Article authoring contract

Public, read-only snapshot for external AI assistants preparing Gamblee Article ZIP packages. **No WordPress login or WPVibe connection is needed to read this repository.**

## Start here

1. [Authoring contract](authoring-contract.json) — the authoritative Article JSON schema (v1.1), import rules, example, packaging instructions, and lookup guidance.
2. [Vocabulary index](vocabulary/index.json) — available dimensions and counts.
3. Open the required canonical vocabulary file(s):
   - [Verticals](vocabulary/verticals.json)
   - [Geographies](vocabulary/geographies.json)
   - [Topics](vocabulary/topics.json)
   - [Subjects](vocabulary/subjects.json)
   - [Entities](vocabulary/entities.json)
   - [Channels](vocabulary/channels.json)
   - [Editorial types](vocabulary/editorial_types.json)

## For the News Sweeper

- Retrieve `authoring-contract.json` and the relevant canonical vocabularies from this **public GitHub repository**, not from Gamblee's WordPress REST URLs.
- Use exact canonical `slug` values. Never invent classifications or extra fields.
- For brand/entity lookups, search within [entities.json](vocabulary/entities.json) for the name and use the matching slug (e.g. `brand-betway`); check ambiguity before choosing.
- Generate one `article.json` compliant with the `schema` object in the authoring contract.
- Package `article.json` at the ZIP root with no more than one optional local featured image. Use the contract's supported image instructions.
- The existing authenticated Gamblee WordPress importer validates the ZIP and creates **drafts only**. Reading this repository cannot publish or modify the website.

## Source and freshness

Snapshot obtained from the **staging** Article REST endpoints on 2026-10-12, Gamblee Core **1.83.02**, Article schema **1.1**. Live WordPress remains the source of truth. This repository is **not automatically synchronized**; vocabulary terms and schema may change after this snapshot.

WordPress source routes:
- `/wp-json/gamblee-core/v1/articles/authoring-contract`
- `/wp-json/gamblee-core/v1/articles/vocabulary`
- `/wp-json/gamblee-core/v1/articles/vocabulary/{dimension}`

If the importer rejects a slug or field, stop and refresh the snapshot from the current WordPress endpoints. Do not bypass importer validation.

## Security and performance

Only public authoring metadata and canonical term names/slugs are mirrored. No importer, private content, credentials or write API is mirrored. GitHub serves these static files without triggering WordPress queries, cache purges or registry jobs.
