"""Full-census amount heaping by currency from cache, excluding recorded labels."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
currencies=sorted(json.loads((ROOT/'outputs/cleaned/profile.json').read_text())['category_counts']['currency_code'])
rows=[];top=[]
for i,code in enumerate(currencies):
 j=np.flatnonzero((a['currency']==i)&(a['labeled']==0));v=a['amount'][j]; cents=np.rint(v*100).astype('i8')
 if not len(v):continue
 for party in range(4):
  for late in [False,True]:
   mask=(a['party'][j]==party)&((a['epoch'][j]>=1688169600)==late);c=cents[mask]
   if len(c):rows.append(dict(currency=code,party=['BB','BC','CB','CC'][party],period='July' if late else 'early',n=len(c),integer_n=int((c%100==0).sum()),round100_n=int((c%10000==0).sum()),round1000_n=int((c%100000==0).sum())))
 if len(v)>=10000:
  values,counts=np.unique(cents,return_counts=True);order=np.argsort(counts)[-15:][::-1]
  for k in order:top.append(dict(currency=code,usd_amount=values[k]/100,n=int(counts[k]),currency_n=len(v)))
pd.DataFrame(rows).to_csv(OUT/'rounding_currency_party_period.csv',index=False)
pd.DataFrame(top).to_csv(OUT/'frequent_amounts_currency.csv',index=False)
z=pd.DataFrame(rows).groupby('currency')[['n','integer_n','round100_n','round1000_n']].sum()
z['integer_share']=z.integer_n/z.n;print(z.sort_values('n',ascending=False).head(15).to_string())
print(pd.DataFrame(top).query("currency in ['USD','EUR','GBP','CNY']").to_string(index=False))
