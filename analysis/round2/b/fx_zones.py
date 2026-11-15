"""Independent graph-vs-payment-currency FX rules, shared full-direct counts discovery."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'analysis/round2/a/direct_country_currency.csv',keep_default_na=False)
parent={x:x for x in set(d['from'])|set(d['to'])}
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for r in d[d.fx.eq(0)].itertuples():parent[find(r[1])]=find(r[2])
d['graph_fx']=[int(find(f)!=find(t)) for f,t in zip(d['from'],d['to'])]
same=d[d['from'].eq(d['to'])]
counts=same.groupby(['from','currency']).n.sum().reset_index()
modes=counts.loc[counts.groupby('from').n.idxmax()].set_index('from').currency.to_dict()
d['currency_zone_fx']=[int(modes[f]!=modes[t]) if f in modes and t in modes else -1 for f,t in zip(d['from'],d['to'])]
d['payment_currency_fx']=[int(c!=modes[f])+int(c!=modes[t]) if f in modes and t in modes else -1 for f,t,c in zip(d['from'],d['to'],d.currency)]
result={'population':int(d.n.sum()),'discovery':'all supplied direct-route aggregated counts, including gapped; no pristine validation',
 'graph_components':len(set(map(find,parent))),'multi_code_components':[],
 'match_counts':{k:int(d.loc[d[k].eq(d.fx),'n'].sum()) for k in ['graph_fx','currency_zone_fx','payment_currency_fx']},
 'heuristic_known_code_denominator':int(d.loc[d.currency_zone_fx.ge(0),'n'].sum()),
 'missing_same_country_currency_codes':sorted(set(parent)-set(modes))}
components={}
for x in parent:components.setdefault(find(x),[]).append(x)
result['multi_code_components']=[sorted(v) for v in components.values() if len(v)>1]
pd.DataFrame([{'country_code':x,'zone':find(x),'same_country_modal_currency':modes.get(x,'')} for x in sorted(parent)]).to_csv(OUT/'fx_components.csv',index=False)
d.to_csv(OUT/'fx_direct_rules.csv',index=False)
(OUT/'fx_initial.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
