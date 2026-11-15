"""Independent full-file token-country alignment test; country codes internal only."""
from pathlib import Path
from collections import Counter
import re,time,json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
c=Counter();n=0;start=time.monotonic()
cols=['ordering_tokens','beneficiary_tokens','ordering_type','beneficiary_type','ordering_bic8','beneficiary_bic8','epoch_seconds']
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
 month=pd.to_datetime(d.epoch_seconds.astype('int64'),unit='s',utc=True).dt.strftime('%Y-%m')
 oc=d.ordering_tokens.str.findall(r'<country_code:([^>]+)>');bc=d.beneficiary_tokens.str.findall(r'<country_code:([^>]+)>')
 for side,tokens,other in [('ordering',oc,bc),('beneficiary',bc,oc)]:
  z=pd.DataFrame({'month':month,'party_type':d[side+'_type'],'token_count':tokens.str.len(),
    'own_bank_match':tokens.combine(d[side+'_bic8'].str[4:6],lambda a,b: b in a),
    'ordering_bank_match':tokens.combine(d.ordering_bic8.str[4:6],lambda a,b:b in a),
    'other_bank_match':tokens.combine(d[('beneficiary' if side=='ordering' else 'ordering')+'_bic8'].str[4:6],lambda a,b:b in a),
    'other_party_token_match':tokens.combine(other,lambda a,b:bool(set(a)&set(b)))})
  c.update({(side,)+k:v for k,v in z.value_counts(sort=False).items()})
 n+=len(d)
 if n%1000000==0:print(n,round(time.monotonic()-start,1),flush=True)
assert n==10000000
z=pd.DataFrame([list(k)+[v] for k,v in c.items()],columns=['side','month','party_type','token_count','own_bank_match','ordering_bank_match','other_bank_match','other_party_token_match','n'])
z.to_csv(OUT/'token_country_joint.csv',index=False)
for side,g in z.groupby('side'):
 print(side,'rows',g.n.sum(),'missing',g.loc[g.token_count.eq(0),'n'].sum(),'multiple',g.loc[g.token_count.gt(1),'n'].sum(),flush=True)
 for col in ['own_bank_match','ordering_bank_match','other_bank_match','other_party_token_match']:
  print(col,int(g.loc[g[col],'n'].sum()),flush=True)
(OUT/'token_manifest.json').write_text(json.dumps({'records':n,'seconds':time.monotonic()-start,'complete':True},indent=2))
