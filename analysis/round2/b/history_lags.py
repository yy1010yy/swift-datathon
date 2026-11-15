"""Blind B strict prior recurrence/escalation, deterministic latest timestamp/source tie."""
from pathlib import Path
from decimal import Decimal
from itertools import groupby
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'analysis/round2/c/relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
d['_t']=d.epoch_seconds.astype('int64');d['_s']=d.source_record.astype('int64');d['_c']=d.usd_amount.map(lambda x:int(Decimal(x)*100))
rows=[]
for _,g in d.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
 prev=None
 tuples=list(g[['_t','_s','_c','anomaly_type','ordering_type','beneficiary_type']].itertuples(index=False,name=None))
 tuples.sort(key=lambda x:(x[0],x[1]))
 for timestamp,batch in groupby(tuples,key=lambda x:x[0]):
  batch=list(batch)
  for t,s,c,label,op,bp in batch:
   rows.append(dict(source_record=s,label=label,party=op+bp,with_prior=prev is not None,
     seconds_since_last=t-prev[0] if prev else np.nan,ratio_to_last=c/prev[2] if prev else np.nan,
     previous_record=prev[1] if prev else '',current_cents=c,previous_cents=prev[2] if prev else ''))
  prev=batch[-1]
z=pd.DataFrame(rows);z.to_csv(OUT/'history_lag_rows.csv',index=False)
summary=[]
for label,g in z.groupby('label',dropna=False):
 h=g[g.with_prior];r=h.ratio_to_last;s=h.seconds_since_last
 summary.append(dict(label=label,n=len(g),with_prior=len(h),lag_q10=s.quantile(.1),lag_median=s.median(),lag_q90=s.quantile(.9),
   ratio_q10=r.quantile(.1),ratio_median=r.median(),ratio_q90=r.quantile(.9),increased=int(r.gt(1).sum()),decreased=int(r.lt(1).sum()),equal=int(r.eq(1).sum()),within_hour=int(s.le(3600).sum())))
s=pd.DataFrame(summary);s.to_csv(OUT/'history_lag_summary.csv',index=False);print(s.to_string(index=False))
