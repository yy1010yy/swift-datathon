"""Vectorized strictly-past scorer, avoiding scalar log calls in long histories."""
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent
h=pd.read_csv(P/'relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
h['_time']=h.epoch_seconds.astype('int64');h['_row']=h.source_record.astype('int64')
h['_cents']=np.rint(pd.to_numeric(h.usd_amount)*100).astype('int64')
h=h.sort_values(['ordering_account','beneficiary_account','_time','_row'])
result=[]
for _,g in h.groupby(['ordering_account','beneficiary_account'],sort=False):
    records=g.to_dict('records'); t=g._time.to_numpy(); c=g._cents.to_numpy(); currencies=g.currency_code.to_numpy()
    for i,r in enumerate(records):
        ix=np.flatnonzero((t[:i]<t[i])&(currencies[:i]==currencies[i])); old=c[ix]
        exact_ix=ix[old==c[i]]
        exps=np.zeros(len(old)); valid=(old>0)&(c[i]>0)
        exps[valid]=np.rint(np.log10(c[i]/old[valid]))
        candidate=valid&(exps!=0)&(np.abs(exps)<=6)
        power_mask=candidate&(np.abs(c[i]-old*np.power(10.,exps))<=1)
        power_ix=ix[power_mask]; power_exps=exps[power_mask]
        nearest=ix[np.argmax(t[ix])] if len(ix) else None
        result.append(dict(source_record=r['source_record'],label=r['anomaly_type'],
           party_pair=r['ordering_type']+r['beneficiary_type'],epoch_seconds=int(t[i]),
           prior_same_pair_currency=len(ix),same_amount_prior=len(exact_ix),power10_prior=len(power_ix),
           latest_exact_record=records[exact_ix[-1]]['source_record'] if len(exact_ix) else '',
           latest_power_record=records[power_ix[-1]]['source_record'] if len(power_ix) else '',
           power_exponent=int(power_exps[-1]) if len(power_ix) else '',
           seconds_since_latest_exact=int(t[i]-t[exact_ix[-1]]) if len(exact_ix) else '',
           seconds_since_last=int(t[i]-t[nearest]) if nearest is not None else '',
           ratio_to_last=float(c[i]/c[nearest]) if nearest is not None and c[nearest] else ''))
e=pd.DataFrame(result);e.to_csv(P/'fast_history_tests.csv',index=False)
s=e.groupby('label').agg(n=('source_record','count'),
    with_prior=('prior_same_pair_currency',lambda x:int((x>0).sum())),
    exact_prior=('same_amount_prior',lambda x:int((x>0).sum())),
    power10_prior=('power10_prior',lambda x:int((x>0).sum()))).reset_index()
s['without_prior']=s.n-s.with_prior;s.to_csv(P/'fast_history_summary.csv',index=False)
print(s.to_string(index=False),flush=True)
