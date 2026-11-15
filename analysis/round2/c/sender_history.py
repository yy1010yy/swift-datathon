"""Targeted third full-file scan: same-sender alternatives to exact-pair history."""
from pathlib import Path
import pandas as pd
import numpy as np
import json,time
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
CACHE=ROOT/'outputs/round2/c';CACHE.mkdir(parents=True,exist_ok=True)
targets=pd.read_csv(P/'labelled.csv',dtype=str,keep_default_na=False)
senders=set(targets.ordering_account); pieces=[]; rows=0; start=time.monotonic()
cols=list(targets.columns)
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,
                     keep_default_na=False,chunksize=100000):
    pieces.append(d[d.ordering_account.isin(senders)].copy());rows+=len(d)
    if rows%1000000==0:print('sender scan',rows,round(time.monotonic()-start,1),flush=True)
assert rows==10000000
h=pd.concat(pieces,ignore_index=True);h.to_csv(CACHE/'sender_history.csv.gz',index=False)
h['_time']=h.epoch_seconds.astype('int64');h['_cents']=np.rint(pd.to_numeric(h.usd_amount)*100).astype('int64')
results=[]
for (sender,currency),g in h.groupby(['ordering_account','currency_code'],sort=False):
    times=g._time.to_numpy();cents=g._cents.to_numpy();accounts=g.beneficiary_account.to_numpy();records=g.source_record.to_numpy()
    for r in g[g.anomaly_type.ne('')].to_dict('records'):
        ix=np.flatnonzero(times<r['_time']);old=cents[ix]
        same=accounts[ix]==r['beneficiary_account']; exact=old==r['_cents']
        exps=np.zeros(len(ix));valid=(old>0)&(r['_cents']>0)
        exps[valid]=np.rint(np.log10(r['_cents']/old[valid]))
        p=valid&(exps!=0)&(np.abs(exps)<=6)&(np.abs(r['_cents']-old*np.power(10.,exps))<=1)
        candidates=ix[exact&~same]; latest=candidates[np.argmax(times[candidates])] if len(candidates) else None
        results.append(dict(source_record=r['source_record'],label=r['anomaly_type'],
            party_pair=r['ordering_type']+r['beneficiary_type'],prior_sender_currency=len(ix),
            prior_same_beneficiary=int(same.sum()),exact_same_beneficiary=int((exact&same).sum()),
            exact_different_beneficiary=int((exact&~same).sum()),power10_any_beneficiary=int(p.sum()),
            latest_different_exact_record=records[latest] if latest is not None else '',
            latest_different_exact_lag=int(r['_time']-times[latest]) if latest is not None else ''))
e=pd.DataFrame(results);e.to_csv(P/'sender_tests.csv',index=False)
summary=e.groupby('label').agg(n=('source_record','count'),
  with_prior_sender=('prior_sender_currency',lambda x:int((x>0).sum())),
  exact_same_beneficiary=('exact_same_beneficiary',lambda x:int((x>0).sum())),
  exact_different_beneficiary=('exact_different_beneficiary',lambda x:int((x>0).sum())),
  power10_any_beneficiary=('power10_any_beneficiary',lambda x:int((x>0).sum()))).reset_index()
summary.to_csv(P/'sender_summary.csv',index=False)
(P/'sender_manifest.json').write_text(json.dumps({'rows_scanned':rows,'history_rows':len(h),
 'labelled_rows_scored':len(e),'target_senders':len(senders),'elapsed_seconds':time.monotonic()-start,
 'limits':'strict earlier times; exact raw account strings; same sender/currency, no assumption previous payments legitimate'},indent=2))
print(summary.to_string(index=False))
