"""Train full-Direct zones, test excluded non-Direct routes on saved sequences."""
from pathlib import Path
from collections import Counter
import pandas as pd,time
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
groups=pd.read_csv(OUT/'fx_zone_components.csv',keep_default_na=False).set_index('country_like_code').zero_fx_component.to_dict()
train=pd.read_csv(OUT/'fx_training_zones.csv',keep_default_na=False).set_index('country_like_code').training_zone.to_dict()
counts=Counter();examples=Counter();n=0
for d in pd.read_csv(ROOT/'outputs/round2/a/fx_zone_routes.csv.gz',dtype=str,keep_default_na=False,chunksize=100000):
 def pred(s,m):
  a=s.split(';');return sum(m[u]!=m[v] for u,v in zip(a,a[1:]))
 predictions={s:pred(s,groups) for s in d.countries.unique()}
 early_predictions={s:pred(s,train) for s in d.countries.unique()}
 p=d.countries.map(predictions);pe=d.countries.map(early_predictions);fx=d.fx.astype(int)
 t=pd.DataFrame({'early':d.early,'route':d.route,'q':d.q,'equal_full_direct_graph':p.eq(fx),'equal_early_graph':pe.eq(fx),'residual_full':fx-p})
 counts.update(t.value_counts(sort=False).to_dict())
 for row in d.loc[pe.ne(fx)].itertuples():examples[(row.countries,row.fx,row.route,row.q)]+=1
 n+=len(d)
table=pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=list(t.columns)+['n'])
table.to_csv(OUT/'fx_route_group_validation.csv',index=False)
pd.DataFrame([list(k)+[v] for k,v in examples.items()],columns=['country_sequence','fx','route','q','n']).to_csv(OUT/'fx_early_exception_sequences.csv',index=False)
print(table.to_string(index=False));print('All rows',n,'nonDirect',int(table.loc[table.route.ne('Direct'),'n'].sum()))
print('Full graph discovery used ALLDirect only; nonDirect routes excluded from zonelearning. Temporal validation remains separate.')
