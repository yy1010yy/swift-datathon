"""Post-initial exact independent B/C population regrouping and timestamp checks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
b=pd.read_csv(OUT/'counterparty_count_histogram.csv');c=pd.read_csv(OUT.parent/'c/counterparty_count_histogram.csv')
keys=['party','period','payments_per_pair']
pd.testing.assert_series_equal(b.set_index(keys).pairs.sort_index(),c.set_index(keys).pairs.sort_index())
b=pd.read_csv(OUT/'counterparty_cohorts.csv');c=pd.read_csv(OUT.parent/'c/counterparty_cohorts.csv')
pd.testing.assert_series_equal(b.set_index(['party','cohort']).pairs.sort_index(),c.set_index(['party','cohort']).pairs.sort_index())
b=pd.read_csv(OUT/'counterparty_interval_summary.csv')
c=pd.read_csv(OUT.parent/'c/counterparty_interval_summary.csv').rename(columns={'mean_seconds':'mean','sd_seconds':'sd'})
m=b.merge(c,on=['party','period'],validate='one_to_one',suffixes=('_b','_c'))
assert len(m)==8
for col in ['n','mean','sd','p01','p10','median','p90','p99']:assert np.allclose(m[col+'_b'],m[col+'_c'],rtol=1e-12,atol=1e-8),col
bm=json.loads((OUT/'counterparty_initial.json').read_text());cm=json.loads((OUT.parent/'c/counterparty_manifest.json').read_text())
assert bm['records']==cm['blank_rows']==9992994
assert bm['pairs']==cm['pairs']==8258480
assert bm['strict_prior_rows']==cm['strict_prior_rows']==1734514
result={'status':'PASS','records':bm['records'],'pairs':bm['pairs'],'strict_prior_rows':bm['strict_prior_rows'],
 'checks':['Exact count histograms byparty/period/count','Exact early/July observedpaircohorts','All8 interval counts/means/SD/quantiles'],
 'disclosure':'Shared C rawpartitionextraction; independent fullstring regrouping and latestdistincttimestamp join.'}
(OUT/'counterparty_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
