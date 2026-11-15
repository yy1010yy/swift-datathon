"""Summarize saved independent full-census B results, without reading other reviewers."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
amount=pd.read_csv(OUT/'amount_unlabeled_currency_party_period.csv')
pair=[]
for (currency,period),g in amount.groupby(['currency','period']):
 t=g.set_index('party')
 for top,base in [('BB','BC'),('BB','CB'),('BC','CC'),('CB','CC')]:
  if top in t.index and base in t.index and min(t.loc[top,'n'],t.loc[base,'n'])>=1000:
   pair.append(dict(currency=currency,period=period,contrast=top+'/'+base,numerator_n=int(t.loc[top,'n']),denominator_n=int(t.loc[base,'n']),median_ratio=t.loc[top,'median']/t.loc[base,'median'],log_mean_shift=t.loc[top,'log_mean']-t.loc[base,'log_mean'],log_sd_difference=t.loc[top,'log_sd']-t.loc[base,'log_sd']))
z=pd.DataFrame(pair);z.to_csv(OUT/'amount_conditional_ratios.csv',index=False)
print('Within-currency customer role contrasts (cells at least1000 rows each):')
print(z.groupby(['contrast','period']).agg(cells=('currency','size'),median_ratio=('median_ratio','median'),median_log_shift=('log_mean_shift','median'),min_log_shift=('log_mean_shift','min'),max_log_shift=('log_mean_shift','max')).to_string())
t=pd.read_csv(OUT/'timing_counts.csv')
calendar=[]
for per,lo,hi in [('MayJune','2023-05-01','2023-06-30'),('July','2023-07-01','2023-07-30')]:
 days=pd.date_range(lo,hi); counts=days.day_of_week.value_counts().to_dict()
 for weekday,n in counts.items():calendar.append(dict(period=per,weekday=weekday,days=n))
c=pd.DataFrame(calendar);t=t.merge(c,on=['period','weekday'],how='left');t['per_day']=t.n/t.days
weekday=t.groupby(['party','period','weekday'])[['n','per_day']].sum().reset_index()
weekday.to_csv(OUT/'weekday_rates.csv',index=False)
r=[]
for (party,period),g in weekday.groupby(['party','period']):
 weekday_mean=g.loc[g.weekday<5,'per_day'].mean();weekend_mean=g.loc[g.weekday>=5,'per_day'].mean()
 r.append(dict(party=['BB','BC','CB','CC'][party],period=period,weekend_to_weekday=weekend_mean/weekday_mean,n=int(g.n.sum())))
print('\nExposure-corrected weekend/weekday daily-rate ratio:',pd.DataFrame(r).to_string(index=False))
hours=t.groupby(['party','period','hour']).n.sum().reset_index();hours.to_csv(OUT/'hour_party.csv',index=False)
country=t.groupby(['sender_country_code','party','period','hour']).n.sum().reset_index()
modes=country.loc[country.groupby(['sender_country_code','party','period']).n.idxmax()]
modes.to_csv(OUT/'country_hour_modes.csv',index=False)
# Country/currency share association remains a descriptive country corridor result.
d=pd.read_csv(OUT/'currency_counts.csv',keep_default_na=False)
agg=d.groupby(['sender_country_code','receiver_country_code','party','period']).n.sum().rename('total')
d=d.join(agg,on=['sender_country_code','receiver_country_code','party','period']);d['share']=d.n/d.total
modes=d.loc[d.groupby(['sender_country_code','receiver_country_code','party','period']).n.idxmax()]
modes.to_csv(OUT/'currency_corridor_modes.csv',index=False)
print('\nTiming and currency tables saved; no local-hour or individual-bank-pair mechanism inferred.')
