"""Independent earlier-period country-modal-currency predictions on July counts."""
from pathlib import Path
import json
import pandas as pd
OUT=Path(__file__).resolve().parent
d=pd.read_csv(OUT/'currency_counts.csv',keep_default_na=False)
early=d[d.period.eq('early')];july=d[d.period.eq('July')].copy()
rows=[];modes={}
for side in ['sender','receiver']:
 col=side+'_country_code'
 c=early.groupby([col,'currency']).n.sum().reset_index().sort_values([col,'n','currency'],ascending=[True,False,True])
 mapping=c.drop_duplicates(col).set_index(col).currency.to_dict();modes[side]=mapping
 july[side+'_known']=july[col].isin(mapping);july[side+'_prediction']=july[col].map(mapping)
 july[side+'_correct']=july.currency.eq(july[side+'_prediction'])
 for party,g in july.groupby('party'):
  known=g[side+'_known'];correct=g[side+'_correct']
  rows.append(dict(predictor=side+'_country_mode',party=['BB','BC','CB','CC'][party],n=int(g.n.sum()),
    known_n=int(g.loc[known,'n'].sum()),correct_n=int(g.loc[known&correct,'n'].sum())))
pd.DataFrame(rows).to_csv(OUT/'currency_temporal_predictions.csv',index=False)
(OUT/'currency_temporal_modes.json').write_text(json.dumps(modes,indent=2))
print(pd.DataFrame(rows).to_string(index=False))
print('Mode discovery uses all earlier records without roleconditioning; heldJuly scores are conditional predictive associations, not causal preferences.')
