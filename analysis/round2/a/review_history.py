"""Independent strict-past history review of C's shared raw extraction, not C results."""
from pathlib import Path
from collections import Counter
import pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(ROOT/'analysis/round2/c/relevant_pair_history.csv.gz',dtype=str,keep_default_na=False)
d['t']=pd.to_numeric(d.epoch_seconds);d['cents2']=np.round(pd.to_numeric(d.usd_amount)*100).astype('int64')
counts=Counter(); examples=[];row_results=[]
for key,g in d.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False):
 seen=set()
 for t,block in g.groupby('t',sort=True):
  for r in block.itertuples():
   cents=r.cents2; exact=cents in seen
   power=False;power_exact=False
   for k in range(1,7):
    factor=10**k
    power |= any(abs(cents-v*factor)<=1 or abs(v-cents*factor)<=factor for v in seen)
    power_exact |= any(cents==v*factor or v==cents*factor for v in seen)
   counts[(r.anomaly_type or '__BLANK__',bool(seen),exact,power)] +=1
   row_results.append([r.source_record,r.anomaly_type,bool(seen),exact,power,power_exact])
  seen.update(block.cents2)
out=pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=['label','has_prior_same_pair_currency','exact_prior_amount','power10_prior_amount_1cent','n'])
out.to_csv(OUT/'history_independent.csv',index=False)
rr=pd.DataFrame(row_results,columns=['source_record','label','has_prior','exact','power_1cent','power_exact'])
rr.to_csv(OUT/'history_independent_rows.csv',index=False)
rr.groupby('label').agg(n=('source_record','size'),power_exact=('power_exact','sum'),power_1cent=('power_1cent','sum')).to_csv(OUT/'history_tolerance_sensitivity.csv')
print('Shared extraction: C relevant_pair_history.csv.gz; no C computed findings used.')
print('Rows:',len(d),'strict earlier timestamps; ties not predecessors; powers1..6,±1cent tolerance.')
for label,g in out.groupby('label'):
 print(label,dict(n=int(g.n.sum()),prior=int(g.loc[g.has_prior_same_pair_currency,'n'].sum()),exact=int(g.loc[g.exact_prior_amount,'n'].sum()),power=int(g.loc[g.power10_prior_amount_1cent,'n'].sum())))
