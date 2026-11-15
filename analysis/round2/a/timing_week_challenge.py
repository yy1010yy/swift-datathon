"""Country/party composition challenge to weekly-volume quantization."""
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
d=pd.read_csv(OUT/'timing_complete_week_counts.csv',keep_default_na=False)
globalshares=d.groupby('week').n.sum().reindex(range(13),fill_value=0).to_numpy();globalshares=globalshares/globalshares.sum()
rows=[]
for c,g in d.groupby('sender_country_code'):
 n=int(g.n.sum())
 if n<10000:continue
 a=g.groupby('week').n.sum().reindex(range(13),fill_value=0).to_numpy()/n
 rows.append([c,n,float(.5*np.abs(a-globalshares).sum()),float(np.max(np.abs(a-np.round(a/.005)*.005))),float(a[0]-globalshares[0]),float(a[-1]-globalshares[-1])])
t=pd.DataFrame(rows,columns=['sender_country_code','n','week_share_TV_vs_global','max_quantization_error','first_week_difference','last_week_difference'])
t.to_csv(OUT/'timing_week_country_challenge.csv',index=False)
parts=[]
for party,g in d.groupby('party'):
 n=int(g.n.sum());a=g.groupby('week').n.sum().reindex(range(13),fill_value=0).to_numpy()/n
 for week,v in enumerate(a):parts.append([party,week+1,n,float(v),float(v-globalshares[week])])
pd.DataFrame(parts,columns=['party','week','party_n','week_share','difference_vs_global']).to_csv(OUT/'timing_week_party_challenge.csv',index=False)
print('Countrylikecode groups>=10000',len(t),'weekshareTV range',t.week_share_TV_vs_global.min(),t.week_share_TV_vs_global.max())
print(t.sort_values('n',ascending=False).head(12).to_string(index=False))
print('Differences can reflect finite-count noise or UTC boundary effects; these tests do not identify local week boundaries.')
