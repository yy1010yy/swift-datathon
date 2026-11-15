"""Learn FX zones only from early direct routes; test all longer routes and July."""
from pathlib import Path
from collections import Counter
import gzip,time,json
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a';CACHE=ROOT/'outputs/round2/a'
parents={};observed_training=set();start=time.monotonic();n=0
def find(v):
 if v not in parents:parents[v]=v
 while parents[v]!=v:parents[v]=parents[parents[v]];v=parents[v]
 return v
cache=CACHE/'fx_zone_routes.csv.gz'
with gzip.open(cache,'wt',newline='',encoding='utf-8') as dest:
 for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=['bic8_path','currency_conversion_count','epoch_seconds','continuity_qflag','transaction_type_code'],dtype=str,keep_default_na=False,chunksize=100000):
  early=d.epoch_seconds.astype('int64')<1688169600
  parsed={v:';'.join(w[4:6] for w in v.split(';') if len(w)==8) for v in d.bic8_path.unique()}
  seq=d.bic8_path.map(parsed)
  for s,f in zip(seq[early & d.transaction_type_code.eq('Direct')],d.currency_conversion_count[early & d.transaction_type_code.eq('Direct')]):
   a,b=s.split(';');observed_training.update([a,b]);find(a);find(b)
   if f=='0':parents[find(b)]=find(a)
  t=pd.DataFrame({'early':early,'route':d.transaction_type_code,'q':d.continuity_qflag,'fx':d.currency_conversion_count,'countries':seq})
  t.to_csv(dest,index=False,header=n==0);n+=len(d)
  if n%1000000==0:print('extract',n,round(time.monotonic()-start,1),flush=True)
groups={v:find(v) for v in observed_training};totals=Counter()
for d in pd.read_csv(cache,keep_default_na=False,dtype=str,chunksize=100000):
 def prediction(s):
  a=s.split(';')
  if any(v not in groups for v in a):return -1
  return sum(groups[u]!=groups[v] for u,v in zip(a,a[1:]))
 pred=d.countries.map({s:prediction(s) for s in d.countries.unique()})
 t=pd.DataFrame({'early':d.early,'route':d.route,'q':d.q,'known':pred.ge(0),'equal':pred.eq(d.fx.astype(int)),'residual':d.fx.astype(int)-pred})
 totals.update(t.value_counts(sort=False).to_dict())
table=pd.DataFrame([list(k)+[v] for k,v in totals.items()],columns=list(t.columns)+['n'])
table.to_csv(OUT/'fx_zone_validation.csv',index=False)
pd.DataFrame(sorted(groups.items()),columns=['country_like_code','training_zone']).to_csv(OUT/'fx_training_zones.csv',index=False)
print(table.to_string(index=False));print('ALL ROWS',n,'training country codes',len(groups),'SECONDS',time.monotonic()-start)
