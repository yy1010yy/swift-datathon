"""Own endpoint recalculation and exact reconciliation to original independent B scan."""
from pathlib import Path
import math,json
import pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
a=pd.read_csv(OUT/'routing_joint.csv');b=pd.read_csv(ROOT/'analysis/reviews/b/joint_counts.csv')
a['period']=np.where(a.month.eq('2023-07'),'late','early')
a['route_name']=a.route.map({0:'Direct',1:'Indirect',2:'Covered'})
a['continuity']=a.q.map({0:'N',1:'Y'})
aa=a.groupby(['period','route_name','continuity','sm','rm']).n.sum().sort_index()
bb=b.groupby(['period','route','continuity','sender_mismatch','receiver_mismatch']).n.sum().sort_index()
assert aa.index.to_list()==bb.index.to_list();assert np.array_equal(aa.to_numpy(),bb.to_numpy())
rows=[]
for key,g in a.groupby(['month','route_name','continuity']):
 cells=np.zeros((2,2),dtype='int64')
 for r in g.itertuples():cells[r.sm,r.rm]+=r.n
 n=int(cells.sum());expected=np.outer(cells.sum(axis=1),cells.sum(axis=0))/n
 chi=float(np.divide((cells-expected)**2,expected,out=np.zeros_like(expected),where=expected>0).sum())
 phi=math.sqrt(chi/n)
 rows.append(list(key)+[n,cells[1].sum()/n,cells[:,1].sum()/n,int(cells[1,1]),float(expected[1,1]),phi,chi])
table=pd.DataFrame(rows,columns=['month','route','continuity','n','sender_rate','receiver_rate','both','both_expected','absolute_phi','pearson_independence'])
table.to_csv(OUT/'endpoint_independent_strata.csv',index=False)
large=table[table.n>=5000];early=table[table.month.ne('2023-07')];july=table[table.month.eq('2023-07')]
print('PASS exact A/B endpoint jointcounts across period/route/continuity,10M records.')
print('Large strata',len(large),'maxabsphi',float(large.absolute_phi.max()),'sender range',large.sender_rate.min(),large.sender_rate.max(),'receiver range',large.receiver_rate.min(),large.receiver_rate.max())
print('Pearson sum across allstrata',table.pearson_independence.sum(),'acrosslarge',large.pearson_independence.sum())
print('Finitepopulation association diagnostic, not a test proving randomgeneration or causalorder.')
print(table.to_string(index=False))
