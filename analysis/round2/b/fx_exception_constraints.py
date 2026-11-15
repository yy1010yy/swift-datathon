"""Independent exception-constraint check; not a fresh holdout or full route rescan."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
m=pd.read_csv(OUT/'fx_components.csv',keep_default_na=False).set_index('country_code').zone.to_dict()
e=pd.read_csv(ROOT/'analysis/round2/a/fx_early_exception_sequences.csv',keep_default_na=False)
d=pd.read_csv(OUT/'fx_direct_rules.csv',keep_default_na=False)
result=[]
for name,links in [('all_direct_graph',[]),('FM_US',[('FM','US')]),('MP_US',[('MP','US')]),('both',[('FM','US'),('MP','US')])]:
 mm=m.copy()
 for x,y in links:
  old,new=mm[x],mm[y];mm={k:new if v==old else v for k,v in mm.items()}
 pred=e.country_sequence.map(lambda s:sum(mm[u]!=mm[v] for u,v in zip(s.split(';'),s.split(';')[1:])))
 pp=[int(mm[f]!=mm[t]) for f,t in zip(d['from'],d['to'])]
 result.append(dict(model=name,selected_exception_records=int(e.n.sum()),selected_remaining_error=int(e.loc[pred.ne(e.fx),'n'].sum()),
  direct_records=int(d.n.sum()),direct_errors=int(d.loc[d.fx.ne(pp),'n'].sum())))
pd.DataFrame(result).to_csv(OUT/'fx_exception_constraints.csv',index=False)
print(pd.DataFrame(result).to_string(index=False))
print('This checks all Direct counts plus the selected exception set only; A full route cache rescan must test whether merges create new errors elsewhere. No holdout claim.')
