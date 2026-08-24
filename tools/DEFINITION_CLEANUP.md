# Definition cleanup — separating identity from context

## The rule
A term's `definition` (and its `plain` twin) is the **narrowest true statement of what the thing is,
stripped of every relationship**. Any clause that says "part of X", "a member of Y", "works with / funds /
adapts Z", or frames the thing through a partnership or programme is *relational* — it moves to a
`context_notes` entry keyed to whichever lens X/Y/Z is the frame for, **not** the definition.

**The test used for the sweep:** does the term have an identity *independent of the programme*?
- **Independent** (an external body, a national/statutory concept, a standard, a company) → the definition
  is that independent identity; the programme's use of it becomes a `context_note`. *(SEND, Gatsby
  Benchmarks, Anglo American, CJS, VCFSE …)*
- **A programme construct** (a role, body, or artefact the programme itself created) → "the programme" is
  intrinsic; leave it. *(Key Worker, ECW, Pupil Journey, the workstreams, the boards, the networks …)*

## The mechanism
- `definition` / `plain` — canonical identity, single-sourced, identical in every lens and the master.
- `context_notes:` — a map keyed by a **programme** (`clr`, inherited by all its lenses) or a **lens**
  (`clr.hf`, `bof`). A lens renders: register-appropriate definition **+** inherited programme note **+**
  its own lens note. A note keyed to a lens the term isn't scoped to simply doesn't render.
- `overrides:` — the rare **replace** case (a term that genuinely *means* something different in one
  context). Not for local colour; replacing the whole definition is what causes drift.

## Applied (24 of the 48)

**First pass (6):** Redcar & Cleveland / Middlesbrough / Stockton councils, North Star, Beyond Housing
(partnership riders → context notes), and KPI (BoF "five schools" example → `bof` note).

**Follow-up pass (18):**

*Estate / CLR side (6):*
- **VCFSE** — now "Voluntary, Community, Faith and Social Enterprise — charities, community groups, faith
  organisations and social enterprises"; the "sector RCVDA works within / holds the deep-dive work on
  behalf of" → `clr` note.
- **RCVDA** — was the placeholder "the publishing host of this deep-dive series"; now its real identity as
  the local infrastructure charity, with "publishing host…" → `clr` note and "runs Building our Futures"
  → `bof` note.
- **CJS** — now actually defines the term (police, courts, prisons, probation); "one of the five
  disadvantage domains" → `clr` note.
- **Crisis Suite** — "one of the four ECW touchpoints" → `clr.kw` note.
- **HDRC South Tees**, **ClRP** — "the programme/vehicle within which this series is produced" → `clr` note.

*BoF — nationally / independently defined terms (identity kept, BoF usage → `bof` note):*
SEND, KS2, EYFS, ASHE, IDACI, Gatsby Benchmarks, Skills Builder Universal Framework, Mantle of the Expert,
CRL, Percy & Mann (2014), Anglo American, Dogger Bank Wind Farm.

## No action (24) — reviewed, correctly left as-is
- **Programme constructs** where "the programme" is intrinsic: Changing Futures, Key Worker, ECW, Multiple
  Disadvantage cohort, the workstreams, Trauma-Informed Champion(s)/Charter, Trauma phases, TIPC, the
  Programme Board, STCFP, Vulnerabilities Service, Lived Experience feed, South Tees geography, the Live
  Well boards, Frequent attender, and the BoF constructs (Pupil Journey, Business/Primary Schools
  Networks, STEM Education & Careers Programmes). These read correctly within their single programme.
- **Already atomic** (matched the scan only incidentally): JCUH, NENC ICB, NEAS, Mental Capacity Act,
  Making Safeguarding Personal, South Tees Hospitals NHS FT.
- **Caseworker** — a deliberate lexical usage note (explains a terminology choice); its purpose *is* the
  context.
- **Unscoped, deferred** to the "12 unscoped terms" decision: Areas of complex need, Lived Experience
  Board, HDRC (national). Their "the programme" wording is fine once their lens home is decided.

## Implication for the CF reports
Moving a clause from `definition` to `context_notes` means a **regenerated** CF report glossary loses it
unless the report render is taught to append the strand's context note. This now applies to the CLR-side
splits (Beyond Housing, VCFSE, RCVDA, CJS, Crisis Suite, HDRC ST, ClRP). Submitted PDFs are unchanged.
**Phase 4 wiring:** point the report tooling at `build/estate` and render `definition + context_notes[strand]`.
