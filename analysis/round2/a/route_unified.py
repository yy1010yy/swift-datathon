"""Independent unified participant length/routing-label candidate tests."""
from pathlib import Path
import numpy as np,pandas as pd,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(OUT/'routing_joint.csv');d['period']=np.where(d.month.eq('2023-07'),'july','early')
fit=[];cells=[]
for period,g in d.groupby('period'):
 n=int(g.n.sum());mean=np.average(g.p,weights=g.n);success=1/(mean-1);direct=int(g.loc[g.route.eq(0),'n'].sum())
 fit.append([period,n,mean,success,direct/n,direct/n-success,int(g.loc[g.route.eq(0).ne(g.p.eq(2)),'n'].sum())])
 if period=='early':early_success=success;early_covered=float(g.loc[g.route.eq(2),'n'].sum()/g.loc[g.route.gt(0),'n'].sum())
for period,g in d.groupby('period'):
 n=int(g.n.sum())
 for p in range(2,12):
  obs=int(g.loc[g.p.eq(p),'n'].sum());exp=n*early_success*(1-early_success)**(p-2)
  cells.append([period,p,obs,exp])
 obs=int(g.loc[g.p.ge(12),'n'].sum());exp=n*(1-early_success)**10
 cells.append([period,12,obs,exp])
pd.DataFrame(fit,columns=['period','n','mean_participants','geometric_success_MLE','Direct_share','share_minus_MLE','Direct_iff_p2_violations']).to_csv(OUT/'route_unified_fit.csv',index=False)
pd.DataFrame(cells,columns=['period','p_or_12plus','observed','expected_early_geometric']).to_csv(OUT/'route_unified_length_cells.csv',index=False)
rows=[]
for groupcols in [['period','p'],['period','p','fx'],['month','p','fx']]:
 for key,g in d[d.route.gt(0)].groupby(groupcols):
  n=int(g.n.sum());covered=int(g.loc[g.route.eq(2),'n'].sum())
  rows.append(['+'.join(groupcols),str(key),n,covered,covered/n,n*early_covered])
tab=pd.DataFrame(rows,columns=['grouping','cell','n','covered','covered_share','expected_constant_covered'])
tab.to_csv(OUT/'route_unified_covered_cells.csv',index=False)
print(pd.DataFrame(fit,columns=['period','n','mean_p','geom_success','Direct_share','difference','violations']).to_string(index=False))
print('EarlyCoveredprobconditionalNonDirect',early_covered)
for grouping in tab.grouping.unique():
 t=tab[(tab.grouping==grouping)&tab.n.ge(1000)];ex=t.expected_constant_covered;v=ex*(1-early_covered)
 print(grouping,'cells>=1000',len(t),'Coveredshare range',t.covered_share.min(),t.covered_share.max(),'Pearsonconstantprob',float(((t.covered-ex)**2/v).sum()))
print('CoveredFXshares pooled',d[d.route.gt(0)].groupby('fx').apply(lambda z:z.loc[z.route.eq(2),'n'].sum()/z.n.sum()).to_dict())
print('Geometric is observationally equivalent to floor exponential for matching rate; does not recover actual sampling call.')
