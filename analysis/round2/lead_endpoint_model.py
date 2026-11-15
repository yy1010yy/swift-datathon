"""Test independent 5% endpoint substitutions across route/month/continuity strata."""
from pathlib import Path
import json,math
import pandas as pd,numpy as np
BASE=Path(__file__).resolve().parent
d=pd.read_csv(BASE/'a/routing_joint.csv')
assert d.n.sum()==10000000
g=d.groupby(['month','route','q','sm','rm']).n.sum().reset_index()
rows=[]
for keys,z in g.groupby(['month','route','q']):
    n=int(z.n.sum()); ps=z.loc[z.sm.eq(1),'n'].sum()/n;pr=z.loc[z.rm.eq(1),'n'].sum()/n
    both=int(z.loc[z.sm.eq(1)&z.rm.eq(1),'n'].sum()); expected=n*ps*pr
    # Phi correlation for two binary endpoint flags.
    table={(int(r.sm),int(r.rm)):int(r.n) for r in z.itertuples()}
    a=table.get((1,1),0);b=table.get((1,0),0);c=table.get((0,1),0);e=table.get((0,0),0)
    denom=math.sqrt((a+b)*(c+e)*(a+c)*(b+e));phi=(a*e-b*c)/denom if denom else float('nan')
    rows.append(dict(month=keys[0],route=['Direct','Indirect','Covered'][keys[1]],continuous=bool(keys[2]),n=n,
      sender_rate=ps,receiver_rate=pr,both_observed=both,both_expected_independent=expected,
      both_standardized=(both-expected)/math.sqrt(max(expected*(1-ps*pr),1e-12)),phi=phi))
out=pd.DataFrame(rows);out.to_csv(BASE/'endpoint_independence_strata.csv',index=False)
tot=d.groupby(['sm','rm']).n.sum();n=int(d.n.sum());ps=d.loc[d.sm.eq(1),'n'].sum()/n;pr=d.loc[d.rm.eq(1),'n'].sum()/n
both=int(d.loc[d.sm.eq(1)&d.rm.eq(1),'n'].sum());expected=n*ps*pr
early=out[out.month.ne('2023-07')];july=out[out.month.eq('2023-07')]
result={'status':'complete','n':n,'sender_mismatch_rate':float(ps),'receiver_mismatch_rate':float(pr),
 'both_observed':both,'both_expected_under_independence':float(expected),
 'strata':len(out),'max_abs_phi':float(out.phi.abs().max()),
 'sender_rate_range_strata':list(map(float,[out.sender_rate.min(),out.sender_rate.max()])),
 'receiver_rate_range_strata':list(map(float,[out.receiver_rate.min(),out.receiver_rate.max()])),
 'early_weighted_sender_rate':float(np.average(early.sender_rate,weights=early.n)),
 'july_weighted_sender_rate':float(np.average(july.sender_rate,weights=july.n)),
 'early_weighted_receiver_rate':float(np.average(early.receiver_rate,weights=early.n)),
 'july_weighted_receiver_rate':float(np.average(july.receiver_rate,weights=july.n)),
 'candidate_rule':'Independently substitute each visible path endpoint with probability approximately 0.05.',
 'limits':['Observed flags cannot identify whether the path endpoint or separate BIC field was changed.',
  'Approximate Bernoulli fit does not prove the random-number call or substitution source.',
  'Sparse April strata widen rate ranges; inspect n before interpreting extremes.']}
(BASE/'endpoint_model_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print(out.to_string(index=False))
