#!/usr/bin/env python3
"""Resolve Find That Charity org IDs for the estate glossary's organisations.
Run LOCALLY (needs internet + charity-data-tools installed). Reads ../glossary.yml, finds every
`type: organisation` (or listed public body) entry with no org_ref, searches FTC across multiple
org types, and writes tools/org_resolution.csv. Then review it and run tools/apply_org_ids.py.
GB-SHPE (social housing) and GB-NHS (NHS trusts/ICBs) are NOT reconcile types — add those by hand.
"""
import csv, os, sys
try: import yaml
except ImportError: sys.exit("pip install pyyaml")
try: from charity_data_tools.ftc.client import FTCClient
except ImportError: sys.exit("pip install git+https://github.com/rcvda/charity-data-tools.git")
HERE=os.path.dirname(os.path.abspath(__file__)); GLOSS=os.path.join(HERE,"..","glossary.yml")
PUBLIC_BODIES={"NHS","DHSC","DLUHC","MHCLG","OHID","NICE","NMC","HCPC","SWE","NIHR","OPCC","ICB"}
QUERY_OVERRIDES={
 "CQC":"Care Quality Commission","NHS":"NHS England","HCPC":"Health and Care Professions Council",
 "OPCC":"Police and Crime Commissioner for Cleveland","PCC":"Police and Crime Commissioner for Cleveland",
 "ICB":"NHS North East and North Cumbria Integrated Care Board","TSAB":"Teeswide Safeguarding Adults Board",
 "North East Ambulance Service":"North East Ambulance Service NHS Foundation Trust","CFE Research (CFE)":"CFE Research",
}
SEARCH_TYPES=[None,"community-interest-company","registered-society","government-organisation","local-authority"]
RANK={"auto":3,"review_high":2,"review_low":1,"no_match":0}
def better(a,b):
    if a is None: return b
    if b is None: return a
    ra,rb=RANK.get(a["verdict"],0),RANK.get(b["verdict"],0)
    if rb>ra: return b
    if rb==ra and (b.get("score") or 0)>(a.get("score") or 0): return b
    return a
def main():
    entries=yaml.safe_load(open(GLOSS,encoding="utf-8"))
    todo=[e for e in entries if not (e.get("org_ref") or "").strip() and (e.get("type")=="organisation" or e.get("abbr") in PUBLIC_BODIES or e["term"] in PUBLIC_BODIES)]
    if not todo: print("Nothing to resolve."); return
    queries={QUERY_OVERRIDES.get(e["term"],e.get("full_term") or e["term"]):e["term"] for e in todo}
    names=list(queries); best={n:None for n in names}
    with FTCClient() as c:
        for tf in SEARCH_TYPES:
            res=c.search_all(names,type_filter=tf)
            for n in names: best[n]=better(best[n],res.get(n))
    rows=[]
    for q,term in queries.items():
        r=best.get(q) or {}; v=r.get("verdict","no_match"); ok=v!="no_match"
        rows.append({"term":term,"query":q,"verdict":v,"score":r.get("score",0),
                     "orgid":r.get("orgid","") if ok else "","matched_name":r.get("name","") if ok else "",
                     "ftc_url":r.get("ftc_url","") if ok else ""})
    out=os.path.join(HERE,"org_resolution.csv")
    w=csv.DictWriter(open(out,"w",newline="",encoding="utf-8"),fieldnames=["term","query","verdict","score","orgid","matched_name","ftc_url"])
    w.writeheader(); w.writerows(rows)
    print(f"Wrote {out} ({len(rows)} rows). Review, then: python3 tools/apply_org_ids.py")
if __name__=="__main__": main()
