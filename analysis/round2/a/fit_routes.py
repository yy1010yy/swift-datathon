"""Candidate distribution fits to previous full-file route census (provenance explicit)."""
from pathlib import Path
import math,json
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
a=pd.read_csv(ROOT/'analysis/reviews/a/route_counts.csv')
a['period']=a.period.map(lambda v:'early' if v<'2023-07' else 'july')
summaries=[];cells=[]
for (period,route),g in a.groupby(['period','route']):
 n=int(g['count'].sum()); pmean=np.average(g.participants,weights=g['count']);gapmean=np.average(g.gaps,weights=g['count'])
 # For sum of geometric failures over p-1 edges, MLE failure probability.
 r=float(((g.participants-1)*g['count']).sum()); failures=float((g.gaps*g['count']).sum())
 alpha=failures/(r+failures)
 # Length: floor(exponential(scale≈1))+3 for non-direct (a discrete geometric tail).
 lengthq=None if route=='Direct' else 1/(1+(pmean-3))
 summaries.append([period,route,n,pmean,gapmean,alpha,lengthq])
 for p,pg in g.groupby('participants'):
  pn=int(pg['count'].sum())
  for k in range(int(pg.gaps.max())+1):
   actual=int(pg.loc[pg.gaps.eq(k),'count'].sum())
   expected=pn*math.comb(k+int(p)-2,k)*(.95**(int(p)-1))*(.05**k)
   cells.append([period,route,p,k,pn,actual,expected])
pd.DataFrame(summaries,columns=['period','route','n','mean_participants','mean_gaps','gap_failure_mle','length_geom_success_mle']).to_csv(OUT/'route_distribution_fit.csv',index=False)
pd.DataFrame(cells,columns=['period','route','participants','gaps','stratum_n','observed','expected_nb_005']).to_csv(OUT/'gap_model_cells.csv',index=False)
print(pd.DataFrame(summaries,columns=['period','route','n','mean_participants','mean_gaps','gap_failure_mle','length_geom_success_mle']).to_string(index=False))
print('These fits use the prior independently produced full-file A route census, not a new independent gap scan.')
