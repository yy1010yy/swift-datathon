"""Reconcile independently scanned exact conditional amount summaries."""
from pathlib import Path
import json
import pandas as pd,numpy as np
root=Path(__file__).resolve().parents[2];base=root/'analysis/round2'
a=pd.read_csv(base/'a/amount_conditional.csv').query("currency!='__ALL_CURRENCIES__'")
b=pd.read_csv(base/'b/amount_unlabeled_currency_party_period.csv').rename(columns={'q10':'p10','q90':'p90','q99':'p99'})
c=pd.read_csv(base/'c/amount_quantiles.csv').query('labelled==False').rename(columns={'party_pair':'party'})
keys=['currency','party','period']
for d in [a,b,c]: d['period']=d.period.str.lower().replace({'pre_july':'early'})
cols=keys+['n','p10','median','p90','p99']
a=a[cols].sort_values(keys).reset_index(drop=True)
b=b[cols].sort_values(keys).reset_index(drop=True)
c=c[cols].sort_values(keys).reset_index(drop=True)
pd.testing.assert_frame_equal(a,b,check_exact=False,rtol=1e-12,atol=1e-8)
pd.testing.assert_frame_equal(a,c,check_exact=False,rtol=1e-12,atol=1e-8)
assert a.n.sum()==9992994
ratios=[]
for (currency,period),g in a.groupby(['currency','period']):
    z=g.set_index('party')
    if all(p in z.index for p in ['BB','BC','CB','CC']):
        ratios.append({'currency':currency,'period':period,'minimum_cell_n':int(z.n.min()),
            'BB_over_BC':z.loc['BB','median']/z.loc['BC','median'],
            'BC_over_CC':z.loc['BC','median']/z.loc['CC','median'],
            'CB_over_CC':z.loc['CB','median']/z.loc['CC','median']})
r=pd.DataFrame(ratios);r.to_csv(base/'amount_scale_ratios.csv',index=False)
result={'status':'PASS','rows':int(a.n.sum()),'matched_currency_party_period_cells':len(a),
    'independence':'Three separate full10M CSV scans, blank labels only, exact quantiles; same raw input.',
    'count_check':'exact','float_tolerance':'rtol1e-12 atol1e-8',
    'scope':'Numerical consistency; distributional/economic interpretation separately reviewed.'}
(base/'amount_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2));print(r.query('minimum_cell_n>=1000').describe().to_string())
