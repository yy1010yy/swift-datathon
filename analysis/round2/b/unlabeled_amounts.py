"""Exact conditional amount quantiles for no-recorded-label controls, from full census cache."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
profile=json.loads((ROOT/'outputs/cleaned/profile.json').read_text())
currencies=sorted(profile['category_counts']['currency_code']); parties=['BB','BC','CB','CC']
period=(a['epoch']>=1688169600).astype('u1')
j=np.flatnonzero(a['labeled']==0)
assert len(j)==9992994
group=a['currency'][j].astype('i4')*8+a['party'][j]*2+period[j]
order=np.argsort(group,kind='stable'); j=j[order];sg=group[order]
bound=np.r_[0,np.flatnonzero(np.diff(sg))+1,len(sg)]
rows=[]
for lo,hi in zip(bound[:-1],bound[1:]):
 ix=j[lo:hi];key=int(sg[lo]);v=a['amount'][ix];log=np.log(v)
 q=np.quantile(v,[.01,.1,.5,.9,.99])
 rows.append(dict(currency=currencies[key//8],party=parties[(key%8)//2],period=['early','July'][key%2],
   n=len(v),q01=q[0],q10=q[1],median=q[2],q90=q[3],q99=q[4],log_mean=log.mean(),log_sd=log.std(),mean=v.mean()))
z=pd.DataFrame(rows);z.to_csv(OUT/'amount_unlabeled_currency_party_period.csv',index=False)
print('No-recorded-label conditional quantile denominator:',int(z.n.sum()))
global_rows=[]
for party,pname in enumerate(parties):
 for per,pername in enumerate(['early','July']):
  v=a['amount'][(a['party']==party)&(period==per)&(a['labeled']==0)];log=np.log(v)
  q=np.quantile(v,[.01,.1,.5,.9,.99]); cents=np.rint(v*100).astype('i8')
  global_rows.append(dict(party=pname,period=pername,n=len(v),q01=q[0],q10=q[1],median=q[2],q90=q[3],q99=q[4],log_mean=log.mean(),log_sd=log.std(),mean=v.mean(),integer_dollar_n=int((cents%100==0).sum())))
zz=pd.DataFrame(global_rows);zz.to_csv(OUT/'amount_unlabeled_party_period.csv',index=False)
print(zz.to_string(index=False))
