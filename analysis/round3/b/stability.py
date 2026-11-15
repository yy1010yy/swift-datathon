"""Stability and boundary checks for the B bank/network initial."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round3/b';CACHE=ROOT/'outputs/round3/b'
x=np.load(CACHE/'rows.npy',mmap_mode='r');B=len(json.loads((CACHE/'bic_map.json').read_text()));cut=1688169600
early=x['epoch']<cut;july=~early;pair=x['sender'].astype('i8')*B+x['receiver'];nd=x['route']>0
def rates(key,y,mask):
 k=key[mask].astype('i8');v=y[mask].astype('i8');uk,n=np.unique(k,return_counts=True);up,c=np.unique(k[v==1],return_counts=True)
 p=np.searchsorted(up,uk);hit=p<len(up);good=np.zeros(len(uk),bool);good[hit]=up[p[hit]]==uk[hit];yes=np.zeros(len(uk),'i8');yes[good]=c[p[good]]
 return uk,n,yes/n
rows=[]
for name,key in [('sender_bic',x['sender']),('receiver_bic',x['receiver']),('bic_pair',pair)]:
 a,an,ar=rates(key,(x['route']==2).astype('u1'),early&nd);b,bn,br=rates(key,(x['route']==2).astype('u1'),july&nd)
 common=np.intersect1d(a,b);ia=np.searchsorted(a,common);ib=np.searchsorted(b,common)
 for threshold in [20,100,1000]:
  m=(an[ia]>=threshold)&(bn[ib]>=threshold);w=bn[ib][m]
  rows.append({'model':name,'min_each_period':threshold,'cells':int(m.sum()),'july_rows':int(w.sum()),
   'rate_correlation':float(np.corrcoef(ar[ia][m],br[ib][m])[0,1]) if m.sum()>1 else np.nan,
   'weighted_abs_rate_change':float(np.average(abs(ar[ia][m]-br[ib][m]),weights=w)) if m.any() else np.nan,
   'early_rate_min':float(ar[ia][m].min()) if m.any() else np.nan,'early_rate_max':float(ar[ia][m].max()) if m.any() else np.nan,
   'early_near_deterministic_share':float(((ar[ia][m]<.01)|(ar[ia][m]>.99)).mean()) if m.any() else np.nan})
pd.DataFrame(rows).to_csv(OUT/'covered_stability.csv',index=False)

# Sender-bank residual-effect temporal stability after fixed known baselines.
def groupmean(key,y,mask):
 k=key[mask].astype('i8');v=y[mask].astype('f8');o=np.argsort(k,kind='stable');sk=k[o];sv=v[o];st=np.r_[0,np.flatnonzero(sk[1:]!=sk[:-1])+1]
 return sk[st],np.diff(np.r_[st,len(sk)]),np.add.reduceat(sv,st)/np.diff(np.r_[st,len(sk)])
def baseline_residual(y,base,mask):
 k,n,m=groupmean(base,y,mask);p=np.searchsorted(k,base[mask]);return y[mask]-m[p]
res=[]
for outcome,y,base in [('amount',x['log_amount'].astype('f8'),x['currency'].astype('i8')*4+x['party']),
 ('duration',x['log_duration'].astype('f8'),((x['route'].astype('i8')*2+x['continuous'])*32+x['participants'])*32+x['fx'])]:
 use=(x['labelled']==0) if outcome=='amount' else np.ones(len(x),bool)
 # Period-specific baselines make this a stability of relative bank effects, not level drift.
 r=np.empty(len(x),'f8');r[early&use]=baseline_residual(y,base,early&use);r[july&use]=baseline_residual(y,base,july&use)
 a,an,am=groupmean(x['sender'],r,early&use);b,bn,bm=groupmean(x['sender'],r,july&use);common=np.intersect1d(a,b);ia=np.searchsorted(a,common);ib=np.searchsorted(b,common)
 for th in [100,1000]:
  m=(an[ia]>=th)&(bn[ib]>=th);res.append({'outcome':outcome,'min_each_period':th,'banks':int(m.sum()),'july_rows':int(bn[ib][m].sum()),
   'effect_correlation':float(np.corrcoef(am[ia][m],bm[ib][m])[0,1]),'weighted_abs_effect_change':float(np.average(abs(am[ia][m]-bm[ib][m]),weights=bn[ib][m]))})
pd.DataFrame(res).to_csv(OUT/'sender_effect_stability.csv',index=False)

# First-intermediary marginal stability, hub overlap, endpoint equality and route dependence.
mid=x['firstmid'];has=mid!=np.iinfo('u2').max
def dist(mask):return np.bincount(mid[mask],minlength=B).astype('f8')
e=dist(early&has);j=dist(july&has);ep=e/e.sum();jp=j/j.sum();active=(e>=100)&(j>=100)
route=[]
for v,name in [(1,'Indirect'),(2,'Covered')]:
 z=dist(has&(x['route']==v));route.append((name,z/z.sum()))
network={'status':'complete','early_firstmid_rows':int(e.sum()),'july_firstmid_rows':int(j.sum()),
 'early_july_total_variation':float(.5*abs(ep-jp).sum()),'active_bic_count_ge100_each':int(active.sum()),
 'active_rate_correlation':float(np.corrcoef(ep[active],jp[active])[0,1]),
 'top10_overlap':len(set(np.argsort(e)[-10:])&set(np.argsort(j)[-10:])),
 'firstmid_equals_sender':int((has&(mid==x['sender'])).sum()),'firstmid_equals_receiver':int((has&(mid==x['receiver'])).sum()),
 'indirect_covered_mid_distribution_tv':float(.5*abs(route[0][1]-route[1][1]).sum())}
(OUT/'network_stability.json').write_text(json.dumps(network,indent=2));print(pd.DataFrame(rows).to_string(index=False));print(pd.DataFrame(res).to_string(index=False));print(json.dumps(network,indent=2))
