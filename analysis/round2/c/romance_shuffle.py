"""Within-series amount-order control: preserve amounts, pairs and timestamps."""
from pathlib import Path
import pandas as pd
import numpy as np
import json
P=Path(__file__).resolve().parent
d=pd.read_csv(P/'labelled.csv',dtype=str,keep_default_na=False);d=d[d.anomaly_type.eq('ROMANCE_SCAM')].copy()
d['t']=d.epoch_seconds.astype('int64');d['row']=d.source_record.astype('int64');d['amount']=pd.to_numeric(d.usd_amount)
series=[]
for _,g in d.groupby(['ordering_account','beneficiary_account','currency_code']):
    g=g.sort_values(['t','row']);t=g.t.to_numpy();a=g.amount.to_numpy();cur=[];prev=[]
    for i in range(len(g)):
        ix=np.flatnonzero(t<t[i])
        if len(ix):cur.append(i);prev.append(ix[np.flatnonzero(t[ix]==t[ix].max())[-1]])
    series.append((a,np.array(cur,dtype=int),np.array(prev,dtype=int)))
def stats(permuted,rng):
    z=[]
    for a,cur,prev in series:
        x=rng.permutation(a) if permuted else a
        z.extend(np.log(x[cur]/x[prev]))
    z=np.array(z);return dict(n=len(z),mean_logratio=float(z.mean()),sd_logratio=float(z.std()),increase_fraction=float((z>0).mean()))
rng=np.random.default_rng(20261114);observed=stats(False,rng)
controls=pd.DataFrame([stats(True,rng) for _ in range(200)])
controls.to_csv(P/'romance_shuffle_controls.csv',index=False)
out={'observed':observed,'permutations':len(controls),'seed':20261114,
     'control_mean_logratio_range':[float(controls.mean_logratio.min()),float(controls.mean_logratio.max())],
     'control_increase_fraction_range':[float(controls.increase_fraction.min()),float(controls.increase_fraction.max())],
     'control_sd_logratio_range':[float(controls.sd_logratio.min()),float(controls.sd_logratio.max())],
     'controls_mean_at_least_observed':int((controls.mean_logratio>=observed['mean_logratio']).sum()),
     'limits':'Order-shuffle diagnostic, not proof of scam intention or a recovered source program.'}
(P/'romance_shuffle.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
