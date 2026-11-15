"""Explicit generative count models on previously independently verified full counts."""
from pathlib import Path
import math,json
import numpy as np,pandas as pd
root=Path(__file__).resolve().parents[2];out=root/'analysis/round2'
t=pd.read_csv(root/'analysis/reviews/a/route_counts.csv')
assert t['count'].sum()==10000000
results=[]
for (route,period),d in t.groupby(['route','period']):
    n=int(d['count'].sum());edges=d.participants-1
    total_edges=int((edges*d['count']).sum());gap_sum=int((d.gaps*d['count']).sum())
    continuation=gap_sum/(total_edges+gap_sum)
    zero=int(d.loc[d.gaps.eq(0),'count'].sum())
    expected_zero=float((d['count']*(1-continuation)**edges).sum())
    expected_geometric_nll=0.; expected_poisson_nll=0.
    rate=gap_sum/total_edges
    for r in d.itertuples():
        k=r.gaps;e=r.participants-1;w=r.count
        logchoose=math.lgamma(k+e)-math.lgamma(k+1)-math.lgamma(e)
        expected_geometric_nll-=w*(logchoose+e*math.log1p(-continuation)+k*math.log(continuation))
        expected_poisson_nll-=w*(-e*rate+k*math.log(e*rate)-math.lgamma(k+1))
    success=None
    if route!='Direct':success=n/(n+int(((d.participants-3)*d['count']).sum()))
    results.append(dict(route=route,period=period,n=n,participant_geometric_success=success,
        gap_continue_probability=continuation,zero_gap_observed=zero,zero_gap_expected=expected_zero,
        zero_gap_error_pp=100*(zero-expected_zero)/n,
        binomial_support_violations=int(d.loc[d.gaps.gt(edges),'count'].sum()),
        negbin_nll_per_payment=expected_geometric_nll/n,poisson_nll_per_payment=expected_poisson_nll/n))
pd.DataFrame(results).to_csv(out/'lead_count_models.csv',index=False)
print(pd.DataFrame(results).to_string(index=False))
(out/'count_model_formulas.json').write_text(json.dumps({
    'participants':'Direct P=2; non-direct P=3+K, Pr(K=k)=s*(1-s)**k; fit s=N/(N+sum(K)).',
    'gaps':'Given P, model G as sum of P-1 geometric-failure counts: Pr(G=g)=choose(g+P-2,g)*(1-q)**(P-1)*q**g; q=sum(G)/(sum(P-1)+sum(G)).',
    'alternative':'Independent at-most-one gap per edge is refuted by G>P-1; Poisson model compared by per-payment likelihood.',
    'limits':'Counts reused from independently verified initial full scan; monthly fits descriptive, causal insertion order not identified.'},indent=2))
