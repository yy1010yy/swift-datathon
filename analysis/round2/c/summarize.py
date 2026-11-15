"""Postprocess independent C outputs; no new raw-data read."""
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent
e=pd.read_csv(P/'history_tests.csv',keep_default_na=False)
e['period']=np.where(e.epoch_seconds<1688169600,'pre_july','july')
e['history_depth']=pd.cut(e.prior_same_pair_currency,[-1,0,1,5,np.inf],labels=['none','one','2-5','6+'])
rows=[]
for key,g in e.groupby(['label','party_pair','period','history_depth'],observed=True):
    rows.append(dict(zip(['label','party_pair','period','history_depth'],key))|dict(n=len(g),
        exact=int(g.same_amount_prior.gt(0).sum()),power10=int(g.power10_prior.gt(0).sum())))
pd.DataFrame(rows).to_csv(P/'history_strata.csv',index=False)
print('HISTORY SUMMARY (all labels, same-pair controls):')
print(pd.read_csv(P/'history_summary.csv',keep_default_na=False).to_string(index=False))
print('\nLABEL PARTY COUNTS:')
print(pd.read_csv(P/'label_party.csv',keep_default_na=False).to_string(index=False))
q=pd.read_csv(P/'amount_quantiles.csv',keep_default_na=False)
q=q[q.labelled.eq(False)]
effects=[]
for (currency,period),g in q.groupby(['currency','period']):
    v=g.set_index('party_pair')
    for left,right,label in [('BB','BC','business_receiver_given_B_sender'),
                            ('CB','CC','business_receiver_given_C_sender'),
                            ('BB','CB','business_sender_given_B_receiver'),
                            ('BC','CC','business_sender_given_C_receiver')]:
        if left in v.index and right in v.index:
            effects.append(dict(currency=currency,period=period,comparison=label,
               n_left=int(v.loc[left,'n']),n_right=int(v.loc[right,'n']),
               log_mean_difference=v.loc[left,'mean_log']-v.loc[right,'mean_log'],
               median_ratio=v.loc[left,'median']/v.loc[right,'median']))
effects=pd.DataFrame(effects); effects.to_csv(P/'amount_conditional_effects.csv',index=False)
print('\nCONDITIONAL AMOUNT EFFECTS (cells each n>=1000):')
eligible=effects[(effects.n_left>=1000)&(effects.n_right>=1000)]
print(eligible.groupby(['comparison','period']).agg(currency_cells=('currency','count'),
    median_ratio_across_currencies=('median_ratio','median'),
    min_ratio=('median_ratio','min'),max_ratio=('median_ratio','max'),
    min_log_effect=('log_mean_difference','min'),max_log_effect=('log_mean_difference','max')).to_string())
print('\nUSD amounts excluding labels:')
print(q[q.currency.eq('USD')].to_string(index=False))
print('\nSame amount prior lag distributions for each label:')
for label,g in e[e.same_amount_prior.gt(0)].groupby('label'):
    print(label or '<unlabelled controls>',len(g),pd.to_numeric(g.seconds_since_latest_exact).quantile([0,.1,.5,.9,1]).to_dict())
print('\nPower exponents by recorded label:')
print(e[e.power10_prior.gt(0)].groupby(['label','power_exponent']).size().to_string())
