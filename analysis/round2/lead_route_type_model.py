"""Test one unified visible-route length model and non-direct route-type choice."""
from pathlib import Path
import json,math
import pandas as pd,numpy as np
P=Path(__file__).resolve().parent
d=pd.read_csv(P/'a/routing_joint.csv')
assert d.n.sum()==10000000
length=d.groupby('p').n.sum().reset_index()
n=int(length.n.sum());failures=int(((length.p-2)*length.n).sum());s=n/(n+failures)
length['geometric_expected']=n*s*(1-s)**(length.p-2)
length['relative_error']=length.n/length.geometric_expected-1
length.to_csv(P/'route_length_unified_fit.csv',index=False)

nd=d[d.route.ne(0)].copy();covered=nd.route.eq(2)
covered_rate=np.average(covered,weights=nd.n)
cells=nd.groupby(['month','p','fx']).apply(lambda z:pd.Series({'n':z.n.sum(),
 'covered_n':z.loc[z.route.eq(2),'n'].sum()}),include_groups=False).reset_index()
cells['covered_rate']=cells.covered_n/cells.n
cells['expected']=cells.n*covered_rate
cells['standardized']=(cells.covered_n-cells.expected)/np.sqrt(np.maximum(cells.n*covered_rate*(1-covered_rate),1e-12))
cells.to_csv(P/'covered_choice_cells.csv',index=False)

# Coarser stable strata for interpretability.
strata=nd.groupby(['month','p','route']).n.sum().unstack(fill_value=0)
for r in [1,2]:
 if r not in strata:strata[r]=0
strata['n']=strata[1]+strata[2];strata['covered_rate']=strata[2]/strata.n
strata.reset_index().to_csv(P/'covered_choice_strata.csv',index=False)

result={'status':'complete','n':n,'participant_min':int(length.p.min()),'participant_max':int(length.p.max()),
 'unified_geometric_success_mle':float(s),'direct_share':float(d.loc[d.route.eq(0),'n'].sum()/n),
 'direct_count':int(d.loc[d.route.eq(0),'n'].sum()),
 'direct_rule_violations':int(d.loc[d.route.eq(0)&d.p.ne(2),'n'].sum()+d.loc[d.route.ne(0)&d.p.eq(2),'n'].sum()),
 'non_direct_n':int(nd.n.sum()),'covered_given_non_direct':float(covered_rate),
 'length_max_abs_relative_error_expected_at_least_100':float(length.loc[length.geometric_expected>=100,'relative_error'].abs().max()),
 'length_tail_observed_expected_lt_100':int(length.loc[length.geometric_expected<100,'n'].sum()),
 'covered_rate_stable_strata_range_n_ge_1000':list(map(float,[strata.loc[strata.n>=1000,'covered_rate'].min(),strata.loc[strata.n>=1000,'covered_rate'].max()])),
 'covered_rate_may_to_july_n_ge_10000':list(map(float,[strata.loc[(strata.n>=10000)&(strata.index.get_level_values('month')!='2023-04'),'covered_rate'].min(),strata.loc[(strata.n>=10000)&(strata.index.get_level_values('month')!='2023-04'),'covered_rate'].max()])),
 'candidate':'Draw P=2+geometric failures with success≈0.6323; Direct iff P=2. If P>2, choose Covered with≈0.1131 otherwise Indirect.',
 'limits':['The geometric family is observationally equivalent to floor of an exponential under matching parameterization.',
  'Covered choice may depend weakly on FX, banks, currency, or other fields not represented in this aggregate fit.',
  'The same full population supplied discovery and parameter estimates; month strata are retrospective checks.']}
(P/'route_type_model_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print(length.to_string(index=False));print(strata.reset_index().to_string(index=False))
