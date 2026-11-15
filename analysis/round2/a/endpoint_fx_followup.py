"""Small-table follow-up: endpoint rates and internal FX-zone discovery."""
from pathlib import Path
import pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
t=pd.read_csv(OUT/'routing_joint.csv')
rows=[]
for key,g in t.groupby(['month','route','q']):
 n=int(g.n.sum());sm=int(g.loc[g.sm.eq(1),'n'].sum());rm=int(g.loc[g.rm.eq(1),'n'].sum());both=int(g.loc[g.sm.eq(1)&g.rm.eq(1),'n'].sum())
 expected=sm*rm/n
 rows.append(list(key)+[n,sm,rm,both,sm/n,rm/n,expected,both-expected])
pd.DataFrame(rows,columns=['month','route','continuous','n','sender_mismatch','receiver_mismatch','both','sender_rate','receiver_rate','expected_both_independent','both_minus_expected']).to_csv(OUT/'endpoint_strata.csv',index=False)
c=pd.read_csv(OUT/'direct_country_currency.csv',keep_default_na=False);z=c[c.fx==0]
d=z.groupby(['from','currency']).n.sum().reset_index();modes=d.sort_values('n',ascending=False).drop_duplicates('from').set_index('from').currency
predict=c['from'].map(modes).ne(c['to'].map(modes)).astype(int)
modes.rename('inferred_currency').to_csv(OUT/'country_currency_inferred.csv')
print('Mode currency discovery on full direct FX0 payments: agreements',int(c.loc[c.fx.eq(predict),'n'].sum()),'/',int(c.n.sum()))
parents={v:v for v in set(c['from'])|set(c['to'])}
def find(v):
 while parents[v]!=v:parents[v]=parents[parents[v]];v=parents[v]
 return v
for r in z.itertuples(index=False):
 a,b=find(r[0]),find(r[1]);parents[b]=a
groups={v:find(v) for v in parents}
pred=c['from'].map(groups).ne(c['to'].map(groups)).astype(int)
print('FX0 country-pair connected components, all-data discovery agreement',int(c.loc[c.fx.eq(pred),'n'].sum()),'/',int(c.n.sum()))
print('This is descriptive full-data discovery: FX0 edges construct groups, so independent period/path validation is essential.')
pd.DataFrame(sorted(groups.items()),columns=['country_like_code','zero_fx_component']).to_csv(OUT/'fx_zone_components.csv',index=False)
