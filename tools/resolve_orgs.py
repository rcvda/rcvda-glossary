#!/usr/bin/env python3
"""Resolve Find That Charity org IDs and write the decision worksheet tools/org_resolution.csv.
Run LOCALLY (needs internet + charity-data-tools). Reads ../glossary.yml, searches FTC across multiple
org types for entries with no org_ref, and writes ONE ROW PER organisation entry with:
  resolver_verdict/orgid/match/ftc_url  – what the machine suggests (blank for already-resolved rows)
  current_org_ref                       – what's in glossary.yml now
  decision                              – YOUR call: keep | blank | apply | skip   (pre-filled where known)
  override_orgid                        – a hand-entered org id to use when decision=apply
  note                                  – provenance / reason
Human columns (decision, override_orgid, note) are PRESERVED across re-runs. Then run apply_org_ids.py.
GB-SHPE (social housing), GB-NHS (NHS trusts/ICBs) and non-FTC companies (Companies House GB-COH) are
added by hand — put the id in override_orgid (or edit glossary.yml directly) and set decision=apply.
"""
import csv, os, sys
try: import yaml
except ImportError: sys.exit("pip install pyyaml")
try: from charity_data_tools.ftc.client import FTCClient
except ImportError: sys.exit("pip install git+https://github.com/rcvda/charity-data-tools.git")
HERE=os.path.dirname(os.path.abspath(__file__)); GLOSS=os.path.join(HERE,"..","glossary.yml"); OUT=os.path.join(HERE,"org_resolution.csv")
PUBLIC_BODIES={"NHS","DHSC","DLUHC","MHCLG","OHID","NICE","NMC","HCPC","SWE","NIHR","OPCC","ICB"}
QUERY_OVERRIDES={"CQC":"Care Quality Commission","NHS":"NHS England","HCPC":"Health and Care Professions Council",
 "OPCC":"Police and Crime Commissioner for Cleveland","PCC":"Police and Crime Commissioner for Cleveland",
 "ICB":"NHS North East and North Cumbria Integrated Care Board","TSAB":"Teeswide Safeguarding Adults Board",
 "North East Ambulance Service":"North East Ambulance Service NHS Foundation Trust","CFE Research (CFE)":"CFE Research"}
SEARCH_TYPES=[None,"community-interest-company","registered-society","government-organisation","local-authority"]
RANK={"auto":3,"review_high":2,"review_low":1,"no_match":0}
COLS=["term","id","type","resolver_verdict","resolver_orgid","resolver_match","ftc_url","current_org_ref","decision","override_orgid","note"]
def better(a,b):
    if a is None: return b
    if b is None: return a
    if RANK.get(b["verdict"],0)>RANK.get(a["verdict"],0): return b
    if RANK.get(b["verdict"],0)==RANK.get(a["verdict"],0) and (b.get("score") or 0)>(a.get("score") or 0): return b
    return a
def main():
    entries=yaml.safe_load(open(GLOSS,encoding="utf-8"))
    prior={}
    if os.path.exists(OUT):
        for r in csv.DictReader(open(OUT,encoding="utf-8")): prior[r["term"]]=r
    orgs=[e for e in entries if e.get("type")=="organisation" or e.get("abbr") in PUBLIC_BODIES or e["term"] in PUBLIC_BODIES]
    todo=[e for e in orgs if not (e.get("org_ref") or "").strip()]
    best={}
    if todo:
        queries={QUERY_OVERRIDES.get(e["term"],e.get("full_term") or e["term"]):e["term"] for e in todo}
        names=list(queries); res_by_name={n:None for n in names}
        with FTCClient() as c:
            for tf in SEARCH_TYPES:
                res=c.search_all(names,type_filter=tf)
                for n in names: res_by_name[n]=better(res_by_name[n],res.get(n))
        for q,term in queries.items(): best[term]=res_by_name.get(q) or {}
    rows=[]
    for e in orgs:
        cur=(e.get("org_ref") or "").strip(); r=best.get(e["term"],{}); p=prior.get(e["term"],{})
        ok=r.get("verdict","no_match")!="no_match"
        rows.append({"term":e["term"],"id":e["id"],"type":e.get("type"),
            "resolver_verdict":r.get("verdict",""),"resolver_orgid":r.get("orgid","") if ok else "",
            "resolver_match":r.get("name","") if ok else "","ftc_url":r.get("ftc_url","") if ok else "",
            "current_org_ref":cur,
            # preserve human columns; default decision from state
            "decision":p.get("decision") or ("keep" if cur else ""),
            "override_orgid":p.get("override_orgid",""),
            "note":p.get("note") or ("Applied." if cur else "OPEN — needs a decision.")})
    rows.sort(key=lambda x:(x["decision"]!="", x["term"]))
    w=csv.DictWriter(open(OUT,"w",newline="",encoding="utf-8"),fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print(f"Wrote {OUT} ({len(rows)} rows). Fill 'decision' (keep/blank/apply/skip) + 'override_orgid', then apply_org_ids.py")
if __name__=="__main__": main()
