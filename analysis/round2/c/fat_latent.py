"""Latent decimal-shift alternatives using C's independently fitted baseline scale.

No observed counterfactual amount is asserted. Normal baseline is an approximation.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import json
P=Path(__file__).resolve().parent
model=json.loads((P/'amount_model.json').read_text());sigma=model['train']['log_rmse']
d=pd.read_csv(P/'labelled.csv',dtype=str,keep_default_na=False);d=d[d.anomaly_type.eq('FAT_FINGER_MISTAKE')].copy()
d['period']=np.where(d.epoch_seconds.astype('int64')<1688169600,'early','July')
d['residual']=np.log(pd.to_numeric(d.usd_amount))-d.currency_code.map(model['currency_intercepts'])-d.ordering_type.eq('B')*model['sender_beta']-d.beneficiary_type.eq('B')*model['receiver_beta']
d.to_csv(P/'fat_residual_cases.csv',index=False)
x=d.loc[d.period.eq('early'),'residual'].to_numpy();y=d.loc[d.period.eq('July'),'residual'].to_numpy()
def normal_logpdf(values,means,sd):return -0.5*((values[:,None]-np.array(means)[None,:])/sd)**2-np.log(sd*np.sqrt(2*np.pi))
def logmix(logpdf,weights):
    z=logpdf+np.log(np.maximum(weights,1e-300));m=z.max(axis=1)
    return m+np.log(np.exp(z-m[:,None]).sum(axis=1))
results=[]
def add(name,means,sd,weights,parameters):
    tr=logmix(normal_logpdf(x,means,sd),weights);te=logmix(normal_logpdf(y,means,sd),weights)
    results.append(dict(name=name,means=list(map(float,means)),sd=float(sd),weights=list(map(float,weights)),
       parameters=parameters,early_n=len(x),July_n=len(y),early_mean_loglik=float(tr.mean()),
       July_mean_loglik=float(te.mean()),early_AIC=float(2*parameters-2*tr.sum())))
add('unchanged_baseline',[0],sigma,[1],0)
add('free_normal',[x.mean()],x.std(),[1],2)
for maximum in [1,2,3,4,6]:
    for zero in [False,True]:
        ks=np.array([k for k in range(-maximum,maximum+1) if zero or k!=0]);means=ks*np.log(10)
        pdf=normal_logpdf(x,means,sigma);w=np.ones(len(ks))/len(ks)
        for iteration in range(2000):
            z=pdf+np.log(np.maximum(w,1e-300));z-=z.max(axis=1)[:,None]
            responsibilities=np.exp(z);responsibilities/=responsibilities.sum(axis=1)[:,None]
            updated=responsibilities.mean(axis=0)
            if np.max(np.abs(updated-w))<1e-11:break
            w=updated
        add(f'EM_decimal_{maximum}_withzero_{zero}',means,sigma,w,len(ks)-1)
        results[-1]['integer_shifts']=ks.tolist();results[-1]['iterations']=iteration+1
        add(f'uniform_decimal_{maximum}_withzero_{zero}',means,sigma,np.ones(len(ks))/len(ks),0)
pd.DataFrame([{k:v for k,v in r.items() if k not in ['means','weights','integer_shifts']} for r in results]).to_csv(P/'fat_latent_comparison.csv',index=False)
meta={'baseline_sigma':sigma,'early_residual_mean':float(x.mean()),'early_residual_sd':float(x.std()),
      'July_residual_mean':float(y.mean()),'July_residual_sd':float(y.std()),
      'models':results,'limits':['Baseline normality approximate; multiple mixtures can fit.',
      'FAT labels used to choose mixture, July retrospective model checking.',
      'No row-level original amount recovered; latent powers are distributional explanations.']}
(P/'fat_latent.json').write_text(json.dumps(meta,indent=2));print(json.dumps({k:v for k,v in meta.items() if k!='models'},indent=2))
print(pd.read_csv(P/'fat_latent_comparison.csv').sort_values('July_mean_loglik',ascending=False).to_string(index=False))
