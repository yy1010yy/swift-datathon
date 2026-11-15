"""Independent B full-census amount/timing/routing investigation. No external data."""
from pathlib import Path
from collections import Counter
import json, time, hashlib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
CACHE=ROOT/'outputs/eda_round2'
CACHE.mkdir(exist_ok=True,parents=True)
source=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
profile=json.loads((ROOT/'outputs/cleaned/profile.json').read_text())
currencies=sorted(profile['category_counts']['currency_code'])
currency_map={s:i for i,s in enumerate(currencies)}
party_names=['BB','BC','CB','CC']; routes=['Direct','Indirect','Covered']
dtype=np.dtype([('amount','f8'),('duration','i4'),('epoch','i8'),('currency','u2'),
 ('party','u1'),('route','u1'),('fx','u1'),('participants','u1'),('continuous','u1'),('labeled','u1'),('country','S2')])
path=CACHE/'b_rows.npy'
a=np.lib.format.open_memmap(path,mode='w+',dtype=dtype,shape=(profile['records'],))
hour=Counter(); currency_choice=Counter(); diagnostic=Counter()
start=time.monotonic(); n=0
cols=['usd_amount','total_duration','epoch_seconds','currency_code','ordering_type','beneficiary_type',
 'transaction_type_code','currency_conversion_count','participant_count','continuity_qflag','ordering_bic8','beneficiary_bic8','anomaly_type']
