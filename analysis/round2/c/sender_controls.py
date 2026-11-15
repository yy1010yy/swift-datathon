"""Nearest earlier unlabelled same-sender/currency controls; exhaustive exact powers."""
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent
h=pd.read_csv(P.parents[2]/'outputs/round2/c/sender_history.csv.gz',dtype=str,keep_default_na=False)
h['_t']=h.epoch_seconds.astype('int64');h['_c']=np.rint(pd.to_numeric(h.usd_amount)*100).astype('int64')
results=[]
for _,g in h.groupby(['ordering_account','currency_code'],sort=False):
    t=g._t.to_numpy();a=g._c.to_numpy();benef=g.beneficiary_account.to_numpy();labels=g.anomaly_type.to_numpy();record=g.source_record.to_numpy()
    def score(i):
        ix=np.flatnonzero(t<t[i]);old=a[ix];same=benef[ix]==benef[i];exact=old==a[i];power=np.zeros(len(old),dtype=bool)
        for k in list(range(-6,0))+list(range(1,7)):
            power|=(old*10**k==a[i]) if k>0 else (old==a[i]*10**(-k))
        return dict(prior=len(ix),exact_same=int((same&exact).sum()),
              exact_different=int((~same&exact).sum()),power_exact=int(power.sum()))
    for i in np.flatnonzero(labels!=''):
        results.append(dict(target_record=record[i],label=labels[i],role='target',record=record[i],**score(i)))
        ix=np.flatnonzero((t<t[i])&(labels==''))
        if len(ix):
            control=ix[np.argmax(t[ix])]
            results.append(dict(target_record=record[i],label=labels[i],role='prior_control',record=record[control],**score(control)))
e=pd.DataFrame(results);e.to_csv(P/'sender_controls.csv',index=False)
s=e.groupby(['label','role']).agg(n=('record','count'),known=('prior',lambda x:int((x>0).sum())),
  exact_same=('exact_same',lambda x:int((x>0).sum())),
  exact_different=('exact_different',lambda x:int((x>0).sum())),
  power_exact=('power_exact',lambda x:int((x>0).sum()))).reset_index()
s.to_csv(P/'sender_controls_summary.csv',index=False);print(s.to_string(index=False))
