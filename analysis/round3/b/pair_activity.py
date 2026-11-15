"""Activity-only benchmark for blank-label directed account-pair recurrence.

Uses C's shared raw-to-pair extraction but independently aggregates exact strings and
scores a Poisson independence benchmark. This does not independently validate filtering.
"""
from pathlib import Path
from collections import Counter
import json,time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round3/b'
P=ROOT/'outputs/round2/c/counterparty_population/pair_summary.csv';N=9_992_994
send=Counter();recv=Counter();sdeg=Counter();rdeg=Counter();rows=0;start=time.monotonic()
for d in pd.read_csv(P,usecols=['sender','receiver','n','party'],dtype={'sender':str,'receiver':str,'n':'int64','party':str},chunksize=200_000):
    # Aggregate duplicate entity keys within each chunk before Counter.update; a plain
    # dict(zip(...)) silently retains only the last row for repeated keys.
    send.update(d.groupby('sender',sort=False).n.sum().to_dict());recv.update(d.groupby('receiver',sort=False).n.sum().to_dict())
    sdeg.update(d.sender);rdeg.update(d.receiver);rows+=len(d)
    if rows%1_000_000<200_000: print('pass1',rows,round(time.monotonic()-start,1),flush=True)
assert sum(send.values())==sum(recv.values())==N
cells=Counter();actual_repeat=0;expected_repeat=0.;actual_payments=0;expected_payments=0.;max_lam=0.;rows2=0
for d in pd.read_csv(P,usecols=['sender','receiver','n','party'],dtype={'sender':str,'receiver':str,'n':'int64','party':str},chunksize=200_000):
    st=d.sender.map(send).to_numpy(dtype='f8');rt=d.receiver.map(recv).to_numpy(dtype='f8');lam=st*rt/N
    # Conditional on the pair being observed at least once under independent Poisson draws.
    q=1-lam/np.expm1(lam);q=np.where(lam>50,1.,q)
    em=lam/(-np.expm1(-lam));em=np.where(lam>50,lam,em)
    rep=d.n.to_numpy()>1;actual_repeat+=int(rep.sum());expected_repeat+=float(q.sum())
    actual_payments+=int(d.n.sum());expected_payments+=float(em.sum());max_lam=max(max_lam,float(lam.max()))
    # Fixed expected-rate bins retain activity scale and party type.
    edges=np.array([-20,-6,-5,-4,-3,-2,-1,0,1,2,20],float);bid=np.digitize(np.log10(np.maximum(lam,1e-300)),edges)-1
    t=pd.DataFrame({'party':d.party,'bin':bid,'pairs':1,'actual_repeat':rep.astype('i8'),'expected_repeat':q,'actual_n':d.n,'expected_n':em})
    for k,row in t.groupby(['party','bin'],sort=False).agg({'pairs':'sum','actual_repeat':'sum','expected_repeat':'sum','actual_n':'sum','expected_n':'sum'}).iterrows():
        for col,val in row.items():cells[(k[0],int(k[1]),col)]+=float(val)
    rows2+=len(d)
    if rows2%1_000_000<200_000: print('pass2',rows2,round(time.monotonic()-start,1),flush=True)
assert rows==rows2==8_258_480 and actual_payments==N
table=[]
for party in ['BB','BC','CB','CC']:
 for b in sorted({k[1] for k in cells if k[0]==party}):
  row={'party':party,'lambda_bin':b};row.update({c:cells[(party,b,c)] for c in ['pairs','actual_repeat','expected_repeat','actual_n','expected_n']});table.append(row)
pd.DataFrame(table).to_csv(OUT/'activity_independence_cells.csv',index=False)
def stat(v):
 a=np.array(list(v),dtype='f8');s=np.sort(a);n=len(s)
 return {'entities':n,'total':int(s.sum()),'median':float(np.median(s)),'p90':float(np.quantile(s,.9)),
 'p99':float(np.quantile(s,.99)),'max':float(s[-1]),'gini':float(2*np.sum((np.arange(n)+1)*s)/(n*s.sum())-(n+1)/n)}
result={'status':'complete','observed_pairs':rows,'blank_payments':N,'actual_repeated_pairs':actual_repeat,
 'poisson_activity_expected_repeated_pairs_conditional_observed':expected_repeat,
 'actual_payments_in_observed_pairs':actual_payments,'poisson_activity_expected_payments_conditional_observed':expected_payments,
 'ratio_actual_to_expected_repeated_pairs':actual_repeat/expected_repeat,'max_lambda':max_lam,
 'sender_payment_activity':stat(send.values()),'receiver_payment_activity':stat(recv.values()),
 'sender_partner_degree':stat(sdeg.values()),'receiver_partner_degree':stat(rdeg.values()),
 'runtime_seconds':time.monotonic()-start,
 'limit':'Shared C blank-label pair extraction; independent exact-string aggregation/scoring. Poisson benchmark conditions on observed pairs and estimated margins; it is diagnostic, not an exact configuration-model test.'}
(OUT/'activity_independence.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
