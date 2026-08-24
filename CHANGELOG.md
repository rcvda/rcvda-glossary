# Changelog — rcvda-glossary

## 2026-08-24 — Definition cleanup: full 48-entry sweep
- Worked through all 48 entries whose definitions blended identity with context. **24 split** (the 6 from
  the first pass + 18 more), **24 left as-is** (programme constructs, already-atomic terms, or unscoped
  terms deferred to the 12-unscoped decision). Rule: a term with an identity independent of the programme
  gets that identity as its definition, with the programme's use moved to a `context_note`; a programme
  construct keeps "the programme".
- Notable fixes: **RCVDA** (was the placeholder "the publishing host of this deep-dive series" → its real
  identity as the local infrastructure charity); **VCFSE** (was self-referential → the actual sector);
  **CJS** (didn't define the term → now does). Plus the BoF national/statutory terms (SEND, KS2, EYFS,
  Gatsby, Skills Builder, ASHE, IDACI …) keep their national identity with BoF usage as a `bof` note.
- Full disposition of all 48 in `tools/DEFINITION_CLEANUP.md`. CLR-side splits join Beyond Housing in the
  Phase-4 report-render note (append `context_notes[strand]`).

## 2026-08-23 — `context_notes`: separating identity from context
- New mechanism: `definition`/`plain` now hold only a term's **atomic identity**; relational facts move
  to `context_notes`, a map keyed by **programme** (`clr`, inherited by its lenses) or **lens**
  (`clr.hf`, `bof`). `build.py` renders `definition + inherited + lens note` per lens; the master stays
  canonical; site-JSON carries the note separately. Validates note keys against `contexts.yml`.
  Distinct from `overrides` (which *replaces* a field for genuine meaning divergence).
- First-pass split of 6 conflated entries: Redcar & Cleveland / Middlesbrough / Stockton councils,
  North Star, Beyond Housing (partnership riders → context notes), and KPI (a BoF-only "five schools"
  example moved out of the shared plain field). Payoff: "South Tees" is a public-health-partnership frame,
  so it now renders only in CLR lenses, not the org-wide or schools lenses.
- Docs: contributor rule (atomic definition; augment-vs-replace) in CONTRIBUTING.md; the full method,
  the 6 applied, the judgement calls (VCFSE etc.) and the CF-report implication in
  `tools/DEFINITION_CLEANUP.md`.

## 2026-08-23 — Company org references (Companies House)
- Resolved the company entries: CFE Research `GB-COH-03345012` (via Find That Charity); and — referenced
  directly to Companies House, since FTC doesn't index them — CDPSOFT `GB-COH-02893590`, Anglo American plc
  `GB-COH-03564138`, SSE plc `GB-COH-SC117119` (SSE Renewables' parent), and Lawn Tennis Association Ltd
  `GB-COH-07459469`. (15 org references resolved in total.)
- Left blank with reasons recorded: **Equinor** and **Vårgrønn** (Norwegian, not registered in England &
  Wales) and **Dogger Bank Wind Farm** (a legal partnership, not a single registered company).

## 2026-08-23 — Org references: Sustrans resolved; ICB/NEAS/HCPC confirmed blank
- **Sustrans → GB-CHC-326550** applied (10 verified org_refs total). The charity was rebranded to
  *Walk Wheel Cycle Trust*, which is why the name-based reconcile missed it; alias + rename note added.
- **ICB, North East Ambulance Service, HCPC** confirmed to have no usable Find That Charity record and
  are left blank on purpose (ICBs not on FTC; the CCG-era NHS dataset is out of date; HCPC has no entry).
  `tools/ORG_REF_STATUS.md` updated accordingly.

## 2026-08-23 — Org references resolved (Find That Charity)
- Ran the FTC multi-type resolver (`tools/resolve_orgs.py`) over the 30 organisation entries lacking an
  `org_ref`. **Applied 9 verified matches**: CQC (GB-GOR-PB251), CPS (GB-GOR-D101), DfE (GB-GOR-D6),
  NHS England (GB-GOR-PB481), Darlington BC (GB-LAE-DAL), Hartlepool BC (GB-LAE-HPL), Tees Valley Rural
  Action (GB-CHC-1080282), VONNE (GB-CHC-1084083), NAVCA (GB-CHC-1001635).
- Held back 21 by design: NHS/LA/FT/CCG/OPCC/PCC and local boards left blank on purpose; ICB, NEAS,
  Sustrans, HCPC need by-hand `GB-NHS`/`GB-CHC`/regulator codes; the wind-farm companies need Companies
  House `GB-COH` lookups. Full breakdown + recommendations in `tools/ORG_REF_STATUS.md`; machine output
  in `tools/org_resolution.csv`. Added the resolver (`tools/resolve_orgs.py`, `apply_org_ids.py`).

## 2026-08-23 — Phase 3: Building Our Futures → `bof` lens (plain register)
- Ingested the Building Our Futures glossary (buildingourfutures.org.uk/glossary, 43 entries).
- **3 already in the master** (RCVDA, RCBC, KPI) → added `bof` to scope and gave each a `plain` form.
- **40 new entries** added with the full treatment plus a reading-age-10 `plain` field as the headline:
  the Dogger Bank funding partners, the six Pupil Journey steps, the careers frameworks (Gatsby
  Benchmarks, Skills Builder, CDI, Investors in Careers), and the education terms (EYFS, KS2, SEND,
  Mantle of the Expert), each sourced (legislation.gov.uk for SEND, gov.uk/ONS for EYFS/KS2/ASHE/IDACI,
  the body's page otherwise). All carry `agreed: n`; org_ref blank for a later resolve.
- **Register mechanism proven end-to-end:** the `bof` lens (and its site-JSON feed) renders the plain
  form, while the estate master keeps the authoritative definition for the same term — e.g. Anglo
  American, SEND. The build reports **0 plain-language fallbacks** (every bof term has a plain form).
- `bof` lens = **43 terms**. Estate master = 259 entries. `clr.*` (38/54/45/43/38) and `rcvda` (76)
  lens counts unchanged; the CF dictionary lines are unchanged since Phase 2.

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
