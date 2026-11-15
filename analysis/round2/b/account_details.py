"""Independent full-file fake-account/first-detail-line construction and sampled identity consistency.

Every record tested for account/detail relation. Identity consistency is only for an
account-hash-selected3/256subset, all occurrences retained; comparisons use exact raw
strings, not hashes. No identifiers normalized. No external data.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,time
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
c=Counter();state={};sample_counts=Counter();conflict_accounts={k:set() for k in ['details','bic','type']};examples=[]
rows=0;start=time.monotonic()
cols=['source_record','epoch_seconds']+[s+'_'+v for s in ['ordering','beneficiary'] for v in ['account','details','bic8','type']]
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
 month=pd.to_datetime(d.epoch_seconds.astype('int64'),unit='s',utc=True).dt.strftime('%Y-%m')
 for side in ['ordering','beneficiary']:
  account=d[side+'_account'];detail=d[side+'_details'];identifier=account.str.slice(6)
  first=detail.str.split(r'\r\n|\n|\\r\\n|\\n',n=1,regex=True).str[0]
  one=first.eq('/'+identifier);allslash=first.str.lstrip('/').eq(identifier)
  leading=[];anywhere=[]
  for f,ident,text in zip(first,identifier,detail):
   prefix=f[:-len(ident)] if ident and f.endswith(ident) else ''
   leading.append(bool(prefix) and prefix.strip('/')=='');anywhere.append(bool(ident) and ident in text)
  z=pd.DataFrame({'month':month,'party':d[side+'_type'],'fake_prefix':account.str.startswith('_FAKE_'),
   'single_slash_match':one,'strip_all_slash_match':allslash,'slash_prefix_match':leading,
   'identifier_anywhere':anywhere,'actual_LF':detail.str.contains('\n',regex=False),
   'literal_backslash_n':detail.str.contains('\\n',regex=False)})
  c.update({(side,)+k:v for k,v in z.value_counts(sort=False).items()})
  chosen={v:hashlib.sha256(v.encode('utf-8')).digest()[0]<3 for v in account.unique()}
  selected=account.map(chosen)
  for record,acc,det,bic,party in d.loc[selected,['source_record',side+'_account',side+'_details',side+'_bic8',side+'_type']].itertuples(index=False,name=None):
   key=(side,acc);sample_counts[side]+=1;new=(det,bic,party)
   if key not in state:state[key]=new
   else:
    original=state[key]
    for i,field in enumerate(['details','bic','type']):
     if original[i]!=new[i]:
      conflict_accounts[field].add(key)
      if len(examples)<30:examples.append(dict(side=side,source_record=record,field=field,account=acc))
 rows+=len(d)
 if rows%1000000==0:print(rows,round(time.monotonic()-start,1),flush=True)
assert rows==10000000
z=pd.DataFrame([list(k)+[v] for k,v in c.items()],columns=['side']+list(z.columns)+['n']);z.to_csv(OUT/'account_detail_joint.csv',index=False)
summary={'rows':rows,'seconds':time.monotonic()-start,'sample_selection':'SHA256(rawaccount UTF8) firstbyte<3,3/256accountsubset; allselectedoccurrences',
 'sample_unique_side_accounts':len(state),'sample_records_by_side':dict(sample_counts),
 'sample_conflicting_side_accounts':{field:len(v) for field,v in conflict_accounts.items()},
 'scope':'Account/detailalignmentfullcensus;identityconsistencysampleonly;exactrawstringcomparison'}
pd.DataFrame(examples).to_csv(OUT/'account_sample_conflict_examples.csv',index=False)
(OUT/'account_details_initial.json').write_text(json.dumps(summary,indent=2))
print(z.groupby('side').apply(lambda g:pd.Series({k:int(g.loc[g[k],'n'].sum()) for k in ['fake_prefix','single_slash_match','strip_all_slash_match','slash_prefix_match','identifier_anywhere','actual_LF','literal_backslash_n']})).to_string(),flush=True)
print(json.dumps(summary,indent=2),flush=True)
