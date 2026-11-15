"""Full-file exact BIC integer cache aligned to round2 A numeric rows."""
from pathlib import Path
import time,json
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
CACHE=ROOT/'outputs/round3/c';CACHE.mkdir(parents=True,exist_ok=True)
dtype=np.dtype([('sender','u4'),('receiver','u4')])
a=np.lib.format.open_memmap(CACHE/'banks.npy',mode='w+',dtype=dtype,shape=(10000000,))
mapping={}; inverse=[]
def encode(s):
    vals=s.unique()
    for v in vals:
        if v not in mapping:mapping[v]=len(inverse);inverse.append(v)
    return s.map(mapping).to_numpy(dtype='u4')
start=time.monotonic();n=0
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=['ordering_bic8','beneficiary_bic8'],dtype=str,keep_default_na=False,chunksize=200000):
    a['sender'][n:n+len(d)]=encode(d.ordering_bic8);a['receiver'][n:n+len(d)]=encode(d.beneficiary_bic8);n+=len(d)
    if n%1000000==0:print(n,round(time.monotonic()-start,1),flush=True)
assert n==10000000;a.flush()
pd.DataFrame({'bank_id':np.arange(len(inverse)),'bic8':inverse,'country':[v[4:6] for v in inverse]}).to_csv(OUT/'bank_codes.csv',index=False)
manifest={'status':'complete','rows':n,'unique_bics':len(inverse),'elapsed_seconds':time.monotonic()-start,
 'alignment':'CSV physical record order; same source/profile as outputs/round2/a/numeric.npy'}
(OUT/'bank_cache_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
