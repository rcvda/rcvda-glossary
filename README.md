# rcvda-glossary

The **single source of truth** for terminology across the RCVDA estate. One canonical definition
per term, held once; every programme, site and report renders its own **lens** — a filtered,
appropriately-worded view — of this master. A glossary stops being something maintained by hand and
becomes something that is *generated*.

See the architecture proposal (`2026-08-23_estate-glossary-architecture-proposal-v01.md`) for the full rationale.

## The model in one minute

A lens differs from the master on three axes:

1. **Selection** — which terms appear (`scope`).
2. **Meaning** — where a term genuinely means something different in a context (`overrides`).
3. **Register / readability** — an authoritative, source-linked definition for a research report vs a
   reading-age-10 plain-language one for a public site (`plain` + each context's `register`).

## Layout

```
glossary.yml     source of truth — every term, defined once
contexts.yml     the registry of lenses (which glossaries exist, and their register/outputs)
build.py         validates, then generates the estate master + every lens
build/           generated output — DO NOT edit by hand
  estate/        glossary.md · glossary-dictionary.txt · glossary.json   (all 165 terms)
  clr.da/ …      one folder per lens: glossary.md + glossary.json (site feed)
```

## Build

```
pip install pyyaml       # ruamel.yaml only needed for schema migrations
python3 build.py
```

`build.py` fails loudly if an id is duplicated or a term is scoped to a context not in `contexts.yml`,
and lists any term rendered in a `plain` lens that has no plain-language form yet.

## Status

- **Phase 1 complete** — the 165-term Changing Futures Deep Dives glossary is migrated in, as the five
  `clr.*` lenses. The estate master `glossary-dictionary.txt` is byte-identical to the old
  cf-deepdive-glossary output, so the existing report tooling is unaffected.
- **Phase 2 complete** — the RCVDA organisation-wide static glossary is in as the `rcvda` lens (76
  terms): 22 reused from the master, 54 new entries with full definitions + sources. New entries carry
  `agreed: n` pending review and blank `org_ref` for a later resolve. See CHANGELOG for the items
  flagged for a human eye.
- **Phase 3 complete** — Building Our Futures is in as the `bof` lens (43 terms, plain register): 3
  reused from the master, 40 new. Every bof term has a reading-age-10 `plain` form, so the lens and its
  `build/bof/glossary.json` site feed render plain text while the master keeps the authoritative
  definition. New entries carry `agreed: n`.
- **All three estate glossaries are now lenses of one master (259 terms).** Remaining work is Phase 4:
  agree canonical wording for overlaps, resolve `org_ref`s on a networked machine, wire the site-JSON
  into `rcvda-base` so the web glossary pages render from the master, and decide the 12 unscoped terms.

## Two things needing a human decision (carried from the migration)

- **12 unscoped terms.** These sit in the master but are scoped to no lens today (they appeared in no
  report glossary): Areas of complex need, HDRC, IRISi, JSNA, Lived Experience Board, Middlesbrough
  Council, NICE, North Star, Redcar and Cleveland Borough Council, South Tees Hospitals NHS Foundation
  Trust, Stockton-on-Tees Borough Council, Trauma-informed care (TIC). Decide whether each belongs in a
  specific lens or is estate-shared context only.
- Everything else carried over unchanged.
