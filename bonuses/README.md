# Gamblee Bonus Research contract

Public, read-only snapshot for external AI assistants researching and preparing Gamblee Bonus Offer JSON.

## Start here

- [Authoring contract](authoring-contract.json) — canonical Bonus Research JSON contract, supported mechanics, current taxonomy vocabulary and example shapes.
- One offer object = one market + one vertical. Multiple offers for the same pair are allowed.
- Market and currency are independent.
- Never force-fit an unsupported mechanic. Return it in `schema_gaps` as `unsupported_but_fixable`.
- Do not research or output markets prohibited for public Bonus Offer publication.
- Use official/current evidence and include source URLs.
- Reading this repository cannot write to Gamblee or publish offers.

## Source and freshness

The WordPress source route is:

`/wp-json/gamblee-core/v1/bonuses/authoring-contract`

GitHub stores a public snapshot so assistants do not need a WordPress login or WPVibe connection. The repository's scheduled sync refreshes the snapshot when the public endpoint is available. If the endpoint is temporarily unavailable, the last good GitHub snapshot is retained.

For authoring/research, prefer this GitHub snapshot. Use WordPress/WPVibe only for authenticated validation/import or site administration.
