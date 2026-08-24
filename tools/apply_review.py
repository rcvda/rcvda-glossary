#!/usr/bin/env python3
"""Apply your sign-off from tools/agreed_review.csv back into ../glossary.yml.
Fill the `decision` column, then run this, then build.py.
  y / yes / approve   -> set agreed: y (applies revised_definition/revised_plain if you filled them)
  edit                -> apply revised_definition/revised_plain and set agreed: y
  drop                -> remove the entry from the glossary entirely
  n / no / hold        -> leave as agreed: n (kept for later)
  (empty)              -> no change
Preserves file formatting (ruamel).
"""
import csv, os, sys
from ruamel.yaml import YAML
HERE=os.path.dirname(os.path.abspath(__file__)); GLOSS=os.path.join(HERE,"..","glossary.yml"); CSVP=os.path.join(HERE,"agreed_review.csv")
def main():
    if not os.path.exists(CSVP): sys.exit("tools/agreed_review.csv not found — run the review generator first.")
    rows={r["id"]:r for r in csv.DictReader(open(CSVP,encoding="utf-8"))}
    yaml=YAML(); yaml.preserve_quotes=True; yaml.width=100
    d=yaml.load(open(GLOSS,encoding="utf-8"))
    approved=edited=dropped=held=0; drop_ids=set()
    for e in d:
        r=rows.get(e["id"])
        if not r: continue
        dec=(r.get("decision") or "").strip().lower()
        rd=(r.get("revised_definition") or "").strip(); rp=(r.get("revised_plain") or "").strip()
        if dec in ("drop","delete","remove"): drop_ids.add(e["id"]); dropped+=1; continue
        if dec in ("y","yes","approve","edit"):
            if rd: e["definition"]=rd; edited+=1
            if rp: e["plain"]=rp
            e["agreed"]="y"; approved+=1
        elif dec in ("n","no","hold"): held+=1
    d=[e for e in d if e["id"] not in drop_ids]
    yaml.dump(d,open(GLOSS,"w",encoding="utf-8"))
    remaining=sum(1 for e in d if str(e.get("agreed")).lower()=="n")
    print(f"Approved {approved} (of which {edited} with edits), dropped {dropped}, held {held}. "
          f"{remaining} entries still agreed:n. Now run build.py.")
if __name__=="__main__": main()
