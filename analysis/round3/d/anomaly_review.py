"""Independent unresolved-label histories; raw scan, strict prior time only."""
from pathlib import Path
import json,time
import numpy as np,pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
CACHE=ROOT/'outputs/round3/d';CACHE.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
LABELS={'CEO_SCAM','ACCOUNT_REPLACEMENT_SCAM','CUSTOMER_RECALL'}
cols=['source_record','epoch_seconds','currency_code','usd_amount','ordering_bic8','beneficiary_bic8','ordering_account','beneficiary_account','ordering_type','beneficiary_type','anomaly_type']
start=time.monotonic();targets=[];scanned=0
for d in pd.read_csv(SRC,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    targets.append(d[d.anomaly_type.isin(LABELS)].copy());scanned+=len(d)
    if scanned%1000000==0:print('target_scan',scanned,round(time.monotonic()-start,1),flush=True)
t=pd.concat(targets,ignore_index=True);assert len(t)==1911
accounts=set(t.ordering_account)|set(t.beneficiary_account)
pieces=[];scanned2=0
for d in pd.read_csv(SRC,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    keep=d.ordering_account.isin(accounts)|d.beneficiary_account.isin(accounts)
    pieces.append(d[keep].copy());scanned2+=len(d)
    if scanned2%1000000==0:print('history_scan',scanned2,round(time.monotonic()-start,1),flush=True)
h=pd.concat(pieces,ignore_index=True)
h['time']=h.epoch_seconds.astype('int64');h['amount']=pd.to_numeric(h.usd_amount);h['cents']=np.rint(h.amount*100).astype('int64')
t['time']=t.epoch_seconds.astype('int64');t['amount']=pd.to_numeric(t.usd_amount);t['cents']=np.rint(t.amount*100).astype('int64')
target_senders=set(t.ordering_account)
hout=h[h.ordering_account.isin(target_senders)].copy()
out_groups=hout.groupby(['ordering_account','currency_code'],sort=False).indices
empty=h.iloc[0:0]
def outgoing(key):
    ix=out_groups.get(key)
    return empty if ix is None else hout.iloc[ix]
controls=[]
for r in t.itertuples(index=False):
    g=outgoing((r.ordering_account,r.currency_code))
    q=g[(g.time<r.time)&g.anomaly_type.eq('')]
    if len(q):
        x=q.loc[q.time.idxmax(),cols+['time','amount','cents']].to_dict();x['target_label']=r.anomaly_type;controls.append(x)
control=pd.DataFrame(controls)
reverse_keys=set((r.beneficiary_account,r.ordering_account,r.currency_code) for r in t.itertuples(index=False))
reverse_keys.update((r.beneficiary_account,r.ordering_account,r.currency_code) for r in control.itertuples(index=False))
hkeys=pd.MultiIndex.from_frame(h[['ordering_account','beneficiary_account','currency_code']])
hr=h[hkeys.isin(reverse_keys)].copy();reverse_groups=hr.groupby(['ordering_account','beneficiary_account','currency_code'],sort=False).indices
def reverse_history(key):
    ix=reverse_groups.get(key)
    return empty if ix is None else hr.iloc[ix]
def score(r,role,label):
    out=outgoing((r.ordering_account,r.currency_code))
    out=out[out.time<r.time]
    same_acc=out.beneficiary_account.eq(r.beneficiary_account);same_bic=out.beneficiary_bic8.eq(r.beneficiary_bic8)
    reverse=reverse_history((r.beneficiary_account,r.ordering_account,r.currency_code))
    reverse=reverse[reverse.time<r.time]
    vals=out.amount.to_numpy();exact=out.cents.eq(r.cents)
    def lag(q):return int(r.time-q.time.max()) if len(q) else np.nan
    return dict(source_record=r.source_record,label=label,role=role,history_n=len(out),recipient_account_seen=bool(same_acc.any()),recipient_bic_seen=bool(same_bic.any()),same_bic_different_account=bool((same_bic&~same_acc).any()),exact_amount_any=bool(exact.any()),exact_amount_same_account=bool((exact&same_acc).any()),exact_amount_diff_account=bool((exact&~same_acc).any()),amount_percentile=float((vals<=r.amount).mean()) if len(vals) else np.nan,amount_over_prior_median=float(r.amount/np.median(vals)) if len(vals) else np.nan,lag_any=lag(out),lag_same_account=lag(out[same_acc]),lag_same_bic_diff_account=lag(out[same_bic&~same_acc]),reverse_seen=bool(len(reverse)),reverse_exact_amount=bool(reverse.cents.eq(r.cents).any()) if len(reverse) else False,reverse_lag=lag(reverse),party=r.ordering_type+r.beneficiary_type)
queries=[score(r,'target',r.anomaly_type) for r in t.itertuples(index=False)]
queries += [score(r,'control',r.target_label) for r in control.itertuples(index=False)]
e=pd.DataFrame(queries);e.to_csv(OUT/'anomaly_rows.csv',index=False)
summary=e.groupby(['label','role']).agg(n=('source_record','size'),history=('history_n',lambda x:int((x>0).sum())),account_seen=('recipient_account_seen','sum'),bic_seen=('recipient_bic_seen','sum'),same_bic_diff=('same_bic_different_account','sum'),exact_any=('exact_amount_any','sum'),exact_same=('exact_amount_same_account','sum'),exact_diff=('exact_amount_diff_account','sum'),reverse=('reverse_seen','sum'),reverse_exact=('reverse_exact_amount','sum'),amount_pct_median=('amount_percentile','median'),amount_ratio_median=('amount_over_prior_median','median'),lag_any_median=('lag_any','median'),lag_account_median=('lag_same_account','median'),reverse_lag_median=('reverse_lag','median')).reset_index()
summary.to_csv(OUT/'anomaly_summary.csv',index=False)
manifest={'status':'complete','source_rows':scanned,'target_rows':len(t),'involved_history_rows':len(h),'controls':len(control),'elapsed_seconds':time.monotonic()-start,'history':'strict earlier timestamp; exact account/currency; both directions retained','limits':['Controls are nearest earlier blank same-sender/currency rows and may repeat.','No invoices or intended amounts are observed.','Reverse payment is only a candidate recall signature.']}
(OUT/'anomaly_manifest.json').write_text(json.dumps(manifest,indent=2))
print(summary.to_string(index=False));print(json.dumps(manifest,indent=2))
