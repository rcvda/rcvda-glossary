# Changelog — rcvda-glossary

## 2026-08-23 — Phase 1: estate schema + CF migration
- New estate repo established: `glossary.yml` (source of truth) + `contexts.yml` (lens registry) +
  generalised `build.py` (estate master + per-lens markdown + site JSON, with overrides / plain /
  register handling and validation).
- Migrated the 165-entry Changing Futures Deep Dives glossary in:
  - added a stable `id` to every entry (slug from the term; `iris` / `iris-plus` disambiguated);
  - renamed `appears_in` → `scope` with context codes (`clr.da`, `clr.kw`, `clr.tip`, `clr.hf`, `clr.md`).
- **Non-disruption proven:** the estate master `glossary-dictionary.txt` is byte-identical (sha256) to
  the previous cf-deepdive-glossary output, and the human glossary reproduces the old README exactly
  under the old title. Every original field preserved across all 165 entries.
- Registered the `rcvda` and `bof` lenses (no terms yet — Phases 2/3).
- Carried forward: 12 unscoped terms and the plain-language backfill, both needing a human decision.
