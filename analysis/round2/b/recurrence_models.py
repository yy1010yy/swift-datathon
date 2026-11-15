"""Candidate waiting-time and multiplicative growth distributions; full cached histories."""
from pathlib import Path
import math,json
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent
d=pd.read_csv(OUT/'history_lag_rows.csv',keep_default_na=False)
raw=pd.read_csv(OUT.parent/'c/relevant_pair_history.csv.gz',usecols=['source_record','epoch_seconds','ordering_type','beneficiary_type'],dtype=str,keep_default_na=False)
raw.source_record=raw.source_record.astype('int64');raw['epoch']=raw.epoch_seconds.astype('int64')
d=d.merge(raw,on='source_record',validate='one_to_one');d=d[d.with_prior]
d['seconds_since_last']=pd.to_numeric(d.seconds_since_last,errors='raise')
d['ratio_to_last']=pd.to_numeric(d.ratio_to_last,errors='raise')
def ks(values,cdf):
 v=np.sort(values);f=np.asarray([cdf(x) for x in v]);n=len(v)
 return float(max(np.max(np.arange(1,n+1)/n-f),np.max(f-np.arange(n)/n)))
results=[]
romance=d[d.label.eq('ROMANCE_SCAM')]
early=romance[romance.epoch<1688169600]
lag_mu=float(early.seconds_since_last.mean());log_mu=float(np.log(early.ratio_to_last).mean());log_sd=float(np.log(early.ratio_to_last).std(ddof=0))
waitlog=np.log(early.seconds_since_last);wait_logmu=float(waitlog.mean());wait_logsd=float(waitlog.std(ddof=0))
laplace_location=float(np.log(early.ratio_to_last).median());laplace_scale=float(np.abs(np.log(early.ratio_to_last)-laplace_location).mean())
for label,sub in [('ROMANCE_SCAM',romance),('blank_selected_pairs',d[d.label.eq('')])]:
 for period,mask in [('early',sub.epoch<1688169600),('July',sub.epoch>=1688169600)]:
  for party,g in [('ALL',sub[mask])]+list(sub[mask].groupby('party')):
   if len(g)<10:continue
   lag=g.seconds_since_last.to_numpy(float);log=np.log(g.ratio_to_last.to_numpy(float))
   normal_cdf=lambda x:.5*(1+math.erf((x-log_mu)/(log_sd*math.sqrt(2))))
   record=dict(label=label,period=period,party=party,n=len(g),lag_mean=float(lag.mean()),lag_sd=float(lag.std()),
    logratio_mean=float(log.mean()),logratio_sd=float(log.std()),
    lag_ks_early_exp=ks(lag,lambda x:1-math.exp(-x/lag_mu)),logratio_ks_early_normal=ks(log,normal_cdf),
    lag_ks_exp300=ks(lag,lambda x:1-math.exp(-x/300)),
    logratio_ks_normal_04_04=ks(log,lambda x:.5*(1+math.erf((x-.4)/(.4*math.sqrt(2))))),
    lag_exponential_nll=float(np.mean(np.log(lag_mu)+lag/lag_mu)),
    lag_gamma_shape2_nll=float(np.mean(-np.log(lag)+2*np.log(lag_mu/2)+2*lag/lag_mu)),
    lag_lognormal_nll=float(np.mean(np.log(lag)+np.log(wait_logsd*math.sqrt(2*math.pi))+.5*((np.log(lag)-wait_logmu)/wait_logsd)**2)),
    logratio_laplace_nll=float(np.mean(np.log(2*laplace_scale)+np.abs(log-laplace_location)/laplace_scale)),
    logratio_normal_nll=float(np.mean(np.log(log_sd*math.sqrt(2*math.pi))+.5*((log-log_mu)/log_sd)**2)))
   results.append(record)
z=pd.DataFrame(results);z.to_csv(OUT/'recurrence_model_scores.csv',index=False)
(OUT/'recurrence_model_parameters.json').write_text(json.dumps({'trained_population':'preJuly observedprior romance labels',
 'n':len(early),'exponential_mean_seconds':lag_mu,'normal_logratio_mean':log_mu,'normal_logratio_sd':log_sd,
 'limits':'KS descriptive with clustered pairs and fitted early parameters; no iid significance claim. Same-pair selected controls are not representative.'},indent=2))
print(z.to_string(index=False))
