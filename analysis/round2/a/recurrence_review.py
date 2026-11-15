"""Blind latest-strict-prior recurrence comparison on shared extracted histories."""
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(ROOT/'analysis/round2/c/relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
d['t']=d.epoch_seconds.astype('int64');d['row']=d.source_record.astype('int64');d['amt']=pd.to_numeric(d.usd_amount)
records=[]
for key,g in d.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
 prev=None
 for timestamp,batch in g.sort_values(['t','row']).groupby('t',sort=True):
  for r in batch.itertuples():
   if prev is not None:
    records.append([r.source_record,r.anomaly_type or '__BLANK__',r.ordering_type+r.beneficiary_type,
      'early' if r.t<1688169600 else 'july',r.t-prev.t,r.amt/prev.amt,r.amt==prev.amt,prev.source_record])
  prev=batch.iloc[-1]
t=pd.DataFrame(records,columns=['source_record','label','party','period','lag_seconds','amount_ratio','same_amount','previous_source_record'])
t.to_csv(OUT/'recurrence_latest_rows.csv',index=False)
rows=[]
for label,g in t.groupby('label'):
 rows.append([label,len(g),*g.lag_seconds.quantile([.1,.5,.9]).to_list(),*g.amount_ratio.quantile([.1,.5,.9]).to_list(),float((g.amount_ratio>1).mean()),float((g.amount_ratio<1).mean()),float((g.amount_ratio==1).mean())])
summary=pd.DataFrame(rows,columns=['label','n','lag_p10','lag_median','lag_p90','ratio_p10','ratio_median','ratio_p90','increase_fraction','decrease_fraction','equal_fraction'])
summary.to_csv(OUT/'recurrence_latest_summary.csv',index=False);print(summary.to_string(index=False))
strata=[]
for key,g in t.groupby(['label','party','period']):
 strata.append(list(key)+[len(g),float(g.lag_seconds.median()),float(g.amount_ratio.median()),float(g.lag_seconds.mean()),float(np.log(g.amount_ratio).mean()),float(np.log(g.amount_ratio).std())])
pd.DataFrame(strata,columns=['label','party','period','n','lag_median','ratio_median','lag_mean','logratio_mean','logratio_sd']).to_csv(OUT/'recurrence_latest_strata.csv',index=False)
r=t[t.label.eq('ROMANCE_SCAM')];rr=[]
for period,g in r.groupby('period'):
 a=g.lag_seconds.to_numpy();b=np.log(g.amount_ratio.to_numpy())
 rr.append([period,len(g),float(a.mean()),float(a.std()),float(np.mean(a>600)),float(b.mean()),float(b.std()),float((g.amount_ratio>1).mean()),*np.quantile(a,[.1,.5,.9]).tolist(),*np.quantile(g.amount_ratio,[.1,.5,.9]).tolist()])
rom=pd.DataFrame(rr,columns=['period','n','lag_mean','lag_sd','lag_above600_fraction','logratio_mean','logratio_sd','increase_fraction','lag_p10','lag_median','lag_p90','ratio_p10','ratio_median','ratio_p90'])
rom.to_csv(OUT/'romance_generator_fit.csv',index=False);print(rom.to_string(index=False))
print('Candidate lag Exp(mean300sec), multiplier LogNormal(logmean0.4,logSD0.4); empirical log moments close, not unique code identification.')
print('Selected-pair controls; same-currency; exact account strings; latest strictly earlier timestamp; maxsource tie. No causal claim.')
