"""Exact post-debate B/C amount/history and B/A token table reconciliation."""
from pathlib import Path
import json,re
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
b=pd.read_csv(OUT/'history_nearest_decade_rows.csv');c=pd.read_csv(OUT.parent/'c/history_tests.csv')
m=b.merge(c,on='source_record',validate='one_to_one');assert len(m)==22523
assert ((m.history_n>0)==(m.prior_same_pair_currency>0)).all()
assert (m.prior_exact==(m.same_amount_prior>0)).all()
assert (m.prior_power10==(m.power10_prior>0)).all()
b=pd.read_csv(OUT/'amount_unlabeled_currency_party_period.csv',keep_default_na=False)
c=pd.read_csv(OUT.parent/'c/amount_quantiles.csv',keep_default_na=False)
c=c[c.labelled.eq(False)].rename(columns={'party_pair':'party','p01':'q01','p10':'q10','p90':'q90','p99':'q99','mean_log':'log_mean','sd_log':'log_sd'})
c['period']=c.period.map({'pre_july':'early','july':'July'})
m=b.merge(c,on=['currency','party','period'],validate='one_to_one',suffixes=('_b','_c'))
assert len(m)==len(b)==len(c)
assert (m.n_b==m.n_c).all()
for col in ['q01','q10','median','q90','q99','mean','log_mean','log_sd']:
 assert np.allclose(m[col+'_b'],m[col+'_c'],rtol=1e-10,atol=1e-8),col
b=pd.read_csv(OUT/'token_country_joint.csv').rename(columns={'party_type':'type','token_count':'token_n','own_bank_match':'matches_own_bank','other_bank_match':'matches_other_bank','other_party_token_match':'matches_other_token'})
c=pd.read_csv(OUT.parent/'a/text_country_joint.csv')
keys=['side','month','type','token_n','matches_own_bank','matches_other_bank','matches_other_token']
pd.testing.assert_series_equal(b.groupby(keys).n.sum().sort_index(),c.groupby(keys).n.sum().sort_index())
result={'status':'PASS','history_rows':22523,'amount_currency_party_period_cells':len(m),'amount_rows':int(m.n_b.sum()),
 'checks':['B/C all history eligibility/exact/nearest-decade-power row indicators',
 'B/C unlabeled exact amount quantiles/moments/counts across every currency party period',
 'B/A full month/type/side token-country joint tables'],
 'scope':'History uses C shared raw extraction; amount/token scans independent.'}
(OUT/'cross_review_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
