"""Independent C early-fitted currency heuristics on B's full-file aggregate counts."""
from pathlib import Path
import pandas as pd
import numpy as np
import json
P=Path(__file__).resolve().parent
d=pd.read_csv(P.parent/'b/currency_counts.csv',keep_default_na=False)
assert d.n.sum()==10000000
train=d[d.period.eq('early')];test=d[d.period.eq('July')].copy()
def modes(col):
    a=train.groupby([col,'currency'],as_index=False).n.sum().sort_values([col,'n','currency'],ascending=[True,False,True])
    return a.drop_duplicates(col).set_index(col).currency
sm=modes('sender_country_code');rm=modes('receiver_country_code')
sm.rename('sender_mode').to_csv(P/'sender_code_currency_modes.csv');rm.rename('receiver_mode').to_csv(P/'receiver_code_currency_modes.csv')
global_mode=train.groupby('currency').n.sum().idxmax()
test['sender_mode']=test.sender_country_code.map(sm).fillna('UNSEEN')
test['receiver_mode']=test.receiver_country_code.map(rm).fillna('UNSEEN')
test['sender_hit']=test.currency.eq(test.sender_mode);test['receiver_hit']=test.currency.eq(test.receiver_mode)
test['either_hit']=test.sender_hit|test.receiver_hit;test['global_hit']=test.currency.eq(global_mode)
test['sender_unseen']=test.sender_mode.eq('UNSEEN');test['receiver_unseen']=test.receiver_mode.eq('UNSEEN')
def summary(g):
    n=int(g.n.sum());return dict(n=n,**{k:int(g.loc[g[k],'n'].sum()) for k in
      ['sender_hit','receiver_hit','either_hit','global_hit','sender_unseen','receiver_unseen']})
result={'population':'all records including labelled','training':'preJuly','evaluation':'July',
        'input':'B independently extracted full10M corridor/party/currency count table; shared input with lead, independent heuristic implementation',
        'global_early_mode':global_mode,'all':summary(test),
        'by_party':{['BB','BC','CB','CC'][int(p)]:summary(g) for p,g in test.groupby('party')}}
(P/'currency_modes.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
weighted=test[['sender_country_code','receiver_country_code','party','n']].copy()
for col in ['sender_hit','receiver_hit','either_hit','global_hit','sender_unseen','receiver_unseen']:
    weighted[col]=test.n*test[col]
weighted.groupby(['sender_country_code','receiver_country_code','party'],as_index=False).sum().rename(
    columns={'sender_country_code':'sender_code','receiver_country_code':'receiver_code'}).to_csv(P/'currency_mode_corridors.csv',index=False)
