"""Independent full-file text country-token/bank-code review."""
from pathlib import Path
from collections import Counter
import re,time
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
counts=Counter();rows=0;start=time.monotonic()
cols=['ordering_tokens','beneficiary_tokens','ordering_type','beneficiary_type','ordering_bic8','beneficiary_bic8','epoch_seconds']
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
 month=pd.to_datetime(d.epoch_seconds.astype('int64'),unit='s',utc=True).dt.strftime('%Y-%m')
 for side,other in [('ordering','beneficiary'),('beneficiary','ordering')]:
  cache={v:re.findall(r'<country_code:([^>]+)>',v) for v in d[side+'_tokens'].unique()}
  matches=d[side+'_tokens'].map(cache)
  othercache={v:re.findall(r'<country_code:([^>]+)>',v) for v in d[other+'_tokens'].unique()}
  othermatches=d[other+'_tokens'].map(othercache)
  bank=d[side+'_bic8'].str[4:6];otherbank=d[other+'_bic8'].str[4:6]
  t=pd.DataFrame({'side':side,'month':month,'type':d[side+'_type'],
      'token_n':matches.map(len),'matches_own_bank':[b in m for b,m in zip(bank,matches)],
      'matches_other_bank':[b in m for b,m in zip(otherbank,matches)],
      'matches_other_token':[bool(set(a)&set(b)) for a,b in zip(matches,othermatches)]})
  counts.update(t.value_counts(sort=False).to_dict())
 rows+=len(d)
 if rows%1000000==0:print(rows,round(time.monotonic()-start,1),flush=True)
table=pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=list(t.columns)+['n'])
table.to_csv(OUT/'text_country_joint.csv',index=False)
print(table.groupby(['side','token_n','matches_own_bank','matches_other_bank','matches_other_token']).n.sum().to_string())
print('ROWS',rows)
