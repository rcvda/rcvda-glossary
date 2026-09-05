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
- **`agreed` gates publication.** An entry only reaches a lens/site feed when `agreed: y` (case-insensitive). Any other value (`n`, blank) holds it back: it stays in `glossary.yml` and the estate master, but does not appear on any site until it is agreed. `build.py` prints the held-back terms each run. Use `agreed: n` for drafted-but-not-signed-off terms.
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
- **Programme constructs: name them with the programme.** If a term only exists inside one programme
  (a network, role, or artefact it created), put the programme in the name — `term`/`full_term` =
  "Building our Futures Business Network" — and add a `short_name` ("Business Network"). The build shows
  the `short_name` as the heading **in that programme's own lens** (where the prefix is redundant) and the
  full qualified name in the estate master and any other lens. Add the short form to `aliases` so it still
  matches. This keeps the definition free of "the programme" scaffolding without inventing a hollow generic.
- **`overrides` vs `context_notes` — replace vs augment.** `context_notes` *adds* a sentence and keeps the
  canonical definition intact (use this for relational facts). `overrides` *replaces* a field for one
  context — reserve it for the rare case where a term genuinely *means* something different there:
  ```yaml
  overrides:
    rcvda: { plain: "A named worker who helps someone get support from lots of services." }
  ```
- **Plain language.** A lens whose `register` is `plain` (e.g. `bof`) prefers the `plain` field; if a
  term has none, the build falls back to the authoritative definition and prints a warning listing it.

- **Definitions carry no abbreviations** (bar universally-known ones such as NHS, A&E, UK). Spell a
  term out on first use with the abbreviation only in parentheses — "the Department for Transport (DfT)",
  not "the DfT". The short forms live in `abbr` / `full_term` / `aliases`, and the abbreviation is never
  spelled out again in a note that already links the term.
- **The general term carries the abbreviation; specific instances alias it.** When several bodies share
  an abbreviation (CAB → Citizens Advice, Middlesbrough Citizens Advice, Citizens Advice Darlington,
  Redcar and Cleveland), give the `abbr` to ONE general entry (`Citizens Advice`, `abbr: CAB`) and leave
  each instance's `abbr` blank, keeping the short form only in its `aliases`. Same pattern as NHS (the
  system) vs NHS England (a body). Cross-link with `[[wiki-links]]`.
- **Split a body from the product it publishes.** A publisher and its dataset/tool/report are two
  entries, not one — College of Policing vs its Crime Reduction Toolkit; OHID vs Fingertips; Sport
  England vs the Active Lives Survey; MaPS vs its Adult Financial Wellbeing Survey. Each gets its own
  `id`; the abbreviation goes on whichever it truly belongs to; cross-link "Produces …" ↔ "Produced by …".
- **A one-off study is not a term.** A single named report or article cited once is a reference-list
  item, not a glossary entry (e.g. a named 2015 evidence review, a single journal). Add recurring
  sources, standing datasets, bodies and concepts; leave individual evidence in the citing document's
  references. Recurring, periodically-refreshed products (a Strategic Housing Market Assessment, a
  Serious Violence Strategic Needs Assessment) do belong, defined as the study *type*.

## Per-site grouping (optional)
A lens can render its own section layout. Define the ordered sections on the context in `contexts.yml`
(`group_order: {Section: [Sub, Sub…]}`), and tag each entry with its place for that lens:
`groups: {rcvda: [Organisations, "Tees Valley"]}`. The per-lens `glossary.json` then carries the
`group_order` in `meta` and each entry's `groups` path — the WordPress glossary block groups by these.
Lenses with no `group_order` render flat/alphabetical.

## YAML gotcha
A plain scalar cannot contain `": "`. Wrap any definition containing a colon in double quotes.

## After editing
Run `python3 build.py`, check it reports no validation errors, then commit `glossary.yml`,
`contexts.yml` and the regenerated `build/` together.
