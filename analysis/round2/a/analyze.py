"""Independent reviewer A: full-file numeric and path mechanism census."""
from pathlib import Path
from collections import Counter
import json,time,re
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'analysis/round2/a'
CACHE=ROOT/'outputs/round2/a'; CACHE.mkdir(parents=True,exist_ok=True)
DT=np.dtype([('amount','f8'),('duration','i4'),('p','i2'),('fx','i2'),('epoch','i8'),('route','u1'),('q','u1'),('party','U2'),('currency','U3'),('label','U30'),('changes','i2'),('sm','u1'),('rm','u1')])
data=np.lib.format.open_memmap(CACHE/'numeric.npy',mode='w+',dtype=DT,shape=(10000000,))
cols=['epoch_seconds','usd_amount','total_duration','participant_count','currency_conversion_count','transaction_type_code','continuity_qflag','ordering_type','beneficiary_type','currency_code','anomaly_type','bic8_path','ordering_bic8','beneficiary_bic8']
country=Counter(); counts=Counter(); offset=0; start=time.monotonic()
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    n=len(d); x=data[offset:offset+n]
    for dest,src in [('amount','usd_amount'),('duration','total_duration'),('p','participant_count'),('fx','currency_conversion_count'),('epoch','epoch_seconds')]:x[dest]=pd.to_numeric(d[src]).to_numpy()
    x['route']=d.transaction_type_code.map({'Direct':0,'Indirect':1,'Covered':2})
    x['q']=d.continuity_qflag.eq('Y');x['party']=d.ordering_type+d.beneficiary_type
    x['currency']=d.currency_code;x['label']=d.anomaly_type
    paths=d.bic8_path.str.split(';'); first=paths.str[0]; last=paths.str[-1]
    x['sm']=first.ne(d.ordering_bic8); x['rm']=last.ne(d.beneficiary_bic8)
    parsed={}
    for path in d.bic8_path.unique():
        a=[v for v in path.split(';') if re.fullmatch('[A-Z0-9]{8}',v)]
        parsed[path]=sum(a[i][4:6]!=a[i-1][4:6] for i in range(1,len(a)))
    x['changes']=d.bic8_path.map(parsed)
    t=pd.DataFrame({'from':first.str[4:6],'to':last.str[4:6],'fx':x['fx'],'currency':d.currency_code})
    country.update(t.loc[x['route']==0].value_counts(sort=False).to_dict())
    month=pd.to_datetime(x['epoch'],unit='s',utc=True).strftime('%Y-%m')
    t=pd.DataFrame({'route':x['route'],'q':x['q'],'p':x['p'],'fx':x['fx'],'changes':x['changes'],'month':month,'sm':x['sm'],'rm':x['rm']})
    counts.update(t.value_counts(sort=False).to_dict())
    offset+=n
    if offset%1000000==0:print(offset,round(time.monotonic()-start,1),flush=True)
assert offset==10000000; data.flush()
pd.DataFrame([list(k)+[v] for k,v in country.items()],columns=['from','to','fx','currency','n']).to_csv(OUT/'direct_country_currency.csv',index=False)
pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=['route','q','p','fx','changes','month','sm','rm','n']).to_csv(OUT/'routing_joint.csv',index=False)
print('Census complete',offset,'seconds',time.monotonic()-start,flush=True)
