"""Independent C: full-file amount distributions and strictly-past anomaly histories.
Run from project root with .venv/Scripts/python.exe analysis/round2/c/anomaly_amount.py.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json,time
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
SRC=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
cols=['source_record','epoch_seconds','currency_code','usd_amount','ordering_account','beneficiary_account',
      'ordering_type','beneficiary_type','ordering_bic8','beneficiary_bic8','anomaly_type']
started=time.monotonic(); labelled=[]; amounts=defaultdict(list); party=Counter(); rows=0
for d in pd.read_csv(SRC,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    labelled.append(d[d.anomaly_type.ne('')].copy())
    a=pd.to_numeric(d.usd_amount,errors='raise').to_numpy()
    d['period']=np.where(d.epoch_seconds.astype('int64')<1688169600,'pre_july','july')
    d['pair']=d.ordering_type+d.beneficiary_type
    party.update(d[['anomaly_type','pair']].value_counts().to_dict())
    # All amounts retained; separately report blank-label baseline versus all labels.
    d['labelled']=d.anomaly_type.ne(''); d['_amount']=a
    for key,g in d.groupby(['currency_code','pair','period','labelled'],sort=False):
        amounts[key].append(g._amount.to_numpy())
    rows+=len(d)
    if rows%1000000==0: print('pass1',rows,'seconds',round(time.monotonic()-started,1),flush=True)
assert rows==10000000
targets=pd.concat(labelled,ignore_index=True); targets.to_csv(OUT/'labelled.csv',index=False)
party_table=pd.DataFrame([dict(label=k[0],party_pair=k[1],n=n) for k,n in party.items()])
party_table.to_csv(OUT/'label_party.csv',index=False)
stats=[]
for k,v in amounts.items():
    a=np.concatenate(v); q=np.quantile(a,[.01,.1,.5,.9,.99]); logs=np.log(a)
    stats.append(dict(zip(['currency','party_pair','period','labelled'],k))|dict(n=len(a),
      p01=q[0],p10=q[1],median=q[2],p90=q[3],p99=q[4],mean=float(a.mean()),
      mean_log=float(logs.mean()),sd_log=float(logs.std()),
      round_dollar=int((np.rint(a*100).astype(np.int64)%100==0).sum())))
pd.DataFrame(stats).to_csv(OUT/'amount_quantiles.csv',index=False)
del amounts
# Relevant pair histories; no knowledge of later payments is used when scoring a row.
pair_keys=set(targets.ordering_account+'\x1f'+targets.beneficiary_account)
hist=[]; rows2=0
for d in pd.read_csv(SRC,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    keys=d.ordering_account+'\x1f'+d.beneficiary_account
    hist.append(d[keys.isin(pair_keys)].copy())
    rows2+=len(d)
    if rows2%1000000==0: print('pass2',rows2,'seconds',round(time.monotonic()-started,1),flush=True)
assert rows2==rows
h=pd.concat(hist,ignore_index=True)
h['_time']=h.epoch_seconds.astype('int64'); h['_row']=h.source_record.astype('int64')
h['_cents']=np.rint(pd.to_numeric(h.usd_amount).to_numpy()*100).astype(np.int64)
h=h.sort_values(['ordering_account','beneficiary_account','_time','_row'])
h.to_csv(OUT/'relevant_pair_history.csv.gz',index=False)
evaluated=[]
for _,g in h.groupby(['ordering_account','beneficiary_account'],sort=False):
    history=[]
    # Tie-time rows are deliberately not treated as prior, regardless of file order.
    for stamp,batch in g.groupby('_time',sort=False):
        for r in batch.itertuples(index=False):
            # Access nonidentifier columns through record dictionaries below.
            pass
        for r in batch.to_dict('records'):
            prev=[v for v in history if v['currency_code']==r['currency_code']]
            cents=r['_cents']; exact=[v for v in prev if v['_cents']==cents]
            powers=[]
            for v in prev:
                if v['_cents']<=0 or cents<=0: continue
                ratio=cents/v['_cents']
                exponent=int(round(np.log10(ratio)))
                # allow one cent rounding after a decimal-shift transformation
                if exponent!=0 and abs(exponent)<=6 and abs(cents-v['_cents']*10.0**exponent)<=1:
                    powers.append((v,exponent))
            nearest=max(prev,key=lambda v:v['_time']) if prev else None
            evaluated.append(dict(source_record=r['source_record'],label=r['anomaly_type'],
                party_pair=r['ordering_type']+r['beneficiary_type'],epoch_seconds=r['_time'],
                prior_same_pair_currency=len(prev),same_amount_prior=len(exact),power10_prior=len(powers),
                latest_exact_record=exact[-1]['source_record'] if exact else '',
                latest_power_record=powers[-1][0]['source_record'] if powers else '',
                power_exponent=powers[-1][1] if powers else '',
                seconds_since_latest_exact=r['_time']-exact[-1]['_time'] if exact else '',
                seconds_since_last=r['_time']-nearest['_time'] if nearest else '',
                ratio_to_last=cents/nearest['_cents'] if nearest and nearest['_cents'] else ''))
        history.extend(batch.to_dict('records'))
e=pd.DataFrame(evaluated); e.to_csv(OUT/'history_tests.csv',index=False)
summary=[]
for label,g in e.groupby('label',dropna=False):
    known=g.prior_same_pair_currency.gt(0)
    summary.append(dict(label=label,n=len(g),with_prior=int(known.sum()),without_prior=int((~known).sum()),
                        exact_prior=int(g.same_amount_prior.gt(0).sum()),power10_prior=int(g.power10_prior.gt(0).sum())))
s=pd.DataFrame(summary); s.to_csv(OUT/'history_summary.csv',index=False)
meta={'scope_rows':rows,'labelled_rows':len(targets),'target_directed_pairs':len(pair_keys),
      'history_rows':len(h),'seconds':time.monotonic()-started,'input_bytes':SRC.stat().st_size,
      'input_mtime_ns':SRC.stat().st_mtime_ns,
      'controls':'Unlabelled rows in labelled account pairs, NOT population representative.',
      'history':'Only strict earlier epoch timestamps; same pair and currency; tie-time excluded.'}
(OUT/'manifest.json').write_text(json.dumps(meta,indent=2))
print(s.to_string(index=False)); print(json.dumps(meta,indent=2))
