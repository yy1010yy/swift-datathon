"""Lead independently scores shared extracted country sequences and recurrence rows."""
from pathlib import Path
from collections import Counter
import json
import pandas as pd,numpy as np
base=Path(__file__).resolve().parent;root=base.parents[1]
groups=json.loads((base/'fx_zones.json').read_text())['zones']
mapping={code:i for i,z in enumerate(groups) for code in z}
refined=dict(mapping)
for code in ['FM','MP']: refined[code]=refined['US']
counts=Counter();rows=0
for d in pd.read_csv(root/'outputs/round2/a/fx_zone_routes.csv.gz',dtype=str,keep_default_na=False,chunksize=200000):
    fx=d.fx.astype(int)
    for name,m in [('all_direct',mapping),('residual_refined',refined)]:
        predictions={s:sum(m[a]!=m[b] for a,b in zip(s.split(';'),s.split(';')[1:])) for s in d.countries.unique()}
        v=d.countries.map(predictions)
        t=pd.DataFrame({'model':name,'early':d.early,'route':d.route,'continuity':d.q,'residual':fx-v})
        counts.update(t.value_counts(sort=False).to_dict())
    rows+=len(d)
assert rows==10000000
table=pd.DataFrame([(*k,n) for k,n in counts.items()],columns=['model','early','route','continuity','residual','records'])
table.to_csv(base/'lead_fx_validation.csv',index=False)
assert table.loc[table.model.eq('residual_refined')&table.residual.ne(0),'records'].sum()==0
assert table.loc[table.model.eq('all_direct')&table.residual.ne(0),'records'].sum()==13
a=pd.read_csv(base/'a/recurrence_latest_rows.csv').query("label=='ROMANCE_SCAM'").set_index('source_record').sort_index()
b=pd.read_csv(base/'b/history_lag_rows.csv').query("label=='ROMANCE_SCAM' and with_prior==True").set_index('source_record').sort_index()
c=pd.read_csv(base/'c/romance_predecessors.csv').set_index('source_record').sort_index()
assert len(a)==len(b)==len(c)==1973
np.testing.assert_array_equal(a.lag_seconds,b.seconds_since_last)
np.testing.assert_array_equal(a.lag_seconds,c.lag)
np.testing.assert_allclose(a.amount_ratio,b.ratio_to_last,rtol=1e-12)
np.testing.assert_allclose(a.amount_ratio,c.ratio,rtol=1e-12)
result={'status':'PASS','fx_rows':rows,'unrefined_non_direct_errors':13,'refined_errors':0,
    'romance_latest_predecessor_rows':1973,'raw_sources':'FX country-sequence extraction shared from A; recurrence raw pair extraction shared from C. Scoring/lead graph implementation independent.',
    'limits':'Final FX refinement uses held-out exceptions; full fit is discovery, not untouched validation. Romance equal-time predecessor ambiguity preserved in sensitivity records.'}
(base/'fx_recurrence_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
