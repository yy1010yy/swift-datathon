"""Independent remaining-anomaly history features from C's prior full-source cache."""
from pathlib import Path
import json,time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
HIST=ROOT/'outputs/round2/c/sender_history.csv.gz'
targets={'CEO_SCAM','ACCOUNT_REPLACEMENT_SCAM','CUSTOMER_RECALL'}
start=time.monotonic()
h=pd.read_csv(HIST,dtype=str,keep_default_na=False)
h['_time']=h.epoch_seconds.astype('int64')
h['_amount']=h.usd_amount.astype(float)
h['_cents']=np.rint(h._amount*100).astype('int64')
h['_country']=h.beneficiary_bic8.str[4:6]
control=pd.read_csv(ROOT/'analysis/round2/c/sender_controls.csv',dtype=str,keep_default_na=False)
control=control[control.label.isin(targets)]
queries=[]
for r in control.itertuples(index=False):
    queries.append({'target_record':r.target_record,'label':r.label,'role':r.role,'source_record':r.record})
q=pd.DataFrame(queries).drop_duplicates(['label','role','source_record'])
lookup=h.set_index('source_record',drop=False)
missing=set(q.source_record)-set(lookup.index)
assert not missing,missing
q=q.merge(h[['source_record','ordering_account','currency_code']],on='source_record',how='left',validate='many_to_one')
out=[]; grouped=h.groupby(['ordering_account','currency_code'],sort=False)
for (sender,currency),qq in q.groupby(['ordering_account','currency_code'],sort=False):
    g=grouped.get_group((sender,currency)).sort_values(['_time','source_record'],kind='stable')
    times=g._time.to_numpy(); amount=g._amount.to_numpy(); cents=g._cents.to_numpy()
    acc=g.beneficiary_account.to_numpy(); bic=g.beneficiary_bic8.to_numpy(); country=g._country.to_numpy()
    obic=g.ordering_bic8.to_numpy(); rec=g.source_record.to_numpy()
    for row in qq.itertuples(index=False):
        r=lookup.loc[row.source_record]
        k=np.searchsorted(times,int(r['_time']),side='left')
        old=np.arange(k); sameacc=acc[:k]==r['beneficiary_account']; samebic=bic[:k]==r['beneficiary_bic8']
        samecountry=country[:k]==r['_country']; diffacc=~sameacc; exact=cents[:k]==int(r['_cents'])
        def lag(mask):
            ix=np.flatnonzero(mask)
            return int(r['_time']-times[ix[-1]]) if len(ix) else np.nan
        med=float(np.median(amount[:k])) if k else np.nan
        out.append(dict(target_record=row.target_record,label=row.label,role=row.role,
          source_record=row.source_record,history_n=k,
          recipient_account_seen=int(sameacc.any()),recipient_bic_seen=int(samebic.any()),
          same_bic_different_account=int((samebic&diffacc).any()),
          exact_amount_same_bic_different_account=int((samebic&diffacc&exact).any()),
          recipient_country_seen=int(samecountry.any()),ordering_bic_seen=int((obic[:k]==r['ordering_bic8']).any()),
          amount_prior_percentile=float(np.mean(amount[:k]<=float(r['_amount']))) if k else np.nan,
          amount_over_prior_median=float(float(r['_amount'])/med) if med and med>0 else np.nan,
          lag_any_seconds=lag(np.ones(k,dtype=bool)),lag_same_account_seconds=lag(sameacc),
          lag_same_bic_diff_account_seconds=lag(samebic&diffacc)))
e=pd.DataFrame(out);e.to_csv(OUT/'anomaly_history_features.csv',index=False)
metrics=['recipient_account_seen','recipient_bic_seen','same_bic_different_account',
 'exact_amount_same_bic_different_account','recipient_country_seen','ordering_bic_seen']
rows=[]
for (label,role),g in e.groupby(['label','role']):
    z={'label':label,'role':role,'n':len(g),'history_n_positive':int((g.history_n>0).sum())}
    for m in metrics:z[m+'_n']=int(g[m].sum())
    for m in ['amount_prior_percentile','amount_over_prior_median','lag_any_seconds','lag_same_account_seconds','lag_same_bic_diff_account_seconds']:
        x=g[m].dropna();z[m+'_known']=len(x);z[m+'_median']=float(x.median()) if len(x) else None
    rows.append(z)
s=pd.DataFrame(rows).sort_values(['label','role']);s.to_csv(OUT/'anomaly_history_summary.csv',index=False)
result={'status':'complete','history_cache_rows':len(h),'query_rows':len(e),
 'labels':sorted(targets),'elapsed_seconds':time.monotonic()-start,
 'history_rule':'strict earlier timestamp; exact raw sender/account/currency; source order unused',
 'control':'nearest earlier blank same-sender/currency records selected in round2; rescored using their own past',
 'limits':['Controls may be reused and have shallower histories.','No invoice or intended amount is observed.',
           'Novel recipient/account signatures can reflect ordinary first payments.']}
(OUT/'anomaly_history_manifest.json').write_text(json.dumps(result,indent=2))
print(s.to_string(index=False));print(json.dumps(result,indent=2))
