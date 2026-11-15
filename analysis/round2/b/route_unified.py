"""Independent unified participant/route distribution from full-census B numeric cache."""
from pathlib import Path
from collections import Counter
import math,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r');counter=Counter()
for lo in range(0,len(a),200000):
 d=a[lo:lo+200000];late=(d['epoch']>=1688169600).astype('i4')
 key=d['route'].astype('i4')*10000+d['participants'].astype('i4')*100+d['fx'].astype('i4')*2+late
 k,n=np.unique(key,return_counts=True);counter.update(dict(zip(map(int,k),map(int,n))))
rows=[]
for k,n in counter.items():
 route=k//10000;rem=k%10000;p=rem//100;rem%=100;fx=rem//2;period=rem%2
 rows.append(dict(route=['Direct','Indirect','Covered'][route],p=p,fx=fx,period=['early','July'][period],n=n))
d=pd.DataFrame(rows);d.to_csv(OUT/'route_unified_joint.csv',index=False)
early=d[d.period.eq('early')];july=d[d.period.eq('July')]
p_hat=1/(np.average(early.p,weights=early.n)-1)
p_direct=early.loc[early.route.eq('Direct'),'n'].sum()/early.n.sum()
train_non=early[early.p>2];cover=train_non.loc[train_non.route.eq('Covered'),'n'].sum()/train_non.n.sum()
result={'population':int(d.n.sum()),'direct_iff_p2_exceptions':int(d.loc[d.route.eq('Direct').ne(d.p.eq(2)),'n'].sum()),
 'early_geometric_success':float(p_hat),'early_direct_share':float(p_direct),'early_covered_given_non_direct':float(cover),'scores':[]}
cells=[]
for period,g in d.groupby('period'):
 byp=g.groupby('p').n.sum();n=g.n.sum()
 for parameter,name in [(p_hat,'early_MLE'),(1-math.exp(-1),'floor_exp_scale1')]:
  tv=0;pearson=0;used=0
  for p in range(2,max(d.p)+2):
   expected=n*parameter*(1-parameter)**(p-2);observed=int(byp.get(p,0));tv+=abs(expected-observed)
   if expected>=10:pearson+=(observed-expected)**2/expected;used+=1
   cells.append(dict(model=name,period=period,p=p,observed=observed,expected=expected))
  result['scores'].append(dict(model=name,period=period,n=int(n),tv=float(tv/n/2),pearson=float(pearson),cells_expected_ge10=used))
pd.DataFrame(cells).to_csv(OUT/'route_unified_participant_cells.csv',index=False)
trainmaps={}
for keys,name in [(['p'],'p'),(['p','fx'],'p_fx')]:
 tab=train_non.groupby(keys+['route']).n.sum().unstack('route',fill_value=0)
 estimates=(tab.get('Covered',0)+100*cover)/(tab.sum(axis=1)+100)
 trainmaps[name]=estimates.to_dict()
for model in ['constant','p','p_fx']:
 nll=total=0
 for row in july[july.p>2].itertuples():
  prob=cover if model=='constant' else trainmaps[model].get(row.p if model=='p' else (row.p,row.fx),cover)
  nll-=row.n*math.log(prob if row.route=='Covered' else 1-prob);total+=row.n
 result['scores'].append(dict(model='covered_'+model,period='July',n=total,bernoulli_nll=nll/total))
condition=d[d.p>2].groupby(['period','p','fx','route']).n.sum().unstack('route',fill_value=0).reset_index()
condition['covered_rate']=condition.Covered/(condition.Covered+condition.Indirect)
condition.to_csv(OUT/'covered_conditional.csv',index=False)
(OUT/'route_unified_initial.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
