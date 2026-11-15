"""Test latent currency-zone equivalence learned only from observed zero-FX routes."""
from pathlib import Path
import json,pandas as pd
base=Path(__file__).resolve().parent
d=pd.read_csv(base/'a/direct_country_currency.csv',keep_default_na=False)
parent={x:x for x in set(d['from'])|set(d['to'])}
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]];x=parent[x]
    return x
for r in d[d.fx.eq(0)].itertuples(index=False):
    parent[find(r[0])]=find(r[1])
d['predicted_fx']=[int(find(a)!=find(b)) for a,b in zip(d['from'],d['to'])]
d['match']=d.fx.eq(d.predicted_fx)
d.to_csv(base/'fx_zone_checks.csv',index=False)
zones={}
for code in parent:zones.setdefault(find(code),[]).append(code)
zones=sorted([sorted(v) for v in zones.values()],key=lambda z:(-len(z),z))
(base/'fx_zones.json').write_text(json.dumps({'input_rows':int(d.n.sum()),
    'matching_rows':int(d.loc[d.match,'n'].sum()),'zones':zones,
    'limits':'Equivalence fitted and tested on same direct routes; transitivity tested, no untouched temporal validation; internal country codes only, no real-world mapping used.'},indent=2))
print('Direct population:',int(d.n.sum()),'matches:',int(d.loc[d.match,'n'].sum()))
print('Non-singleton zones:',[z for z in zones if len(z)>1])
print('Contradictions:',d.loc[~d.match].to_string(index=False))
