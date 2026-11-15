"""Independent binomial/geometric/negative-binomial gap models from verified joint counts."""
from pathlib import Path
import math,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'analysis/reviews/a/route_counts.csv')
rows=[]
for (route,period),g in d.groupby(['route','period']):
 n=g['count'].sum();mean_p=np.average(g.participants,weights=g['count']);mean_gap=np.average(g.gaps,weights=g['count'])
 rows.append(dict(route=route,period=period,n=int(n),participant_mean=mean_p,gap_mean=mean_gap,
    gap_n=int(g.loc[g.gaps.gt(0),'count'].sum()),participants_2_n=int(g.loc[g.participants.eq(2),'count'].sum())))
pd.DataFrame(rows).to_csv(OUT/'gap_route_period.csv',index=False)
# Fit early population, predict July conditional count table. Candidate opportunities are
# visible institutions, visible edges, and one route-level geometric gap draw.
d['period2']=np.where(d.period<'2023-07','early','July')
train=d[d.period2.eq('early')]
for offset in [0,-1,1]:
 total_g=(train.gaps*train['count']).sum(); total_opp=((train.participants+offset)*train['count']).sum()
 q=total_g/(total_opp+total_g) # NB counts failures before r successes.
 p=total_g/total_opp # binomial opportunity model.
 predicted=[]
 for (period,part),g in d.groupby(['period2','participants']):
  n=g['count'].sum();r=part+offset
  for k in range(7):
   observed=int(g.loc[g.gaps.eq(k),'count'].sum())
   nb=math.comb(k+r-1,k)*(1-q)**r*q**k
   bi=(math.comb(r,k)*p**k*(1-p)**(r-k)) if k<=r else 0.
   predicted.append(dict(period=period,participants=int(part),gaps=k,n=int(n),observed=observed,
      nb_expected=n*nb,binomial_expected=n*bi,nb_q=q,binomial_p=p))
 z=pd.DataFrame(predicted);z.to_csv(OUT/f'gap_models_offset_{offset}.csv',index=False)
 # Min expected10 cells Pearson descriptive misfit; many census observations make small errors detectable.
 for period,g in z.groupby('period'):
  for model in ['nb','binomial']:
   valid=g[f'{model}_expected']>=10
   err=((g.loc[valid,'observed']-g.loc[valid,f'{model}_expected'])**2/g.loc[valid,f'{model}_expected']).sum()
   print(dict(offset=offset,model=model,period=period,parameter=q if model=='nb' else p,pearson=float(err),cells=int(valid.sum())),flush=True)
print(pd.DataFrame(rows).to_string(index=False))
