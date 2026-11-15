"""Exhaustive integer-cent power tests; preserve the initial nearest-power method."""
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent
h=pd.read_csv(P/'relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
h['_t']=h.epoch_seconds.astype('int64');h['_c']=np.rint(pd.to_numeric(h.usd_amount)*100).astype('int64')
results=[]
for _,g in h.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
    t=g._t.to_numpy();a=g._c.to_numpy()
    for i,r in enumerate(g.to_dict('records')):
        old=a[t<t[i]];exact=np.zeros(len(old),dtype=bool);onecent=exact.copy();rounded=exact.copy()
        for k in list(range(-6,0))+list(range(1,7)):
            if k>0:
                delta=np.abs(a[i]-old*10**k)
                exact|=delta==0;onecent|=delta<=1;rounded|=delta==0
            else:
                factor=10**(-k);delta=np.abs(a[i]*factor-old)
                exact|=delta==0;onecent|=delta<=factor
                rounded|=np.rint(old/factor).astype('int64')==a[i]
        results.append(dict(source_record=r['source_record'],label=r['anomaly_type'],prior=len(old),
              exact_power_prior=int(exact.sum()),onecent_power_prior=int(onecent.sum()),
              rounded_power_prior=int(rounded.sum())))
e=pd.DataFrame(results);e.to_csv(P/'power_sensitivity.csv',index=False)
s=e.groupby('label').agg(n=('source_record','count'),known=('prior',lambda x:int((x>0).sum())),
   exact=('exact_power_prior',lambda x:int((x>0).sum())),
   onecent=('onecent_power_prior',lambda x:int((x>0).sum())),
   rounded=('rounded_power_prior',lambda x:int((x>0).sum()))).reset_index()
s.to_csv(P/'power_sensitivity_summary.csv',index=False);print(s.to_string(index=False))
