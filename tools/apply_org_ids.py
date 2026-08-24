#!/usr/bin/env python3
"""Write org IDs into ../glossary.yml from the tools/org_resolution.csv decision worksheet (org_ref only).
Honours the `decision` column:
  apply / y / yes        -> write override_orgid if given, else resolver_orgid (must not be no_match)
  keep                   -> leave the existing org_ref untouched
  blank / skip / n       -> leave org_ref empty on purpose
  (empty)                -> fall back to verdict: auto applied; review_* only with --all
override_orgid may be a Companies-House id (GB-COH-...): it is referenced to Companies House; any other
id is referenced to Find That Charity. Preserves file formatting (ruamel). Then run build.py.
"""
import csv, os, sys
from ruamel.yaml import YAML
HERE=os.path.dirname(os.path.abspath(__file__)); GLOSS=os.path.join(HERE,"..","glossary.yml"); CSVP=os.path.join(HERE,"org_resolution.csv")
ALL="--all" in sys.argv
CH="https://find-and-update.company-information.service.gov.uk/company/"
FTC="https://findthatcharity.uk/orgid/"
def ref_for(orgid):
    orgid=orgid.strip()
    if orgid.upper().startswith("GB-COH-"):
        num=orgid.split("GB-COH-",1)[1]
        return f"Companies House GB-COH-{num}", CH+num
    return f"findthatcharity org ID {orgid}", FTC+orgid
def main():
    if not os.path.exists(CSVP): sys.exit("run tools/resolve_orgs.py first")
    rows={r["term"]:r for r in csv.DictReader(open(CSVP,encoding="utf-8"))}
    yaml=YAML(); yaml.preserve_quotes=True; yaml.width=100
    d=yaml.load(open(GLOSS,encoding="utf-8")); applied=[]; held=[]
    for e in d:
        r=rows.get(e["term"])
        if not r: continue
        dec=(r.get("decision") or "").strip().lower()
        if dec in ("keep","blank","skip","n","no"): continue
        orgid=(r.get("override_orgid") or "").strip() or (r.get("resolver_orgid") or "").strip()
        if not orgid: 
            if dec in ("apply","y","yes","accept"): held.append(f"{e['term']} [decision=apply but no orgid]")
            continue
        if dec in ("apply","y","yes","accept"):
            pass
        else:  # empty decision -> verdict default
            v=(r.get("resolver_verdict") or "no_match")
            if v=="no_match" or (v!="auto" and not ALL): 
                if v!="no_match": held.append(f"{e['term']} [{v}]")
                continue
        if (e.get("org_ref") or "").strip(): continue   # don't overwrite an existing ref
        e["org_ref"],e["org_ref_url"]=ref_for(orgid); applied.append(f"{e['term']} -> {orgid}")
    yaml.dump(d,open(GLOSS,"w",encoding="utf-8"))
    print(f"Applied {len(applied)}:"); [print("  "+a) for a in applied]
    if held: print(f"Held ({len(held)}):"); [print("  "+h) for h in held]
    print("Now run: python3 build.py")
if __name__=="__main__": main()
