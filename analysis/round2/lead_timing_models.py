"""Fit timing rules on complete May-June dates and evaluate complete July dates.

Input is B's independently extracted full-population timing count table. This script
does not use external timezone/country data. Country-like values are BIC characters 5-6.
"""
from pathlib import Path
import json, math
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parent
d=pd.read_csv(BASE/'b/timing_counts.csv',keep_default_na=False)
assert d.n.sum()==9991528  # May 1 through July 30; partial boundary dates excluded.
exposure={'MayJune':{0:9,1:9,2:9,3:9,4:9,5:8,6:8},
          'July':{0:4,1:4,2:4,3:4,4:4,5:5,6:5}}
party_names={0:'BB',1:'BC',2:'CB',3:'CC'}

def normalized_daily_rates(frame, period, group):
    z=frame.groupby(group+['weekday']).n.sum().reset_index()
    z['daily_rate']=z.n/z.weekday.map(exposure[period])
    z['probability']=z.daily_rate/(z.groupby(group).daily_rate.transform('sum') if group else z.daily_rate.sum())
    return z

# Common weekday schedule: compare party-specific daily-rate distributions.
week=[]
for period in ['MayJune','July']:
    z=normalized_daily_rates(d[d.period.eq(period)],period,['party'])
    z['period']=period;week.append(z)
week=pd.concat(week,ignore_index=True)
week['party_name']=week.party.map(party_names)
week.to_csv(BASE/'timing_weekday_probabilities.csv',index=False)
wide=week.pivot_table(index=['period','weekday'],columns='party_name',values='probability')
wide['range_across_party']=wide.max(axis=1)-wide.min(axis=1)
wide.reset_index().to_csv(BASE/'timing_weekday_party_spread.csv',index=False)

# Train a single May-June weekday rate and evaluate July; party-specific alternative.
early=d[d.period.eq('MayJune')];july=d[d.period.eq('July')]
global_week=normalized_daily_rates(early,'MayJune',[]).set_index('weekday').probability
party_week=normalized_daily_rates(early,'MayJune',['party']).set_index(['party','weekday']).probability
actual_week=normalized_daily_rates(july,'July',[]).set_index('weekday').probability
weekday_rows=[]
for w in range(7):
    weekday_rows.append(dict(weekday=w,early_probability=global_week[w],
      july_probability=actual_week[w],ratio_july_to_early=actual_week[w]/global_week[w]))
pd.DataFrame(weekday_rows).to_csv(BASE/'timing_weekday_temporal.csv',index=False)

# Hour models. Model P uses party only. Model CP uses sender code+party with a
# declared 100-record shrinkage toward the party profile; sensitivity is also scored.
def hour_counts(frame, groups):
    z=frame.groupby(groups+['hour']).n.sum().unstack(fill_value=0)
    return z.reindex(columns=range(24),fill_value=0)
early_party=hour_counts(early,['party'])
july_party=hour_counts(july,['party'])
early_cp=hour_counts(early,['sender_country_code','party'])
july_cp=hour_counts(july,['sender_country_code','party'])
party_prob=early_party.div(early_party.sum(axis=1),axis=0)

def score(alpha):
    total_ll_party=total_ll_cp=total_n=0.; rows=[]
    for key, obs in july_cp.iterrows():
        country,party=key;n=float(obs.sum())
        if key not in early_cp.index or n==0:continue
        tr=early_cp.loc[key].to_numpy(float); base=party_prob.loc[party].to_numpy(float)
        pp=np.maximum(base,1e-300)
        cp=(tr+alpha*base)/(tr.sum()+alpha)
        llp=float((obs.to_numpy()*np.log(pp)).sum());llc=float((obs.to_numpy()*np.log(cp)).sum())
        total_ll_party+=llp;total_ll_cp+=llc;total_n+=n
        rows.append(dict(sender_country_code=country,party=party,early_n=int(tr.sum()),july_n=int(n),
            nll_party=-llp/n,nll_country_party=-llc/n,improvement_nats=(llc-llp)/n,
            early_mode=int(np.argmax(tr)),july_mode=int(np.argmax(obs.to_numpy())),
            circular_mode_difference=int(min((np.argmax(tr)-np.argmax(obs.to_numpy()))%24,
                                             (np.argmax(obs.to_numpy())-np.argmax(tr))%24))))
    return dict(alpha=alpha,n=int(total_n),party_nll=-total_ll_party/total_n,
                country_party_nll=-total_ll_cp/total_n,
                improvement_nats=(total_ll_cp-total_ll_party)/total_n),pd.DataFrame(rows)
scores=[]
for alpha in [10,100,1000]:
    result,rows=score(alpha);scores.append(result)
    if alpha==100:rows.to_csv(BASE/'timing_country_party_validation.csv',index=False)
pd.DataFrame(scores).to_csv(BASE/'timing_hour_model_scores.csv',index=False)

# Stable-cell summaries, stated separately from all-row predictive scores.
stable=rows[(rows.early_n>=1000)&(rows.july_n>=500)].copy()
mode_share=(stable.circular_mode_difference<=1).mean()
weighted_mode_share=np.average(stable.circular_mode_difference<=1,weights=stable.july_n)
result={'status':'complete','source_rows':int(d.n.sum()),'MayJune_rows':int(early.n.sum()),
 'July_rows':int(july.n.sum()),'complete_dates':'2023-05-01 through 2023-07-30 UTC',
 'weekday_max_party_probability_range':float(wide.range_across_party.max()),
 'weekday_max_temporal_ratio_change':float(max(abs(pd.DataFrame(weekday_rows).ratio_july_to_early-1))),
 'hour_model_scores':scores,'stable_country_party_cells':len(stable),
 'stable_cells_mode_within_1_hour_fraction':float(mode_share),
 'stable_rows_mode_within_1_hour_fraction':float(weighted_mode_share),
 'limits':['UTC profiles only; no external timezone mapping.',
  'Country-party model uses observed BIC country substring and smoothing chosen before score inspection.',
  'May-June and July are retrospective development/check periods from one synthetic population.',
  'Hour model does not yet condition on individual bank or corridor.']}
(BASE/'timing_model_summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
print('\nWeekday probabilities by party/period:\n',week.to_string(index=False))
