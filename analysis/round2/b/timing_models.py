"""Blind B exposure-aware UTC timing model comparison on own full-census counts.

Train complete May1–June30 dates; evaluate July1–30. July counts per sender-code/party
stratum condition the comparison: this tests within-stratum timing, not country volumes.
No geography/timezone mapping is used. Dirichlet168pseudo-counts toward global train
distribution smooth sparse stratum cells, fixed before observing July model scores.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
d=pd.read_csv(OUT/'timing_counts.csv',keep_default_na=False)
train=d[d.period.eq('MayJune')];test=d[d.period.eq('July')]
days_train=np.bincount(pd.date_range('2023-05-01','2023-06-30').day_of_week,minlength=7).astype(float)
days_test=np.bincount(pd.date_range('2023-07-01','2023-07-30').day_of_week,minlength=7).astype(float)
def tensor(g):
 a=np.zeros((7,24))
 for r in g.itertuples():a[r.weekday,r.hour]+=r.n
 return a
global_count=tensor(train);prior=global_count/global_count.sum()
def normalized(v):return v/v.sum()
def julyprob(count,mode):
 rates=count/days_train[:,None]
 if mode=='full':v=rates*days_test[:,None]
 else:
  hour=count.sum(axis=0)/count.sum();daily=rates.sum(axis=1)
  if mode=='weekend':daily=np.r_[np.repeat(daily[:5].mean(),5),np.repeat(daily[5:].mean(),2)]
  v=daily[:,None]*hour[None,:]*days_test[:,None]
 return normalized(v)
globalpred={f'global_{mode}':julyprob(global_count,mode) for mode in ['weekend','weekday','full']}
globalpred['calendar_uniform']=normalized(np.repeat(days_test[:,None],24,axis=1))
grouptrain={key:tensor(g) for key,g in train.groupby(['sender_country_code','party'])}
countrytrain={key:tensor(g) for key,g in train.groupby('sender_country_code')}
partytrain={key:tensor(g) for key,g in train.groupby('party')}
scores=[];cells=[]
for key,g in test.groupby(['sender_country_code','party']):
 observed=tensor(g);n=observed.sum();country,party=key
 count=grouptrain.get(key,np.zeros((7,24)));known=count.sum()>0
 smooth=count+168*prior
 predictions=dict(globalpred)
 predictions['sender_only_full']=julyprob(countrytrain.get(country,np.zeros((7,24)))+168*prior,'full')
 predictions['party_only_full']=julyprob(partytrain[party]+168*prior,'full')
 predictions.update({f'sender_party_{mode}':julyprob(smooth,mode) for mode in ['weekend','weekday','full']})
 for model,prob in predictions.items():
  nll=float(-np.sum(observed*np.log(prob))/n)
  tv=float(np.abs(observed/n-prob).sum()/2)
  scores.append(dict(sender_country_code=country,party=party,model=model,n=int(n),train_n=int(count.sum()),known=known,nll=nll,tv=tv))
  if model in ['global_weekend','sender_party_weekend','sender_party_full']:
   for weekday in range(7):
    for hour in range(24):cells.append(dict(sender_country_code=country,party=party,model=model,weekday=weekday,hour=hour,observed=int(observed[weekday,hour]),predicted=float(n*prob[weekday,hour])))
s=pd.DataFrame(scores);s.to_csv(OUT/'timing_model_strata.csv',index=False)
summary=[]
for (model,party),g in s.groupby(['model','party']):
 summary.append(dict(model=model,party=['BB','BC','CB','CC'][party],n=int(g.n.sum()),strata=len(g),unknown_n=int(g.loc[~g.known,'n'].sum()),
  july_nll=float(np.average(g.nll,weights=g.n)),july_tv_weighted=float(np.average(g.tv,weights=g.n))))
for model,g in s.groupby('model'):
 summary.append(dict(model=model,party='ALL',n=int(g.n.sum()),strata=len(g),unknown_n=int(g.loc[~g.known,'n'].sum()),
  july_nll=float(np.average(g.nll,weights=g.n)),july_tv_weighted=float(np.average(g.tv,weights=g.n))))
z=pd.DataFrame(summary);z.to_csv(OUT/'timing_model_scores.csv',index=False)
pd.DataFrame(cells).to_csv(OUT/'timing_model_cells.csv',index=False)
print(z.to_string(index=False))
print('Train weekday exposures:',days_train.tolist(),'July:',days_test.tolist())
(OUT/'timing_model_manifest.json').write_text(json.dumps({'train_rows':int(train.n.sum()),'july_rows':int(test.n.sum()),
 'calendar_train':'May1–June30 UTC complete dates','calendar_test':'July1–30 UTC complete dates',
 'conditioning':'July sender-code/party totals held fixed; no volume forecasts',
 'smoothing_pseudocounts':168,'no_external_timezones':True,'no_iid_significance_claim':True},indent=2))
