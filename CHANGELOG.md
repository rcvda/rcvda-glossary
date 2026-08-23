# Changelog — rcvda-glossary

## 2026-08-23 — Phase 2: RCVDA static glossary → `rcvda` lens
- Ingested the RCVDA organisation-wide static glossary (rcvda.org.uk/resources/glossary, 75 rows).
- **22 already in the master** → added `rcvda` to their scope (no duplication). Widened three entries'
  aliases so the static abbreviations resolve: DHSC←DH, Middlesbrough Council←MBC, VCFSE←VCSE.
- **54 new entries** added with full estate treatment (definition + type + authoritative source;
  legislation.gov.uk for statutory terms, gov.uk / body pages otherwise). All carry `agreed: n`
  pending review; `org_ref` left blank for a later networked Find That Charity resolve.
- **Two homonyms correctly kept separate** (the id-model working as designed): RCVDA's `THRIVE`
  (values acronym) ≠ the Thrive Partnership; RCVDA's `MSP` (Making Safeguarding Personal) ≠ My
  Sister's Place. Each is its own entry with a cross-reference note.
- `rcvda` lens now renders **76 terms**. Estate master = 219 entries. The existing 165 CF dictionary
  lines are unchanged except the three deliberate alias widenings; `clr.*` lens counts unchanged.
- **Needs a human eye** (flagged in-entry via `note`): NHS England transition status (abolition
  announced March 2025); the intended sense of `Duty to Co-operate`; the remit of the Health and
  Wellbeing Executive; and whether Care Programme Approach wording should note its replacement.

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
