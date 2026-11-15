"""Independent timing models from shared exact full-file timing counts."""
from pathlib import Path
import pandas as pd,numpy as np,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(ROOT/'analysis/round2/b/timing_counts.csv',keep_default_na=False)
train=d[d.period.eq('MayJune')];test=d[d.period.eq('July')]
exposures={}
for period,start,end in [('MayJune','2023-05-01','2023-06-30'),('July','2023-07-01','2023-07-30')]:
 ex=pd.date_range(start,end,freq='D').dayofweek.value_counts().sort_index().to_numpy()
 exposures[period]=ex.astype(float)
weekday=train.groupby('weekday').n.sum().reindex(range(7),fill_value=0).to_numpy()/exposures['MayJune']
dayflat=np.array([weekday[:5].mean()]*5+[weekday[5:].mean()]*2)
hour=train.groupby('hour').n.sum().reindex(range(24),fill_value=0).to_numpy()+.5
country_hours={}
for country,g in train.groupby('sender_country_code'):
 country_hours[country]=g.groupby('hour').n.sum().reindex(range(24),fill_value=0).to_numpy()+.5
party_hours={}
for (country,party),g in train.groupby(['sender_country_code','party']):
 party_hours[(country,party)]=g.groupby('hour').n.sum().reindex(range(24),fill_value=0).to_numpy()+.5
country_days={}
for country,g in train.groupby('sender_country_code'):
 country_days[country]=(g.groupby('weekday').n.sum().reindex(range(7),fill_value=0).to_numpy()+.5)/exposures['MayJune']
joint={}
for (country,party),g in train.groupby(['sender_country_code','party']):
 mat=np.zeros((7,24))+.5
 for r in g.itertuples():mat[r.weekday,r.hour]+=r.n
 joint[(country,party)]=mat/exposures['MayJune'][:,None]
def distribution(model,country,party):
 h=hour;day=weekday
 if model=='uniform':h=np.ones(24);day=np.ones(7)
 if model=='weekend_multiplier_pooled_hour':day=dayflat
 if model in ['country_hour','country_hour_day','country_party_hour','joint_country_party']:
  h=country_hours.get(country,hour)
 if model in ['country_party_hour','joint_country_party']:h=party_hours.get((country,party),h)
 if model=='country_hour_day':day=country_days.get(country,weekday)
 if model=='joint_country_party' and (country,party) in joint:
  mat=joint[(country,party)]*exposures['July'][:,None]
 else:mat=np.outer(day*exposures['July'],h)
 return mat/mat.sum()
models=['uniform','weekend_multiplier_pooled_hour','pooled_hour_day','country_hour','country_party_hour','country_hour_day','joint_country_party']
rows=[];strata=[];unknown=0
for (country,party),g in test.groupby(['sender_country_code','party']):
 obs=np.zeros((7,24))
 for r in g.itertuples():obs[r.weekday,r.hour]+=r.n
 n=int(obs.sum())
 if country not in country_hours:unknown+=n
 for model in models:
  pred=distribution(model,country,party)
  nll=float(-(obs*np.log(pred)).sum());tv=.5*float(np.abs(obs/n-pred).sum())
  strata.append([country,party,model,n,nll,tv])
s=pd.DataFrame(strata,columns=['sender_country_code','party','model','n','nll_total','total_variation'])
s.to_csv(OUT/'timing_model_strata.csv',index=False)
for model,g in s.groupby('model'):
 rows.append([model,int(g.n.sum()),float(g.nll_total.sum()/g.n.sum()),float(np.average(g.total_variation,weights=g.n))])
scores=pd.DataFrame(rows,columns=['model','July_n','July_nll_nats','weighted_total_variation'])
scores.to_csv(OUT/'timing_model_scores.csv',index=False)
rates=[]
for (party,period),g in d.groupby(['party','period']):
 counts=g.groupby('weekday').n.sum().reindex(range(7),fill_value=0).to_numpy();rate=counts/exposures[period]
 for day in range(7):rates.append([party,period,day,int(counts[day]),int(exposures[period][day]),float(rate[day])])
pd.DataFrame(rates,columns=['party','period','weekday','n','calendar_days','daily_rate']).to_csv(OUT/'timing_exposure_rates.csv',index=False)
profiles=[]
for country,h in country_hours.items():
 n=int(train.loc[train.sender_country_code.eq(country),'n'].sum())
 for hourid,v in enumerate(h):profiles.append([country,hourid,n,float(v/h.sum())])
pd.DataFrame(profiles,columns=['sender_country_code','hour_utc','train_n','hour_share']).to_csv(OUT/'timing_sender_hour_profiles.csv',index=False)
print(scores.to_string(index=False));print('Unknown sender code July records',unknown)
print('Exposure MayJune',exposures['MayJune'],'July',exposures['July'])
print('Pooled weekday daily rates',weekday,'weekend/weekday',weekday[5:].mean()/weekday[:5].mean())
print('Full weekday variation weekdays max/min',weekday[:5].max()/weekday[:5].min())
print('Shared B extraction; conditional scheduling validation, no local-hour/countryeconomic inference.')
