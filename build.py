#!/usr/bin/env python3
"""build.py — regenerate the RCVDA estate glossary: the estate master + every lens.

Source of truth: glossary.yml  +  contexts.yml (the lens registry). Edit those, then run:
    python3 build.py

Outputs (under build/):
  build/estate/glossary.md            human-readable master (every term)
  build/estate/glossary-dictionary.txt machine format consumed by the report tooling
  build/estate/glossary.json          full master feed (canonical + plain + scope + overrides)
  build/<context>/glossary.md         one lens (filtered, overrides applied, register-appropriate)
  build/<context>/glossary.json       one lens as a site feed

Requires PyYAML:  pip install pyyaml
"""
import re, sys, os, json
try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

TYPE_ORDER = [
    ("statutory", "Statutory terms", "Rooted in an Act of Parliament; the source links to the specific section on legislation.gov.uk."),
    ("substantive", "Substantive concepts", "Terms carrying a specific or contested meaning, rooted in an originating authority."),
    ("acronym", "Acronyms and abbreviations", "Bodies and standard abbreviations; the source is the body's own name or official page."),
    ("organisation", "Organisations (non-statutory)", "Bodies and services not established by statute; sourced to their own organisation reference (findthatcharity org ID, resolving the Companies House / Charity Commission / Regulator of Social Housing record)."),
    ("local-programme", "Local & programme terms", "South Tees Changing Futures roles, bodies and services; rooted in the programme's own documents."),
    ("method", "Methods & measures", "Research designs, frameworks and measurement tools."),
]

def alpha(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())
def esc(t): return (t or "").replace("|", "\\|").replace("\n", " ").strip()
def full_term(e): return (e.get("full_term") or e.get("term") or "").strip()

def is_agreed(e):
    """Publication gate: an entry reaches a lens/site feed only when agreed == 'y'
    (case-insensitive). Any other value ('n', blank, etc.) holds it back — it stays
    in glossary.yml and the estate master, but does not appear on any site."""
    return str(e.get("agreed", "")).strip().lower() == "y"

