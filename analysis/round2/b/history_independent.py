"""Independent strict prior checks from C's extracted relevant-pair raw payments.

Shared extraction is disclosed; logic independently implemented with Decimal cents
and integer arithmetic, not C's history scoring code/results.
"""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal
import json
import math,sys
from bisect import bisect_left, insort
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
p=ROOT/'analysis/round2/c/relevant_pair_history.csv.gz'
d=pd.read_csv(p,dtype=str,keep_default_na=False)
assert len(d)==22523
d['time']=d.epoch_seconds.astype('int64')
d['cents']=d.usd_amount.map(lambda x:int(Decimal(x)*100))
out=[]
nearest_decade='--nearest-decade' in sys.argv
for _,g in d.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
 history={}; ordered=[]
 for timestamp,batch in g.sort_values(['time','source_record']).groupby('time',sort=True):
  for row in batch.itertuples():
   cents=row.cents; hits=[]
   for k in [-6,-5,-4,-3,-2,-1,1,2,3,4,5,6]:
    # Search the exact integer interval of prior cents that maps within ±one target cent.
    factor=10**abs(k)
    lower,upper=(((cents-1+factor-1)//factor,(cents+1)//factor) if k>0 else
                 ((cents-1)*factor,(cents+1)*factor))
    if nearest_decade:
     lower=max(lower,math.ceil(cents/(10.0**k*math.sqrt(10))))
     upper=min(upper,math.floor(cents*math.sqrt(10)/(10.0**k)))
    ix=bisect_left(ordered,lower)
    if ix<len(ordered) and ordered[ix]<=upper:hits.append((history[ordered[ix]],k))
   out.append(dict(source_record=row.source_record,anomaly_type=row.anomaly_type,
    history_n=len(history),prior_exact=cents in history,prior_power10=bool(hits),
    example_power_prior=hits[0][0] if hits else '',example_power=hits[0][1] if hits else ''))
  # Atomically insert equal-time batches, so none sees a same-timestamp predecessor.
  for row in batch.itertuples():
   if row.cents not in history:insort(ordered,row.cents)
   history[row.cents]=row.source_record
suffix='nearest_decade' if nearest_decade else 'independent'
z=pd.DataFrame(out);z.to_csv(OUT/f'history_{suffix}_rows.csv',index=False)
summary=[]
for label,g in z.groupby('anomaly_type',dropna=False):
 summary.append(dict(label=label,n=len(g),with_prior=int(g.history_n.gt(0).sum()),
  exact=int(g.prior_exact.sum()),power10=int(g.prior_power10.sum())))
s=pd.DataFrame(summary);s.to_csv(OUT/f'history_{suffix}_summary.csv',index=False)
print(s.to_string(index=False))
