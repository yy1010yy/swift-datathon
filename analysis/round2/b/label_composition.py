"""Independent exact label-party census; no anomaly mechanism inferred from names."""
from pathlib import Path
from collections import Counter
import time
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
c=Counter();n=0;start=time.monotonic()
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=['anomaly_type','ordering_type','beneficiary_type'],dtype=str,keep_default_na=False,chunksize=200000):
 c.update(d.value_counts(sort=False).to_dict());n+=len(d)
 if n%2000000==0:print(n,round(time.monotonic()-start,1),flush=True)
assert n==10000000
z=pd.DataFrame([list(k)+[v] for k,v in c.items()],columns=['ordering_type','beneficiary_type','anomaly_type','n'])
# pandas read_csv usecols preserves source column order, not requested list order.
# Source order: ordering_type, beneficiary_type, anomaly_type.
assert z.loc[z.anomaly_type.eq('CUSTOMER_RECALL'),'n'].sum()==317
z.to_csv(OUT/'label_party.csv',index=False)
print(z.to_string(index=False),flush=True)
