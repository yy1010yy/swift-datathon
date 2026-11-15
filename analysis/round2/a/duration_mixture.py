"""Fit actual generative duration distributions; score July exact discrete counts."""
from pathlib import Path
import math,json
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a'
x=np.load(ROOT/'outputs/round2/a/numeric.npy',mmap_mode='r')
dur=x['duration'].copy();early=x['epoch'].copy()<1688169600;rt=x['route'].copy();p=x['p'].copy();q=x['q'].copy();del x
bins=np.arange(1,int(dur.max())+1); z=np.log(bins)
def density(z,mu,sd):return np.exp(-.5*((z-mu)/sd)**2)/sd/np.sqrt(2*np.pi)
def cdf(z,mu,sd):return np.array([.5*(1+math.erf((v-mu)/sd/np.sqrt(2))) for v in z])
results=[];records=[]
for route,participants in [(0,2),(1,3),(1,4),(2,3)]:
 mask=(rt==route)&(p==participants)&(q==1)
 train=np.bincount(dur[mask&early],minlength=len(bins)+1)[1:]
 test=np.bincount(dur[mask&~early],minlength=len(bins)+1)[1:]
 mu=np.average(z,weights=train); sd=np.sqrt(np.average((z-mu)**2,weights=train))
 mus=np.array([3.,7.]);sds=np.array([.6,.7]);mix=np.array([.6,.4])
 for iteration in range(200):
  likelihood=np.stack([mix[j]*density(z,mus[j],sds[j]) for j in range(2)])
  responsibility=likelihood/np.maximum(likelihood.sum(axis=0),1e-300)
  weighted=responsibility*train;totals=weighted.sum(axis=1)
  newmus=(weighted*z).sum(axis=1)/totals
  newsds=np.sqrt((weighted*(z-newmus[:,None])**2).sum(axis=1)/totals)
  newmix=totals/train.sum()
  change=np.max(abs(newmus-mus))+np.max(abs(newmix-mix))
  mus,sds,mix=newmus,newsds,newmix
  if change<1e-10:break
 upper=np.log(bins+.5);lower=np.log(np.maximum(bins-.5,.01))
 single=cdf(upper,mu,sd)-cdf(lower,mu,sd)
 mixture=sum(mix[j]*(cdf(upper,mus[j],sds[j])-cdf(lower,mus[j],sds[j])) for j in range(2))
 mean=np.average(bins,weights=train)
 exponential=np.exp(-(bins-.5)/mean)-np.exp(-(bins+.5)/mean)
 for model,prob in [('single_exponential',exponential),('single_lognormal',single),('two_lognormals',mixture)]:
  nll=-float((test*np.log(np.maximum(prob,1e-300))).sum()/test.sum())
  tv=.5*float(np.abs(test/test.sum()-prob).sum())
  results.append([route,participants,model,int(train.sum()),int(test.sum()),nll,tv])
 params={'route':route,'participants':participants,'mix':mix.tolist(),'logmeans':mus.tolist(),'logstds':sds.tolist(),'single_logmean':mu,'single_logstd':sd}
 records.append(params)
 pd.DataFrame({'duration_seconds':bins,'early_observed':train,'july_observed':test,'mixture_july_expected':mixture*test.sum(),'single_july_expected':single*test.sum()}).to_csv(ROOT/f'outputs/round2/a/duration_model_r{route}_p{participants}.csv',index=False)
table=pd.DataFrame(results,columns=['route','participants','model','early_n','july_n','july_nll_nats','july_total_variation'])
table.to_csv(OUT/'duration_model_scores.csv',index=False)
(OUT/'duration_model_parameters.json').write_text(json.dumps(records,indent=2))
print(table.to_string(index=False));print(json.dumps(records,indent=2))
print('Two lognormals are identifiable as a fitted mixture, not proof of actual generator families or which bank delayed.')