def load():
    with open("glossary.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)
def load_contexts():
    with open("contexts.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)

def md_source(e):
    s = (e.get("source") or "").strip(); url = e.get("source_url")
    if url: return f"[{s}]({url})" if s else f"[{url}]({url})"
    return s or "—"
def md_orgref(e):
    s = (e.get("org_ref") or "").strip(); url = e.get("org_ref_url")
    if url: return f"[{s}]({url})" if s else f"[{url}]({url})"
    return s or "—"

# ---- header presets: ESTATE for shipped output, CF for the non-disruption proof ----
CF_TITLE = "Changing Futures Deep Dives — shared glossary"
CF_P1 = ("A single, canonical set of definitions, terms and acronyms for the RCVDA / HDRC South Tees "
         "**Changing Futures Deep Dive** report series. Every report draws its glossary from here, so a "
         "term is defined once, consistently, and rooted in an authoritative source.")
ESTATE_TITLE = "RCVDA estate glossary — master"
ESTATE_P1 = ("A single, canonical set of definitions, terms and acronyms for the RCVDA estate. Every "
             "programme, site and report draws its glossary from here as a *lens*, so a term is defined "
             "once, consistently, and rooted in an authoritative source.")

def build_readme(entries, title=CF_TITLE, p1=CF_P1):
    n = len(entries)
    abbr_entries = sorted([e for e in entries if (e.get("abbr") or "").strip()], key=lambda e: alpha(e["abbr"]))
    out = []
    out.append(f"# {title}\n")
    out.append(p1 + "\n")
    out.append("> **Source of truth:** [`glossary.yml`](glossary.yml). Do not edit this README by hand — "
               "edit `glossary.yml` and run `python3 build.py`. See [CONTRIBUTING.md](CONTRIBUTING.md).\n")
    out.append(f"The glossary is in two parts: an **Abbreviations** list ({len(abbr_entries)} short forms, each with "
               f"the words it stands for, its source and its organisation reference where one exists) and the "
               f"**Glossary of terms** ({n} entries, each defined once under its spelt-out name with a type and an "
               "authoritative source). A term that has an abbreviation is defined in the terms section; the "
               "abbreviation points to it. Statutory terms link to the exact section on legislation.gov.uk.\n")
    out.append("## Abbreviations\n")
    out.append("| Abbreviation | Stands for | Source (law / authority) | Org reference |")
    out.append("|---|---|---|---|")
    for e in abbr_entries:
        out.append(f"| **{esc(e['abbr'])}** | {esc(full_term(e))} | {md_source(e)} | {md_orgref(e)} |")
    out.append("")
    out.append("## Glossary of terms\n")
    out.append("Types: " + "; ".join(f"*{t}* — {d}" for _, t, d in TYPE_ORDER) + "\n")
    out.append("| Term | Abbr. | Type | Definition | Source (law / authority) | Org reference |")
    out.append("|---|---|---|---|---|---|")
    for e in sorted(entries, key=lambda e: alpha(full_term(e))):
        out.append(f"| **{esc(full_term(e))}** | {esc((e.get('abbr') or ''))} | {esc(e.get('type',''))} | "
                   f"{esc(e['definition'])} | {md_source(e)} | {md_orgref(e)} |")
    out.append("")
    out.append("---\n")
    out.append("*Generated from `glossary.yml` by `build.py`. Licensed under [CC BY 4.0](LICENSE).*\n")
    return "\n".join(out)

def build_dictionary(entries):
    out = []
    out.append("# glossary-dictionary.txt — generated from glossary.yml by build.py. DO NOT EDIT BY HAND.")
    out.append("# Format: term ::: aliases (|-separated) ::: type ::: source ::: org_ref ::: definition ::: abbr ::: full_term")
    out.append("# 'source' and 'org_ref' include their URL where one exists. 'abbr' is the short form (blank if none);")
    out.append("# 'full_term' is the spelt-out name. Split into an abbreviations list + a terms section. Consumed by the report tooling.")
    out.append("")
    for e in sorted(entries, key=lambda e: alpha(e["term"])):
        src = (e.get("source") or "").strip()
        if e.get("source_url"): src = f"{src} ({e['source_url']})" if src else e["source_url"]
        orgref = (e.get("org_ref") or "").strip()
        if e.get("org_ref_url"): orgref = f"{orgref} ({e['org_ref_url']})" if orgref else e["org_ref_url"]
        out.append(" ::: ".join([
            e["term"].strip(), (e.get("aliases") or e["term"]).strip(), (e.get("type") or "").strip(),
            src.replace(":::", ";"), orgref.replace(":::", ";"),
            " ".join((e.get("definition") or "").split()),
            (e.get("abbr") or "").strip(), (e.get("full_term") or e["term"]).strip(),
        ]))
    return "\n".join(out) + "\n"

# ---------------- lens layer ----------------
def notes_for(e, code, programme):
    """Additive context notes for this lens: the programme-level note (inherited by all
    its lenses) then the lens-specific note. De-duplicated when code == programme."""
    cn = e.get("context_notes") or {}
    out, seen = [], set()
    for k in (programme, code):
        if k and k in cn and k not in seen and (cn[k] or "").strip():
            seen.add(k); out.append(cn[k].strip())
    return " ".join(out)

def resolve(e, code, register, programme=None):
    """Shallow copy of e with this context's overrides applied, the register-appropriate
    definition selected, and its additive context note attached as `context_note`.
    The canonical `definition` is left intact; the note is separate (composed in for md)."""
    ov = (e.get("overrides") or {}).get(code, {}) or {}
    r = dict(e)
    for k in ("definition", "plain", "source", "source_url", "note"):
        if k in ov: r[k] = ov[k]
    warn = None
    if register == "plain":
        if r.get("plain"):
            r["definition"] = r["plain"]
        else:
            warn = f"{code}: '{e['term']}' has no plain-language form; fell back to the authoritative definition."
    r["context_note"] = notes_for(e, code, programme)
    return r, warn

def lens_entries(entries, code, register, programme=None, member_codes=None):
    # A combined lens (e.g. `clr`) unions all its programme's strand lenses: an entry is in it
    # if its scope hits ANY member code. A normal lens just matches its own code. De-duped because
    # each entry is visited once.
    match = set(member_codes) if member_codes else set()
    match.add(code)
    picked, warns = [], []
    for e in entries:
        if match & set(e.get("scope") or []):
            if not is_agreed(e):
                continue  # held back — not yet agreed
            r, w = resolve(e, code, register, programme)
            picked.append(r)
            if w: warns.append(w)
    return picked, warns

def with_note_in_definition(picked):
    """For markdown rendering: fold the context note into the definition as a trailing sentence."""
    out = []
    for e in picked:
        note = e.get("context_note")
        if note:
            d = (e.get("definition") or "").rstrip()
            if d and d[-1] not in ".!?": d += "."
            e = dict(e, definition=f"{d} {note}")
        out.append(e)
    return out

def entry_json(e):
    return {
        "id": e.get("id"), "term": e.get("term"), "abbr": e.get("abbr") or None,
        "full_term": full_term(e), "aliases": [a for a in (e.get("aliases") or "").split("|") if a],
        "type": e.get("type"), "definition": e.get("definition"),
        "source": e.get("source") or None, "source_url": e.get("source_url"),
        "org_ref": e.get("org_ref") or None, "org_ref_url": e.get("org_ref_url"),
    }

def master_json(entries):
    return [dict(entry_json(e), plain=e.get("plain"), scope=e.get("scope") or [],
                context_notes=e.get("context_notes") or {}, overrides=e.get("overrides") or {})
            for e in entries]

def main():
    entries = load(); reg = load_contexts()
    contexts = reg["contexts"]

    # ---- validation ----
    errs = []
    ids = [e.get("id") for e in entries]
    dup = {i for i in ids if ids.count(i) > 1 and i}
    if dup: errs.append(f"duplicate ids: {sorted(dup)}")
    if any(not i for i in ids): errs.append("entries missing id")
    valid_codes = set(contexts)
    programmes = set(reg.get("programmes") or {})
    valid_note_keys = valid_codes | programmes          # a note may key to a lens OR a programme
    for e in entries:
        for c in (e.get("scope") or []):
            if c not in valid_codes: errs.append(f"'{e['term']}' scope has unknown context {c!r}")
        for c in (e.get("overrides") or {}):
            if c not in valid_codes: errs.append(f"'{e['term']}' override for unknown context {c!r}")
        for c in (e.get("context_notes") or {}):
            if c not in valid_note_keys: errs.append(f"'{e['term']}' context_note for unknown lens/programme {c!r}")
    if errs:
        sys.exit("VALIDATION FAILED:\n  " + "\n  ".join(errs))

    # ---- publication gate: report entries held back (agreed != y) ----
    held = [e for e in entries if not is_agreed(e)]
    if held:
        print(f"Holding back {len(held)} un-agreed term(s) (agreed != y) from ALL lens/site feeds "
              f"(they remain in glossary.yml and the estate master):")
        for e in held:
            print(f"  • {e.get('id')}  (scope {e.get('scope') or []})")
        print()

    os.makedirs("build/estate", exist_ok=True)
    # ---- estate master ----
    open("build/estate/glossary.md","w",encoding="utf-8").write(build_readme(entries, ESTATE_TITLE, ESTATE_P1))
    open("build/estate/glossary-dictionary.txt","w",encoding="utf-8").write(build_dictionary(entries))
    json.dump(master_json(entries), open("build/estate/glossary.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

    # ---- lenses ----
    all_warns = []
    summary = []
    for code, cfg in contexts.items():
        register = cfg.get("register","authoritative")
        programme = cfg.get("programme")
        outs = cfg.get("outputs", ["md","json"])
        member_codes = None
        if cfg.get("combine"):
            member_codes = {c for c, cc in contexts.items() if cc.get("programme") == programme and c != code}
        picked, warns = lens_entries(entries, code, register, programme, member_codes); all_warns += warns
        # In a term's HOME lens (all its scope within this programme) show its short_name; the estate
        # master and cross-programme lenses keep the qualified full_term.
        def _disp(e):
            sn = e.get("short_name")
            if sn and programme:
                progs = {contexts[c].get("programme") for c in (e.get("scope") or []) if c in contexts}
                if progs and progs == {programme}: return sn
            return full_term(e)
        picked = [dict(e, full_term=_disp(e)) for e in picked]
        d = f"build/{code}"; os.makedirs(d, exist_ok=True)
        title = f"{cfg.get('title', code)} — glossary"
        p1 = (f"Lens of the RCVDA estate glossary for **{cfg.get('title', code)}** "
              f"({len(picked)} terms, {register} register). Generated from `glossary.yml`; do not edit by hand.")
        if "md" in outs:
            open(f"{d}/glossary.md","w",encoding="utf-8").write(
                build_readme(with_note_in_definition(picked), title, p1) if picked
                else f"# {title}\n\n_No terms scoped to `{code}` yet._\n")
        if "json" in outs:
            feed = {
                "meta": {"lens": code, "title": cfg.get("title", code), "register": register,
                         "group_order": cfg.get("group_order")},
                "entries": [dict(entry_json(e), context_note=e.get("context_note") or None,
                                 short_name=e.get("short_name"), order=e.get("order"),
                                 groups=(e.get("groups") or {}).get(code)) for e in picked],
            }
            json.dump(feed, open(f"{d}/glossary.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
        summary.append((code, len(picked), register))

    print(f"Built estate master ({len(entries)} entries) + {len(contexts)} lenses.")
    for code, n, r in summary: print(f"  {code:9} {n:4d} terms   [{r}]")
    if all_warns:
        print(f"\n{len(all_warns)} plain-language fallback(s):")
        for w in all_warns[:20]: print("  •", w)

if __name__ == "__main__":
    main()
