"""Independent strict prior checks from C's extracted relevant-pair raw payments.

Shared extraction is disclosed; logic independently implemented with Decimal cents
and integer arithmetic, not C's history scoring code/results.
"""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
p=ROOT/'analysis/round2/c/relevant_pair_history.csv.gz'
d=pd.read_csv(p,dtype=str,keep_default_na=False)
assert len(d)==22523
d['time']=d.epoch_seconds.astype('int64')
d['cents']=d.usd_amount.map(lambda x:int(Decimal(x)*100))
out=[]
for _,g in d.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
 history={}
 for timestamp,batch in g.sort_values(['time','source_record']).groupby('time',sort=True):
  for row in batch.itertuples():
   cents=row.cents; hits=[]
   for previous,record in history.items():
    for k in [-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]:
     # ±one cent in target amount after shift, integer-exact calculation.
     match=abs(previous*(10**k)-cents)<=1 if k>0 else abs(previous-cents*(10**(-k)))<=10**(-k)
     if match:hits.append((record,k))
   out.append(dict(source_record=row.source_record,anomaly_type=row.anomaly_type,
    history_n=len(history),prior_exact=cents in history,prior_power10=bool(hits),
    example_power_prior=hits[0][0] if hits else '',example_power=hits[0][1] if hits else ''))
  # Atomically insert equal-time batches, so none sees a same-timestamp predecessor.
  for row in batch.itertuples():history[row.cents]=row.source_record
z=pd.DataFrame(out);z.to_csv(OUT/'history_independent_rows.csv',index=False)
summary=[]
for label,g in z.groupby('anomaly_type',dropna=False):
 summary.append(dict(label=label,n=len(g),with_prior=int(g.history_n.gt(0).sum()),
  exact=int(g.prior_exact.sum()),power10=int(g.prior_power10.sum())))
s=pd.DataFrame(summary);s.to_csv(OUT/'history_independent_summary.csv',index=False)
print(s.to_string(index=False))
