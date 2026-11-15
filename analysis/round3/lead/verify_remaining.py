"""Lead reconciliation for anomalies, intermediary hubs and Covered choice."""
from pathlib import Path
import json
import numpy as np,pandas as pd

ROOT=Path(__file__).resolve().parents[3];B=ROOT/'analysis/round3/b';C=ROOT/'analysis/round3/c';D=ROOT/'analysis/round3/d';OUT=Path(__file__).resolve().parent
c=pd.read_csv(C/'anomaly_history_summary.csv').rename(columns={'role':'c_role'})
d=pd.read_csv(D/'anomaly_summary.csv').rename(columns={'role':'d_role'})
rolemap={'target':'target','prior_control':'control'}
checks=[]
for label in ['ACCOUNT_REPLACEMENT_SCAM','CEO_SCAM','CUSTOMER_RECALL']:
  for cr,dr in rolemap.items():
    x=c[(c.label==label)&(c.c_role==cr)].iloc[0];y=d[(d.label==label)&(d.d_role==dr)].iloc[0]
    pairs=[('n','n'),('history_n_positive','history'),('recipient_account_seen_n','account_seen'),('recipient_bic_seen_n','bic_seen')]
    for a,b in pairs: assert int(x[a])==int(y[b])
    assert np.isclose(x.amount_prior_percentile_median,y.amount_pct_median,equal_nan=True)
    assert np.isclose(x.amount_over_prior_median_median,y.amount_ratio_median,equal_nan=True)
    checks.append({'label':label,'role':dr,'n':int(y.n),'history':int(y.history),'account_seen':int(y.account_seen),'bic_seen':int(y.bic_seen)})

bc=pd.read_csv(B/'covered_bank_models.csv');dc=pd.read_csv(D/'covered_models.csv')
covered={}
for model in ['global','sender_country','sender_bic','bic_pair']:
  dm='endpoint_pair' if model=='bic_pair' else model
  x=bc[bc.model==model].iloc[0] if model=='global' else bc[(bc.model==model)&(bc.alpha==10)].iloc[0]
  y=dc[dc.model==dm].iloc[0]
  assert abs(x.test_nll-y.nll)<1e-6 and abs(x.known_key_share-y.known_share)<1e-9
  covered[model]={'july_nll':float(x.test_nll),'coverage':float(x.known_key_share)}

bn=json.loads((B/'network_stability.json').read_text());ds=pd.read_csv(D/'intermediary_stability.csv');dr=pd.read_csv(D/'intermediary_smoothing_recheck.csv')
first=ds[ds.target=='first'].iloc[0];smooth=dr[dr.target=='first'].iloc[0]
assert abs(first.total_variation-bn['early_july_total_variation'])<1e-12
assert abs(first.pearson_rate_correlation-bn['active_rate_correlation'])<1e-12
assert abs(smooth.jeffreys_nll-6.26509)<1e-3

result={'status':'PASS','anomaly_cells':checks,
 'recall_reverse_target_rows':int(d[(d.label=='CUSTOMER_RECALL')&(d.d_role=='target')].reverse.iloc[0]),
 'recall_exact_reverse_target_rows':int(d[(d.label=='CUSTOMER_RECALL')&(d.d_role=='target')].reverse_exact.iloc[0]),
 'covered_models':covered,
 'intermediary':{'rows':3676720,'first_tv':float(first.total_variation),'first_rate_correlation':float(first.pearson_rate_correlation),
  'first_global_jeffreys_nll':float(smooth.jeffreys_nll),'unseen_july_rows':int(smooth.unseen_july_rows)},
 'scope':'C/D anomaly initials reconcile exactly; B/D Covered NLL/coverage reconcile; B/D first-intermediary stability and smoothing reconcile.'}
(OUT/'remaining_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