for d in pd.read_csv(source,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    sl=a[n:n+len(d)]
    for dest,src in [('amount','usd_amount'),('duration','total_duration'),('epoch','epoch_seconds'),('fx','currency_conversion_count'),('participants','participant_count')]: sl[dest]=pd.to_numeric(d[src],errors='raise')
    sl['currency']=d.currency_code.map(currency_map)
    sl['party']=(d.ordering_type.eq('C').astype('uint8')*2+d.beneficiary_type.eq('C').astype('uint8'))
    sl['route']=d.transaction_type_code.map({x:i for i,x in enumerate(routes)})
    sl['continuous']=d.continuity_qflag.eq('Y')
    sl['labeled']=d.anomaly_type.ne('')
    country=d.ordering_bic8.str[4:6]
    sl['country']=country.to_numpy(dtype='S2')
    dt=pd.to_datetime(sl['epoch'],unit='s',utc=True)
    # Complete observed calendar dates only, excluding partial boundary days.
    full=(dt>=pd.Timestamp('2023-05-01',tz='UTC'))&(dt<pd.Timestamp('2023-07-31',tz='UTC'))
    t=pd.DataFrame({'country':country.to_numpy(),'party':sl['party'],'period':np.where(sl['epoch']<1688169600,'MayJune','July'),
      'hour':dt.hour,'weekday':dt.dayofweek})
    hour.update(t.loc[full].value_counts(sort=False).to_dict())
    c=pd.DataFrame({'sender':d.ordering_bic8.str[4:6],'receiver':d.beneficiary_bic8.str[4:6],
      'party':sl['party'],'currency':d.currency_code,'period':np.where(sl['epoch']<1688169600,'early','July')})
    currency_choice.update(c.value_counts(sort=False).to_dict())
    n+=len(d)
    if n%1000000==0: print(f'{n:,} rows / {time.monotonic()-start:.1f}s',flush=True)
assert n==10000000
a.flush()
def counter_csv(counter,names,path):
    z=pd.DataFrame([list(k)+[int(v)] for k,v in counter.items()],columns=names+['n'])
    z.to_csv(OUT/path,index=False);return z
counter_csv(hour,['sender_country_code','party','period','hour','weekday'],'timing_counts.csv')
counter_csv(currency_choice,['sender_country_code','receiver_country_code','party','currency','period'],'currency_counts.csv')
print('Full scan completed, computing exact quantiles',flush=True)
period=(a['epoch']>=1688169600).astype('u1')
def summarize_amount(indices,group):
    v=a['amount'][indices]; log=np.log(v)
    q=np.quantile(v,[.01,.1,.5,.9,.99])
    cents=np.rint(v*100).astype('i8')
    return dict(group,n=len(v),q01=q[0],q10=q[1],median=q[2],q90=q[3],q99=q[4],
      mean=float(v.mean()),log_mean=float(log.mean()),log_sd=float(log.std()),
      integer_dollar_n=int((cents%100==0).sum()),round_100_n=int((cents%10000==0).sum()),
      labeled_n=int(a['labeled'][indices].sum()))
amount=[]
group=a['currency'].astype('i4')*8+a['party']*2+period
order=np.argsort(group,kind='stable'); sg=group[order]
bound=np.r_[0, np.flatnonzero(np.diff(sg))+1,len(sg)]
for lo,hi in zip(bound[:-1],bound[1:]):
    key=int(sg[lo]); currency=currencies[key//8]; party=party_names[(key%8)//2]; per=['early','July'][key%2]
    amount.append(summarize_amount(order[lo:hi],dict(currency=currency,party=party,period=per)))
pd.DataFrame(amount).to_csv(OUT/'amount_currency_party_period.csv',index=False)
global_amount=[]
for p in range(4):
 for per in [0,1]:
  idx=np.flatnonzero((a['party']==p)&(period==per))
  global_amount.append(summarize_amount(idx,dict(party=party_names[p],period=['early','July'][per])))
pd.DataFrame(global_amount).to_csv(OUT/'amount_party_period.csv',index=False)
print(pd.DataFrame(global_amount).to_string(index=False),flush=True)
# Exact route/fx/participant/period duration summaries: variance distinguishes deterministic increments.
keys=a['route'].astype('i4')*10000+a['continuous'].astype('i4')*5000+a['participants'].astype('i4')*100+a['fx'].astype('i4')*2+period
ix=np.argsort(keys,kind='stable'); sk=keys[ix]
bound=np.r_[0,np.flatnonzero(np.diff(sk))+1,len(sk)]
dur=[]
for lo,hi in zip(bound[:-1],bound[1:]):
 j=ix[lo:hi]; first=j[0]; v=a['duration'][j].astype(float)
 dur.append(dict(route=routes[a['route'][first]],continuity='Y' if a['continuous'][first] else 'N',
    participants=int(a['participants'][first]),fx=int(a['fx'][first]),period=['early','July'][period[first]],
    n=len(j),minimum=float(v.min()),q10=float(np.quantile(v,.1)),median=float(np.median(v)),q90=float(np.quantile(v,.9)),maximum=float(v.max()),mean=float(v.mean()),sd=float(v.std()),
    under_60_n=int((v<60).sum()),over_3600_n=int((v>3600).sum())))
pd.DataFrame(dur).to_csv(OUT/'duration_route_fx.csv',index=False)
# Full-data OLS controls, with temporal evaluation. The same design tests route-mixture alternative.
def design(j,mode):
    r=a['route'][j]; p=a['participants'][j].astype(float); f=a['fx'][j].astype(float)
    if mode=='route_only':return np.column_stack([np.ones(len(j)),r==1,r==2])
    return np.column_stack([np.ones(len(j)),r==1,r==2,p,f,a['continuous'][j],(r==1)*p,(r==2)*p])
fits=[]
for mode in ['route_only','route_participant_fx']:
 xtx=None; xty=None
 for lo in range(0,n,100000):
  j=np.arange(lo,min(lo+100000,n)); j=j[period[j]==0]; x=design(j,mode); y=a['duration'][j]
  xx=x.T@x; xy=x.T@y
  xtx=xx if xtx is None else xtx+xx; xty=xy if xty is None else xty+xy
 coef=np.linalg.lstsq(xtx,xty,rcond=None)[0]
 for per in [0,1]:
  ss=sy=sy2=nn=0.; ae=0.
  for lo in range(0,n,100000):
   j=np.arange(lo,min(lo+100000,n)); j=j[period[j]==per]; y=a['duration'][j].astype(float); pred=design(j,mode)@coef
   ss+=float(np.square(y-pred).sum());ae+=float(np.abs(y-pred).sum());sy+=y.sum();sy2+=np.square(y).sum();nn+=len(y)
  fits.append(dict(model=mode,period=['early','July'][per],n=int(nn),r2=1-ss/(sy2-sy*sy/nn),mae_seconds=ae/nn,rmse_seconds=(ss/nn)**.5,coefficients=coef.tolist()))
(OUT/'duration_models.json').write_text(json.dumps(fits,indent=2))
print(json.dumps(fits,indent=2),flush=True)
manifest={'records':n,'elapsed_seconds':time.monotonic()-start,'source':str(source),'size_bytes':source.stat().st_size,'mtime_ns':source.stat().st_mtime_ns,
 'method':'full census, exact conditional quantiles; MayJune timing excludes April30 and July31 partial dates; July descriptive validation',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'complete':True}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('DONE',flush=True)
