"""Lead reconciliation of independent duration and exact predecessor calculations."""
from pathlib import Path
import json
import pandas as pd,numpy as np
base=Path(__file__).resolve().parent
a=pd.read_csv(base/'a/duration_conditional.csv')
b=pd.read_csv(base/'b/duration_route_fx.csv').query("continuity=='Y'")
a['route']=a.route.map({0:'Direct',1:'Indirect',2:'Covered'});a['period']=a.period.str.lower()
b['period']=b.period.str.lower()
keys=['period','route','participants','fx']
cols=keys+['n','min','p10','median','p90','max','mean']
b=b.rename(columns={'minimum':'min','maximum':'max','q10':'p10','q90':'p90'})
a=a[cols].sort_values(keys).reset_index(drop=True);b=b[cols].sort_values(keys).reset_index(drop=True)
pd.testing.assert_frame_equal(a,b,check_exact=False,rtol=1e-12,atol=1e-8)
ca=pd.read_csv(base/'a/history_independent_rows.csv',keep_default_na=False)
cb=pd.read_csv(base/'b/history_independent_rows.csv',keep_default_na=False)
cc=pd.read_csv(base/'c/history_tests.csv',keep_default_na=False)
print('A row columns:',list(ca));print('B row columns:',list(cb));print('C row columns:',list(cc))
# Grouped exact-predecessor tests are unaffected by power tolerance sensitivity.
ga=pd.read_csv(base/'a/history_independent.csv',keep_default_na=False)
ga['label']=ga.label.replace({'__BLANK__':''})
ga=ga.groupby('label').apply(lambda d:pd.Series({'n':int(d.n.sum()),
 'with_prior':int(d.loc[d.has_prior_same_pair_currency,'n'].sum()),
 'exact':int(d.loc[d.exact_prior_amount,'n'].sum())}),include_groups=False).sort_index()
gb=pd.read_csv(base/'b/history_independent_summary.csv',keep_default_na=False).set_index('label')[['n','with_prior','exact']].sort_index()
gc=pd.read_csv(base/'c/history_summary.csv',keep_default_na=False).rename(columns={'exact_prior':'exact'}).set_index('label')[['n','with_prior','exact']].sort_index()
pd.testing.assert_frame_equal(ga,gb,check_dtype=False)
pd.testing.assert_frame_equal(ga,gc,check_dtype=False)
result={'status':'PASS','continuous_duration_cells':len(a),'continuous_duration_rows':int(a.n.sum()),
 'history_rows':int(ga.n.sum()),'history_exact_checks':'A/B/C exact n, strict-prior availability, amount-copy counts by label match',
 'limits':['History raw extraction shared from C; scoring independent, extraction not independently replicated.',
           'Power10 tolerance/enumeration sensitivity tracked separately; not silently merged.',
           'Selected-pair unlabeled controls are not a random population control.']}
(base/'crosscheck_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2));print(ga.to_string())
