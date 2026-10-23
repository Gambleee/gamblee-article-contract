# Gamblee Article authoring contract

Public, read-only snapshots for external AI assistants preparing Gamblee Article ZIP packages and checking existing Gamblee news coverage. **No WordPress login or WPVibe connection is needed to read this repository.**

## Start here

1. [Authoring contract](authoring-contract.json) — the authoritative Article JSON schema (v1.1), import rules, example, packaging instructions, and lookup guidance.
2. [Editorial guidelines](editorial-guidelines.md) — **required for every article**: natural internal links, restrained featured images, factual prose, and pre-delivery quality checks.
3. [Coverage index](coverage-index.json) — published Gamblee Articles for duplicate-story detection, meaningful-update checks, and internal-link discovery. The file is created after the first successful sync against a Core version exposing the coverage endpoint.
4. [Vocabulary index](vocabulary/index.json) — available dimensions and counts.
5. Open the required canonical vocabulary file(s):
   - [Verticals](vocabulary/verticals.json)
   - [Geographies](vocabulary/geographies.json)
   - [Topics](vocabulary/topics.json)
   - [Subjects](vocabulary/subjects.json)
   - [Entities](vocabulary/entities.json)
   - [Channels](vocabulary/channels.json)
   - [Editorial types](vocabulary/editorial_types.json)

## For the News Sweeper

- Retrieve `authoring-contract.json`, **`editorial-guidelines.md`**, `coverage-index.json`, and the relevant canonical vocabularies from this **public GitHub repository**, not through WPVibe. Read editorial guidelines before drafting any Article.
- Before recommending a story, compare the underlying event/development against `coverage-index.json`; do not rely on headline wording alone.
- Treat candidates as `New`, `Already Covered`, or `Meaningful Update`. A repeated report of the same underlying event is not a new story.
- Use matching existing Article URLs from the coverage index as internal-link candidates when writing a genuine update or closely related story. **Bury links naturally inside relevant sentences; no artificial introductions, forced link count, or link announcements.** Follow `editorial-guidelines.md` for full rules.
- The public coverage index contains **published Articles only**. Draft titles/excerpts are deliberately not mirrored to this public repository.
- Use exact canonical vocabulary `slug` values. Never invent classifications or extra fields.
- For brand/entity lookups, search within [entities.json](vocabulary/entities.json) for the name and use the matching slug (for example `brand-betway`); check ambiguity before choosing.
- Generate one `article.json` compliant with the `schema` object in the authoring contract.
- Package `article.json` at the ZIP root with no more than one optional local featured image. Use the contract's supported image instructions. **Prefer appropriately licensed real photographs; when generating, use restrained, minimal single-subject images—no collages, fake screenshots or fabricated branding.**
- The existing authenticated Gamblee WordPress importer validates the ZIP and creates **drafts only**. Reading this repository cannot publish or modify the website.

## Source and freshness

Live WordPress is the source of truth. GitHub stores static public snapshots so external assistants can read current Gamblee metadata without a WordPress session or WPVibe.

The [sync workflow](.github/workflows/sync-wordpress-snapshots.yml) refreshes snapshots from `https://www.gamblee.com` every three hours and can also be run manually. It updates files only when their contents changed.

WordPress source routes:
- `/wp-json/gamblee-core/v1/articles/authoring-contract`
- `/wp-json/gamblee-core/v1/articles/vocabulary`
- `/wp-json/gamblee-core/v1/articles/vocabulary/{dimension}`
- `/wp-json/gamblee-core/v1/articles/coverage-index`

The coverage route is paginated and exposes only public metadata for published `news` posts. The GitHub sync combines all pages into one stable `coverage-index.json` snapshot.

If the importer rejects a slug or field, stop and check the latest synchronized contract/vocabulary rather than bypassing importer validation. If a sync workflow is failing, WordPress remains authoritative until the snapshot is healthy again.

## Security and performance

Only public authoring metadata, canonical term names/slugs, and metadata from already-published Articles are mirrored. No importer, private draft content, credentials, or write API is mirrored.

Synchronization runs in GitHub Actions rather than WordPress cron. The public WordPress endpoints are read-only and cacheable; no sync call creates WordPress rows, purges caches, or starts background registry/review work.


## Bonus Research contract

Bonus Offer research has its own public contract namespace:

- [Bonus Research authoring contract](bonuses/authoring-contract.json)
- [Bonus Research instructions](bonuses/README.md)

External assistants should read these GitHub files rather than using WPVibe to inspect the Bonus schema. WordPress/WPVibe remains the authenticated write path for validation and import.
