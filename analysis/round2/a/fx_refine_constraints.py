"""Constraint-derived refinement; all-data discovery, expressly not heldout validation."""
from pathlib import Path
from collections import Counter
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
base=pd.read_csv(OUT/'fx_zone_components.csv',keep_default_na=False).set_index('country_like_code').zero_fx_component.to_dict()
maps={}
for name,links in [('base',[]),('FM_US',[('FM','US')]),('MP_US',[('MP','US')]),('both',[('FM','US'),('MP','US')])]:
 m=base.copy()
 for a,b in links:
  old,new=m[a],m[b];m={k:(new if v==old else v) for k,v in m.items()}
 maps[name]=m
counts=Counter()
for d in pd.read_csv(ROOT/'outputs/round2/a/fx_zone_routes.csv.gz',dtype=str,keep_default_na=False,chunksize=100000):
 seq={s:s.split(';') for s in d.countries.unique()}
 for name,m in maps.items():
  p=d.countries.map({s:sum(m[u]!=m[v] for u,v in zip(a,a[1:])) for s,a in seq.items()})
  t=pd.DataFrame({'model':name,'early':d.early,'route':d.route,'q':d.q,'residual':d.fx.astype(int)-p})
  counts.update(t.value_counts(sort=False).to_dict())
table=pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=list(t.columns)+['n'])
table.to_csv(OUT/'fx_constraint_refinement.csv',index=False)
pd.DataFrame(sorted(maps['both'].items()),columns=['country_like_code','refined_zone']).to_csv(OUT/'fx_refined_zones.csv',index=False)
print(table.groupby(['model','residual']).n.sum().to_string())
print('Both links were inferred from residual paths using all data; this is refined-discovery fit, not validation. Temporal and excluded-route results remain separate.')
