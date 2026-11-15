"""Independent B full-file numeric/BIC scan for bank/corridor and network tests."""
from pathlib import Path
import json,time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'analysis/round3/b'; OUT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/'outputs/round3/b'; CACHE.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
N=10_000_000
DT=np.dtype([('epoch','i8'),('log_amount','f4'),('log_duration','f4'),
 ('sender','u2'),('receiver','u2'),('currency','u1'),('party','u1'),
 ('route','u1'),('fx','u1'),('participants','u1'),('continuous','u1'),
 ('labelled','u1'),('firstmid','u2'),('sender_country','u1'),('receiver_country','u1')])
x=np.lib.format.open_memmap(CACHE/'rows.npy',mode='w+',dtype=DT,shape=(N,))
profile=json.loads((ROOT/'outputs/cleaned/profile.json').read_text())
currencies=sorted(profile['category_counts']['currency_code']); cmap={v:i for i,v in enumerate(currencies)}
bics={}; countries={}; empty_mid=np.iinfo('u2').max
def encode(values,mapping):
    for v in pd.unique(values):
        if v not in mapping:
            if len(mapping)>=empty_mid: raise RuntimeError('uint16 category capacity')
            mapping[v]=len(mapping)
    return values.map(mapping).to_numpy()
cols=['epoch_seconds','usd_amount','total_duration','ordering_bic8','beneficiary_bic8',
 'bic8_path','currency_code','ordering_type','beneficiary_type','transaction_type_code',
 'currency_conversion_count','participant_count','continuity_qflag','anomaly_type']
n=0;start=time.monotonic()
for d in pd.read_csv(SOURCE,usecols=cols,dtype=str,keep_default_na=False,chunksize=100_000):
    z=x[n:n+len(d)]
    z['epoch']=pd.to_numeric(d.epoch_seconds).to_numpy()
    z['log_amount']=np.log(pd.to_numeric(d.usd_amount).to_numpy())
    z['log_duration']=np.log(pd.to_numeric(d.total_duration).to_numpy())
    # First visible intermediary; paths with fewer than three visible BICs use sentinel.
    firstmid=[]
    for p in d.bic8_path:
        v=[s for s in p.split(';') if s!='...']
        firstmid.append(v[1] if len(v)>2 else '')
    allbic=pd.concat([d.ordering_bic8,d.beneficiary_bic8,pd.Series(firstmid)],ignore_index=True)
    encode(allbic[allbic.ne('')],bics)
    z['sender']=d.ordering_bic8.map(bics).to_numpy()
    z['receiver']=d.beneficiary_bic8.map(bics).to_numpy()
    z['firstmid']=pd.Series(firstmid).map(bics).fillna(empty_mid).to_numpy(dtype='u2')
    sc=d.ordering_bic8.str[4:6];rc=d.beneficiary_bic8.str[4:6]
    both=pd.concat([sc,rc],ignore_index=True);encode(both,countries)
    z['sender_country']=sc.map(countries).to_numpy();z['receiver_country']=rc.map(countries).to_numpy()
    z['currency']=d.currency_code.map(cmap).to_numpy()
    z['party']=(d.ordering_type.eq('C').astype('u1')*2+d.beneficiary_type.eq('C').astype('u1')).to_numpy()
    z['route']=d.transaction_type_code.map({'Direct':0,'Indirect':1,'Covered':2}).to_numpy()
    z['fx']=pd.to_numeric(d.currency_conversion_count).to_numpy()
    z['participants']=pd.to_numeric(d.participant_count).to_numpy()
    z['continuous']=d.continuity_qflag.eq('Y').to_numpy();z['labelled']=d.anomaly_type.ne('').to_numpy()
    n+=len(d)
    if n%1_000_000==0: print(n,round(time.monotonic()-start,1),len(bics),flush=True)
assert n==N;x.flush()
(CACHE/'bic_map.json').write_text(json.dumps(bics,sort_keys=True))
(CACHE/'country_map.json').write_text(json.dumps(countries,sort_keys=True))
manifest={'status':'complete','rows':n,'seconds':time.monotonic()-start,'bics':len(bics),
 'countries':len(countries),'currencies':len(currencies),'source_bytes':SOURCE.stat().st_size,
 'source_mtime_ns':SOURCE.stat().st_mtime_ns,'firstmid_definition':'second visible non-gap BIC when at least3 visible BICs; otherwise uint16 max'}
(OUT/'scan_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2),flush=True)
