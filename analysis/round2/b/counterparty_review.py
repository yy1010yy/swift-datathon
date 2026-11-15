"""Independent population pair regrouping from C's shared full raw partition cache.

Full strings define identity; partition hashes are not pair keys. Grouping, strict
timestamp predecessor joins and model calculations reimplemented without C result input.
"""
from pathlib import Path
from collections import Counter,defaultdict
import math,json,time
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
CACHE=ROOT/'outputs/round2/c/counterparty_population'
hist=Counter();intervals=defaultdict(list);cohorts=Counter();n=pairs=first_timestamp_rows=ties=mixed=0;start=time.monotonic()
for path in sorted(CACHE.glob('part_*.csv')):
 d=pd.read_csv(path,dtype={'sender':str,'receiver':str,'party':str,'epoch':'int64'},keep_default_na=False)
 keys=['sender','receiver'];g=d.groupby(keys,sort=False)
 pair=g.agg(n=('epoch','size'),first=('epoch','min'),last=('epoch','max'),variants=('party','nunique'),party=('party','first'))
 pair.loc[pair.variants.gt(1),'party']='MIXED'
 d=d.merge(pair[['party','first']].rename(columns={'party':'pair_party'}),on=keys,validate='many_to_one')
 d['early']=d.epoch<1688169600
 periods=d.groupby(keys+['early']).size().unstack('early',fill_value=0)
 for party,p in pair.groupby('party'):
  for size,count in p.n.value_counts().items():hist[(party,'full',int(size))]+=int(count)
  for early,period in [(True,'early'),(False,'July')]:
   values=periods.reindex(p.index)[early]
   for size,count in values[values>0].value_counts().items():hist[(party,period,int(size))]+=int(count)
  values=periods.reindex(p.index)
  cohorts[(party,'early_only')]+=int(((values[True]>0)&(values[False]==0)).sum())
  cohorts[(party,'both_periods')]+=int(((values[True]>0)&(values[False]>0)).sum())
  cohorts[(party,'July_new')]+=int(((values[True]==0)&(values[False]>0)).sum())
 unique=d[keys+['epoch']].drop_duplicates().sort_values(keys+['epoch'])
 unique['previous_epoch']=unique.groupby(keys,sort=False).epoch.shift()
 d=d.merge(unique,on=keys+['epoch'],validate='many_to_one')
 d['lag']=d.epoch-d.previous_epoch
 first_timestamp_rows+=int(d.previous_epoch.isna().sum());ties+=len(d)-len(unique)
 for (party,early),s in d[d.previous_epoch.notna()].groupby(['pair_party','early']):
  arr=s.lag.to_numpy(dtype='i8');assert np.all(arr>0)
  intervals[(party,'early' if early else 'July')].append(arr)
 n+=len(d);pairs+=len(pair);mixed+=int(pair.variants.gt(1).sum())
 print(path.name,n,pairs,round(time.monotonic()-start,1),flush=True)
assert n==9992994
counts=pd.DataFrame([dict(party=p,period=t,payments_per_pair=k,pairs=v) for (p,t,k),v in hist.items()]);counts.to_csv(OUT/'counterparty_count_histogram.csv',index=False)
pd.DataFrame([dict(party=p,cohort=t,pairs=n) for (p,t),n in cohorts.items()]).to_csv(OUT/'counterparty_cohorts.csv',index=False)
summary=[];countfits=[]
for (party,period),s in counts.groupby(['party','period']):
 npairs=s.pairs.sum();payments=(s.pairs*s.payments_per_pair).sum();mean=payments/npairs
 lo=1e-12;hi=max(1,2*mean)
 for _ in range(100):
  lam=(lo+hi)/2
  if lam/(-math.expm1(-lam))<mean:lo=lam
  else:hi=lam
 lam=(lo+hi)/2;geo=1/mean
 summary.append(dict(party=party,period=period,pairs=int(npairs),payments=int(payments),mean=float(mean),singletons=int(s.loc[s.payments_per_pair.eq(1),'pairs'].sum()),repeated_pairs=int(s.loc[s.payments_per_pair.gt(1),'pairs'].sum()),max_payments=int(s.payments_per_pair.max())))
 for model in ['zt_poisson','positive_geometric']:
  observed=[];expected=[]
  for left,right in [(1,1),(2,2),(3,3),(4,4),(5,5),(6,10),(11,20),(21,50),(51,None)]:
   ob=s.loc[(s.payments_per_pair>=left)&((s.payments_per_pair<=right) if right else True),'pairs'].sum()
   if model=='positive_geometric':pr=(1-geo)**(left-1)-((1-geo)**right if right else 0)
   else:
    def poisson(k):return math.exp(-lam+k*math.log(lam)-math.lgamma(k+1))/(-math.expm1(-lam))
    pr=sum(poisson(k) for k in range(left,right+1)) if right else max(0,1-sum(poisson(k) for k in range(1,left)))
   observed.append(ob);expected.append(npairs*pr)
  observed=np.asarray(observed);expected=np.asarray(expected);eligible=expected>=10
  countfits.append(dict(party=party,period=period,model=model,parameter=lam if model=='zt_poisson' else geo,
   tv=float(abs(observed-expected).sum()/npairs/2),pearson=float(((observed[eligible]-expected[eligible])**2/expected[eligible]).sum()),cells_expected_ge10=int(eligible.sum())))
pd.DataFrame(summary).to_csv(OUT/'counterparty_count_summary.csv',index=False);pd.DataFrame(countfits).to_csv(OUT/'counterparty_count_models.csv',index=False)
arrays={k:np.concatenate(v) for k,v in intervals.items()};assert sum(map(len,arrays.values()))+first_timestamp_rows==n
isummary=[];ifits=[];bins=np.array([0,1,10,60,300,1800,3600,21600,86400,604800,np.inf])
for (party,period),arr in arrays.items():
 q=np.quantile(arr,[.01,.1,.5,.9,.99]);scale=float(arrays[(party,'early')].mean())
 isummary.append(dict(party=party,period=period,n=len(arr),mean=float(arr.mean()),sd=float(arr.std()),p01=q[0],p10=q[1],median=q[2],p90=q[3],p99=q[4]))
 obs=np.histogram(arr,bins)[0];probs=np.exp(-bins[:-1]/scale)-np.exp(-bins[1:]/scale);exp=len(arr)*probs
 ifits.append(dict(party=party,period=period,n=len(arr),earlier_mean_seconds=scale,tv=float(abs(obs-exp).sum()/len(arr)/2),pearson=float(((obs[exp>=10]-exp[exp>=10])**2/exp[exp>=10]).sum())))
pd.DataFrame(isummary).to_csv(OUT/'counterparty_interval_summary.csv',index=False);pd.DataFrame(ifits).to_csv(OUT/'counterparty_interval_models.csv',index=False)
meta={'records':n,'pairs':pairs,'mixed_type_pairs':mixed,'first_timestamp_rows_without_prior':first_timestamp_rows,'strict_prior_rows':sum(map(len,arrays.values())),'extra_same_timestamp_rows':ties,
 'elapsed_seconds':time.monotonic()-start,'scope':'Independent exact grouping and predecessor calculation; shared C raw fullpopulation partition extraction; only no-recorded-label rows.'}
(OUT/'counterparty_initial.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2));print(pd.DataFrame(summary).to_string(index=False));print(pd.DataFrame(countfits).to_string(index=False));print(pd.DataFrame(ifits).to_string(index=False))
