# Gamblee Article Editorial Guidelines

These rules apply to every Gamblee news Article prepared using `authoring-contract.json`. The contract remains authoritative for schema, taxonomies and ZIP packaging; this document governs editorial presentation. Read this file before drafting an Article.

## Reporting and prose

- Lead with the actual verified development. Write concise, factual, source-led news copy, not marketing copy or gambling advice.
- Distinguish confirmed facts, allegations, company claims, independent research, and analysis. Describe proposals as proposals and pending proceedings as unresolved.
- Contextually cite primary sources (regulators, courts, filings, operators, researchers) and credit original reporting. Do not imply Gamblee independently discovered a story reported elsewhere.
- No H1 in `content_html`. Use `<p>`, `<h2>`, restrained `<h3>`, and occasional natural lists. Avoid generic background, SEO padding, formulaic conclusions, artificial summaries and repeated context.

## Internal links: natural, not announced

- Read the current `coverage-index.json` before drafting; compare the underlying event against existing coverage and link only to genuinely relevant **published** Gamblee articles using their exact indexed URLs.
- Embed links directly into sentences where the referenced facts or event already belong. Use natural, specific anchor text; do not construct extra sentences just to insert links.
- Do **not** introduce links with phrases like "As Gamblee previously reported", "For more context", "Read our coverage", "Related reading", or announce that the article is interlinked.
- No link quota or default target count. Zero internal links is preferable to forced or tangential links. Avoid repeated links to the same destination.
- Link external primary evidence just as naturally, attached to the claims it supports. Do not add a generic source/link dump in place of contextual attribution.
- Verify that linked pages actually correspond to the claim. Treat new material facts in older stories as an update where appropriate, not automatically as a new article.

**Good:** "The regulator's decision follows [earlier restrictions on sports-event contracts](https://www.gamblee.com/articles/ohio-says-it-will-enforce-gambling-laws-against-kalshi/)." (Only when that relationship is sourced and relevant.)

**Avoid:** "For more context, see Gamblee's previous article about prediction markets."

## Featured images: restrained and credible

- Prefer genuine, relevant editorial or primary-source photography **with verified commercial reuse rights**. Credit the rights holder and retain source-page information as required by the image type and contract.
- If no suitable reusable real image exists, use one bespoke generated image with a **single clear subject**, simple composition, restrained colour palette, natural lighting and realistic textures. Favor documentary-style restraint over conceptual spectacle.
- Avoid multi-panel collages, split-screen composites, infographics disguised as photographs, crowded arrangements, unnatural glow, dramatic cyberpunk effects, floating symbols, fabricated official documents, synthetic screenshots/interfaces, and made-up logos or legible text.
- Avoid the default visual formula of a laptop + poker chips + flag + charts. Do not reuse the same subject, angle, palette or composition across consecutive stories. Rotate responsibly among real locations, architecture, appropriate objects and genuine licensed portraits.
- A photograph of the real subject is preferable to a fabricated depiction of a named person or real-world allegation. For unresolved allegations, use neutral illustrative imagery; never visually imply guilt.
- Keep a clean, readable thumbnail crop. One separate image per Article. Do not combine different stories into a collage or rely on an unrelated image merely to fill the slot.
- If an appropriate image cannot be verified or created, use `featured_image.type=none` instead of supplying a misleading image.

## Pre-delivery review

1. Re-read the live GitHub authoring contract and only the relevant canonical vocabularies.
2. Check current published coverage for duplicate events and meaningful updates; acknowledge that unpublished drafts are not indexed.
3. Verify consequential facts and dates against sources; maintain allegations/proposals/decisions distinctions.
4. Read all internal and external links in context: relevant destination, unobtrusive anchor, no contrived linking sentences.
5. Inspect the featured image: rights/credit where applicable, credible minimal composition, distinct from recent images, accurate alt text.
6. Validate the complete `article.json` against the current schema and check ZIP root contents/image filename. Never publish directly.

When this guide and the machine authoring contract conflict on file structure, fields, or canonical values, follow the machine contract.
