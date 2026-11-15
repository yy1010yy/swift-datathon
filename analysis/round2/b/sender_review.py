"""Blind B same-sender/currency exact/power histories and strict-prior blank controls.

Shared C raw sender-history extraction; independent streaming scorer. Earliest source
breaks ties among controls at the latest eligible timestamp. Controls see only records
strictly earlier than their own timestamp, never target/future records.
"""
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal
from itertools import groupby
import json,time
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
started=time.monotonic()
d=pd.read_csv(ROOT/'outputs/round2/c/sender_history.csv.gz',dtype=str,keep_default_na=False)
d['t']=d.epoch_seconds.astype('int64');d['source']=d.source_record.astype('int64')
d['cents']=d.usd_amount.map(lambda x:int(Decimal(x)*100))
results=[]
for _,g in d.groupby(['ordering_account','currency_code'],sort=False):
 total=0;amount=Counter();benef=defaultdict(Counter);latest_blank=None
 records=sorted(g[['t','source','cents','beneficiary_account','anomaly_type']].itertuples(index=False,name=None))
 for timestamp,batch in groupby(records,key=lambda r:r[0]):
  batch=list(batch);scored=[]
  for t,source,cents,receiver,label in batch:
   candidates=set()
   for k in range(1,7):
    factor=10**k
    if cents%factor==0:candidates.add(cents//factor)
    candidates.add(cents*factor)
   score=dict(record=source,prior=total,exact_same=bool(benef[receiver][cents]),
    exact_different=amount[cents]>benef[receiver][cents],power_exact=any(amount[v]>0 for v in candidates))
   scored.append((source,label,score))
   if label:
    results.append(dict(target_record=source,label=label,role='target',**score))
    if latest_blank is not None:results.append(dict(target_record=source,label=label,role='prior_control',**latest_blank))
  # No same-time predecessor leakage, including controls. Raw source-order tie rule min.
  blanks=[(source,score) for source,label,score in scored if not label]
  if blanks:latest_blank=min(blanks,key=lambda r:r[0])[1]
  for t,source,cents,receiver,label in batch:
   total+=1;amount[cents]+=1;benef[receiver][cents]+=1
z=pd.DataFrame(results);z.to_csv(OUT/'sender_independent_rows.csv',index=False)
summ=[]
for (label,role),g in z.groupby(['label','role']):
 summ.append(dict(label=label,role=role,n=len(g),known=int(g.prior.gt(0).sum()),
   exact_same=int(g.exact_same.sum()),exact_different=int(g.exact_different.sum()),power_exact=int(g.power_exact.sum())))
s=pd.DataFrame(summ);s.to_csv(OUT/'sender_independent_summary.csv',index=False)
assert z[z.role.eq('target')].target_record.nunique()==7006
print(s.to_string(index=False),flush=True)
(OUT/'sender_manifest.json').write_text(json.dumps({'shared_extraction_rows':len(d),'targets':7006,'elapsed_seconds':time.monotonic()-started,
 'controls':'nearest earlier blank same sender/currency; earliest numeric source among timestamp ties; prior to controls own time',
 'amounts':'Decimal integer cents; exact powers10 exponents nonzero±1..6; no tolerance',
 'scope':'independent scorer, shared C full-source targeted extraction'},indent=2))
