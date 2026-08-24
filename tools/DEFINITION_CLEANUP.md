# Definition cleanup — separating identity from context

## The rule
A term's `definition` (and its `plain` twin) is the **narrowest true statement of what the thing is,
stripped of every relationship**. Any clause that says "part of X", "a member of Y", "works with Z", or
frames the thing through a partnership or programme is *relational* — it belongs to whichever lens X/Y/Z
is the frame for, as a `context_notes` entry, **not** in the definition.

Test: if a reader in a *different* programme would find the clause irrelevant or untrue, it's a context
note, not a definition.

## How it renders (the mechanism)
- `definition` / `plain` — canonical identity, single-sourced, identical in every lens and the master.
- `context_notes:` — a map keyed by a **programme** (`clr`) or a **specific lens** (`clr.hf`, `bof`).
  A lens renders: its register-appropriate definition **+** the programme note it inherits **+** its own
  lens note. A note keyed to a lens the term isn't scoped to simply doesn't render (harmless; ready if
  the term is scoped there later).
- `overrides:` stays for the rare **replace** case (a term that genuinely *means* something different in
  one context). Do **not** use it for local colour — replacing the whole definition is what causes drift.

## Applied in this pass (6)
| Entry | Canonical definition | Context notes moved out |
|---|---|---|
| Redcar & Cleveland BC | "The unitary local authority for the Redcar and Cleveland area." | `clr`: South Tees pairing · `clr.hf`: Tees Valley Lettings Partnership · `bof`: works with BoF monthly |
| Middlesbrough Council | "The unitary local authority for the Middlesbrough area." | `clr`: South Tees pairing · `clr.hf`: Lettings Partnership |
| Stockton-on-Tees BC | "The unitary local authority for the Stockton-on-Tees area, in the Tees Valley." | `clr.hf`: Lettings Partnership (outside the South Tees footprint) |
| North Star | "A housing association … operating across the Tees Valley." | `clr.hf`: Lettings Partnership |
| Beyond Housing | "A registered provider of social housing operating across the Tees Valley and the wider region." | `clr`: named partner on the South Tees CF Programme Board |
| KPI | (plain) "A target used to measure how well something is going." | `bof`: "…e.g. running the programme in five schools each term" |

Note the payoff on RCBC: "South Tees" is a public-health-partnership frame, so it now appears **only** in
CLR lenses — not in the `rcvda` (org-wide) or `bof` (schools) lenses, where it was previously noise.

## Needs your decision (judgement calls)
- **VCFSE** — current definition is self-referential: *"The sector RCVDA works within and holds the
  deep-dive work on behalf of."* Suggest atomic: *"Voluntary, Community, Faith and Social Enterprise —
  charities, community groups, faith organisations and social enterprises,"* with a `clr` note: *"the
  sector RCVDA holds the deep-dive work within."* OK to apply?
- **The unscoped bodies** (Lived Experience Board, Areas of complex need, and North Star until now) —
  their definitions lean on "the programme". They read fine *if* scoped into the CLR lenses; the real
  question is whether they should be scoped there at all (part of the wider "12 unscoped terms" decision).

## Deliberately left as-is (no action)
Entries scoped to a **single programme** that say "the programme" are unambiguous within their own lens —
e.g. the BoF entries (Pupil Journey, CRL, Gatsby Benchmarks, Skills Builder, Anglo American, Dogger Bank,
SEND, KS2, Mantle, ASHE, the networks) and the CLR-internal concepts (ECW, workstream, Crisis Suite,
Programme Board, MD cohort, CJS). "The programme" there means exactly one thing. Only cross-lens leaks
were changed.

## One implication for the CF reports
Moving a clause out of `definition` into `context_notes` means a **regenerated** CF report glossary would
lose that clause unless the report tooling is taught to append the strand's context note. Of the six
above, only **Beyond Housing** feeds a CF report (Housing First, `clr.hf`), and only its "Programme Board
partner" clause is affected. Submitted PDFs are unchanged (they're already generated). When the report
pipeline is re-pointed at this master (Phase 4), have it render `definition + context_notes[strand]`.
