# Contributing to the estate glossary

**Edit `glossary.yml`, then run `python3 build.py`.** Never edit anything under `build/` by hand — it
is regenerated.

## Adding or editing a term

An entry looks like this (only `term`, `id`, `type`, `definition` and `scope` are strictly required):

```yaml
- term: Adult Social Care          # the canonical head term
  id: adult-social-care            # stable, estate-unique key. NEVER reuse; never key on abbr.
  abbr: ASC
  full_term: Adult Social Care
  aliases: Adult Social Care|ASC   # |-separated; the matcher used by report tooling
  type: statutory                  # statutory | substantive | acronym | organisation | local-programme | method
  definition: The statutory function of a local authority to provide care and support…
  plain: Help from the council for adults who need support with daily life.   # optional, reading-age-10
  source: Care Act 2014 (Part 1; s.1)              # the law / authority that defines it
  source_url: https://www.legislation.gov.uk/ukpga/2014/23/contents
  org_ref: ''                      # findthatcharity org ID for the live body (via charity-data-tools)
  org_ref_url:
  owner: clr.kw                    # optional — which lens owns the canonical wording
  scope: [clr.kw, rcvda]           # context codes from contexts.yml — where this term appears
  agreed: y
```

### Rules
- **`id` is the join key.** Abbreviations collide (AE/A&E; SHAP = Single Homelessness Accommodation
  Programme *and* SHapley Additive exPlanations), so nothing keys on `abbr`. Pick a slug from the term.
- **`scope` codes must exist in `contexts.yml`.** The build fails otherwise.
- **Dual reference.** `source`/`source_url` = the law or authority; `org_ref`/`org_ref_url` = the live
  organisation's Find That Charity ID. Provisions and roles get a source only; non-statutory orgs get an
  org_ref only; some get both.
- **Definition = atomic identity.** `definition` (and its `plain` twin) states *only what the thing is*,
  stripped of every relationship. If a clause says "part of X", "a member of Y", "works with Z", or frames
  the thing through a partnership/programme, it's relational — move it to `context_notes`, keyed to the
  lens or programme it belongs to. Test: if a reader in a different programme would find the clause
  irrelevant, it's a context note, not a definition. (See `tools/DEFINITION_CLEANUP.md`.)
  ```yaml
  definition: The unitary local authority for the Redcar and Cleveland area.
  plain: The local council for the Redcar and Cleveland area.
  context_notes:
    clr:    With Middlesbrough Council, one of the two authorities that make up South Tees.  # all clr.* lenses
    clr.hf: A member of the Tees Valley Lettings Partnership.                                 # Housing First only
    bof:    Building our Futures works with the council and meets it monthly.                 # BoF only
  ```
  A note keyed to a **programme** (`clr`) is inherited by all its lenses; a note keyed to a **lens**
  (`clr.hf`, `bof`) shows only there. Notes are **additive** (rendered after the definition).
- **`overrides` vs `context_notes` — replace vs augment.** `context_notes` *adds* a sentence and keeps the
  canonical definition intact (use this for relational facts). `overrides` *replaces* a field for one
  context — reserve it for the rare case where a term genuinely *means* something different there:
  ```yaml
  overrides:
    rcvda: { plain: "A named worker who helps someone get support from lots of services." }
  ```
- **Plain language.** A lens whose `register` is `plain` (e.g. `bof`) prefers the `plain` field; if a
  term has none, the build falls back to the authoritative definition and prints a warning listing it.

## YAML gotcha
A plain scalar cannot contain `": "`. Wrap any definition containing a colon in double quotes.

## After editing
Run `python3 build.py`, check it reports no validation errors, then commit `glossary.yml`,
`contexts.yml` and the regenerated `build/` together.
