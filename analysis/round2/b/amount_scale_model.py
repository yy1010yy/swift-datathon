"""Weighted log-amount fixed-currency role models from exact unlabeled moments."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
d=pd.read_csv(OUT/'amount_unlabeled_currency_party_period.csv',keep_default_na=False)
currencies=sorted(d.currency.unique()); cmap={v:i for i,v in enumerate(currencies)}
def xmatrix(z,interaction):
 x=np.zeros((len(z),len(currencies)+2+interaction))
 x[np.arange(len(z)),z.currency.map(cmap).to_numpy()]=1
 x[:,-2-interaction]=(z.party.str[0]=='B').astype(float)
 x[:,-1-interaction]=(z.party.str[1]=='B').astype(float)
 if interaction:x[:,-1]=(z.party=='BB').astype(float)
 return x
results=[]
for interaction in [False,True]:
 tr=d[d.period.eq('early')];x=xmatrix(tr,interaction);w=np.sqrt(tr.n.to_numpy())
 coef=np.linalg.lstsq(x*w[:,None],tr.log_mean.to_numpy()*w,rcond=None)[0]
 params={'sender_business_log_shift':float(coef[-2-int(interaction)]),'receiver_business_log_shift':float(coef[-1-int(interaction)])}
 if interaction:params['business_both_interaction']=float(coef[-1])
 params.update({k.replace('_log_shift','_factor'):float(np.exp(v)) for k,v in list(params.items()) if k.endswith('_log_shift')})
 for period,g in d.groupby('period'):
  pred=xmatrix(g,interaction)@coef;actual=g.log_mean.to_numpy();n=g.n.to_numpy();mean=np.average(actual,weights=n)
  sse=np.sum(n*(g.log_sd.to_numpy()**2+(actual-pred)**2))
  sst=np.sum(n*(g.log_sd.to_numpy()**2+(actual-mean)**2))
  results.append(dict(model='currency_sender_receiver'+('_interaction' if interaction else ''),period=period,n=int(n.sum()),r2_log_amount=float(1-sse/sst),rmse_log_amount=float(np.sqrt(sse/n.sum())),params=params))
(OUT/'amount_scale_models.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
