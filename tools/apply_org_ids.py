#!/usr/bin/env python3
"""Write confirmed org IDs from tools/org_resolution.csv into ../glossary.yml (org_ref only).
    python3 tools/apply_org_ids.py         # 'auto' rows only (default)
    python3 tools/apply_org_ids.py --all   # also review_high / review_low
no_match rows are never written. Preserves file formatting/comments (ruamel). Then run build.py.
Matches the estate convention: org_ref = "findthatcharity org ID <ORGID>".
"""
import csv, os, sys
from ruamel.yaml import YAML
HERE=os.path.dirname(os.path.abspath(__file__)); GLOSS=os.path.join(HERE,"..","glossary.yml"); CSVP=os.path.join(HERE,"org_resolution.csv")
ACCEPT={"auto","review_high","review_low"} if "--all" in sys.argv else {"auto"}
def main():
    if not os.path.exists(CSVP): sys.exit("run tools/resolve_orgs.py first")
    rows={r["term"]:r for r in csv.DictReader(open(CSVP,encoding="utf-8"))}
    yaml=YAML(); yaml.preserve_quotes=True; yaml.width=100
    d=yaml.load(open(GLOSS,encoding="utf-8")); applied=[]; held=[]
    for e in d:
        r=rows.get(e["term"])
        if not r or not (r.get("orgid") or "").strip() or (e.get("org_ref") or "").strip(): continue
        if r["verdict"] not in ACCEPT: held.append(f"{e['term']} [{r['verdict']}]"); continue
        e["org_ref"]=f"findthatcharity org ID {r['orgid']}"
        e["org_ref_url"]=r["ftc_url"] or f"https://findthatcharity.uk/orgid/{r['orgid']}"
        applied.append(f"{e['term']} -> {r['orgid']} [{r['verdict']}]")
    yaml.dump(d,open(GLOSS,"w",encoding="utf-8"))
    print(f"Applied {len(applied)}:"); [print("  "+a) for a in applied]
    if held: print(f"Held ({len(held)}) — use --all to include:"); [print("  "+h) for h in held]
    print("Now run: python3 build.py")
if __name__=="__main__": main()
