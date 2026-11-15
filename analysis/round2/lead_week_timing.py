"""Test a week-volume × weekday-profile construction on the 13 complete weeks.

Uses B's full numeric cache. No external calendar, holiday or timezone data is used.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
a=np.load(ROOT/'outputs/eda_round2/b_rows.npy',mmap_mode='r')
start=np.datetime64('2023-05-01','D').astype('int64')
day=(a['epoch']//86400).astype('int64')-start
keep=(day>=0)&(day<91)
day=day[keep];party=a['party'][keep].astype('int64')
daily=np.bincount(day,minlength=91).reshape(13,7)
weekly=daily.sum(axis=1);weekday=daily.sum(axis=0);total=int(daily.sum())
expected=weekly[:,None]*weekday[None,:]/total
residual=(daily-expected)/np.sqrt(expected)
relative=daily/expected-1

party_daily=np.zeros((4,13,7),dtype='int64')
for p in range(4):party_daily[p]=np.bincount(day[party==p],minlength=91).reshape(13,7)
party_totals=party_daily.sum(axis=(1,2));expected_party=party_totals[:,None,None]*daily[None,:,:]/total
party_z=(party_daily-expected_party)/np.sqrt(expected_party)

dates=pd.date_range('2023-05-01',periods=91,freq='D',tz='UTC')
rows=[]
for w in range(13):
 for wd in range(7):
  rows.append(dict(date=str(dates[w*7+wd].date()),week=w+1,weekday=wd,
    records=int(daily[w,wd]),expected_independent=float(expected[w,wd]),
    standardized_residual=float(residual[w,wd]),relative_error=float(relative[w,wd])))
pd.DataFrame(rows).to_csv(OUT/'timing_week_day_factorization.csv',index=False)
pd.DataFrame({'week':range(1,14),'records':weekly,
 'share':weekly/total,'weekday_equivalent_volume':weekly/7}).to_csv(OUT/'timing_week_volumes.csv',index=False)
pd.DataFrame({'weekday':range(7),'records':weekday,'probability':weekday/total,
 'relative_to_wednesday':weekday/weekday[2]}).to_csv(OUT/'timing_weekday_profile.csv',index=False)
result={'status':'complete','rows':total,'weeks':13,'dates':'2023-05-01 through 2023-07-30 UTC',
 'week_totals':weekly.tolist(),'weekday_probabilities':(weekday/total).tolist(),
 'week_weekday_factorization':{'max_abs_relative_error':float(abs(relative).max()),
   'rmse_relative_error':float(np.sqrt(np.average(relative**2,weights=expected))),
   'max_abs_standardized_residual':float(abs(residual).max()),
   'pearson_chi_square':float((residual**2).sum()),'degrees_of_freedom':72},
 'party_given_day_factorization':{'max_abs_relative_error':float(abs(party_daily/expected_party-1).max()),
   'max_abs_standardized_residual':float(abs(party_z).max()),
   'pearson_chi_square':float((party_z**2).sum()),'degrees_of_freedom':270},
 'interpretation':'Weekly volume and weekday profile are nearly separable; assess residual scale before calling it an exact independent sampler.',
 'limits':['B numeric cache is shared extraction; lead aggregation independent.',
  'Only 13 observed weeks; weekly-volume distribution is weakly identified.',
  'No external holidays, timezones, or economic calendars used.']}
(OUT/'timing_week_factorization.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
