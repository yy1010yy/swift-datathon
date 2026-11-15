"""Train data-only currency preferences by sender/receiver country codes; July checks."""
from pathlib import Path
import pandas as pd,json
base=Path(__file__).resolve().parent
t=pd.read_csv(base/'b/currency_counts.csv',keep_default_na=False)
assert t.n.sum()==10000000
train=t[t.period.eq('early')];test=t[t.period.eq('July')].copy()
preferences={}
for side in ['sender','receiver']:
    col=side+'_country_code'
    g=train.groupby([col,'currency']).n.sum().reset_index()
    preferences[side]=g.sort_values('n',ascending=False).drop_duplicates(col).set_index(col).currency.to_dict()
    test[side+'_mode']=test[col].map(preferences[side])
    test[side+'_mode_hit']=test.currency.eq(test[side+'_mode'])
test['either_mode_hit']=test.sender_mode_hit|test.receiver_mode_hit
test['both_modes_same']=test.sender_mode.eq(test.receiver_mode)
test['mode_category']='neither'
test.loc[test.receiver_mode_hit,'mode_category']='receiver_only'
test.loc[test.sender_mode_hit,'mode_category']='sender_only'
test.loc[test.sender_mode_hit&test.receiver_mode_hit,'mode_category']='both'
out=test.groupby(['party','both_modes_same','mode_category']).n.sum().reset_index()
out.to_csv(base/'currency_mode_validation.csv',index=False)
print('July records',int(test.n.sum()))
print(out.to_string(index=False))
print('Sender mode accuracy',test.loc[test.sender_mode_hit,'n'].sum()/test.n.sum())
print('Either mode coverage',test.loc[test.either_mode_hit,'n'].sum()/test.n.sum())
(base/'currency_mode_parameters.json').write_text(json.dumps({'learned_preferences':preferences,
    'limits':'Country-code preference proxy learned on preJuly counts, not external legal tender map. Receiver preferences estimated from received payment currencies, not native currency definition. Correlation does not identify who selected payment currency.'},indent=2))
