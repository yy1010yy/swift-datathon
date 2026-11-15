"""Earlier-fit exact-bank/corridor models for duration and currency choice."""
from pathlib import Path
import json,time
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
num=np.load(ROOT/'outputs/round2/a/numeric.npy',mmap_mode='r')
bank=np.load(ROOT/'outputs/round3/c/banks.npy',mmap_mode='r')
codes=pd.read_csv(OUT/'bank_codes.csv',dtype=str,keep_default_na=False);codes['bank_id']=codes.bank_id.astype(int);codes=codes.sort_values('bank_id')
assert len(num)==len(bank)==10000000
epoch=num['epoch'];train=(epoch>=1682899200)&(epoch<1688169600);test=(epoch>=1688169600)&(epoch<1690761600)
tr=np.flatnonzero(train);te=np.flatnonzero(test);start=time.monotonic();nb=len(codes)

def dense_effect(key,residual,idx,alpha):
    k=key[idx].astype('int64'); n=int(key.max())+1
    cnt=np.bincount(k,minlength=n); sm=np.bincount(k,weights=residual[idx],minlength=n)
    return sm/(cnt+alpha),cnt
def sparse_effect(key,residual,idx,alpha):
    k=key[idx].astype('int64'); u,inv=np.unique(k,return_inverse=True)
    cnt=np.bincount(inv);sm=np.bincount(inv,weights=residual[idx]);val=sm/(cnt+alpha)
    return u,val,cnt
def sparse_apply(keys,u,val):
    pos=np.searchsorted(u,keys);safe=np.minimum(pos,len(u)-1);ok=(pos<len(u))&(u[safe]==keys)
    out=np.zeros(len(keys));out[ok]=val[pos[ok]];return out,ok
def score_duration(name,pred):
    y=num['duration'][te].astype(float);ly=np.log(y); err=ly-pred;sec=np.exp(pred)
    return {'model':name,'n':len(te),'log_rmse':float(np.sqrt(np.mean(err*err))),
      'log_mae':float(np.mean(abs(err))),'log_r2':float(1-np.sum(err*err)/np.sum((ly-ly.mean())**2)),
      'seconds_mae_median_prediction':float(np.mean(abs(y-sec)))}

ylog=np.log(num['duration'].astype(float));global_log=float(ylog[tr].mean())
basekey=num['route'].astype('int64')*1000+num['p'].astype('int64')*30+num['fx'].astype('int64')
base_eff,base_n=dense_effect(basekey,ylog-global_log,tr,10);base=global_log+base_eff[basekey];res=ylog-base;duration=[]
duration.append(score_duration('route+participants+fx',base[te]))
countries=sorted(codes.country.unique());cmap={v:i for i,v in enumerate(countries)}
bc=np.array([cmap[v] for v in codes.country],dtype='int16');sc=bc[bank['sender']];rc=bc[bank['receiver']]
sce,_=dense_effect(sc,res,tr,1000);r1=res-sce[sc];rce,_=dense_effect(rc,r1,tr,1000)
country_pred=base+sce[sc]+rce[rc];duration.append(score_duration('base+sender_receiver_country',country_pred[te]))
se,_=dense_effect(bank['sender'],res,tr,100);r2=res-se[bank['sender']];re,_=dense_effect(bank['receiver'],r2,tr,100)
bank_pred=base+se[bank['sender']]+re[bank['receiver']];duration.append(score_duration('base+sender_receiver_bic',bank_pred[te]))
how=((((epoch//86400)+3)%7)*24+(epoch//3600)%24).astype('int16')
he,_=dense_effect(how,ylog-bank_pred,tr,1000);bank_hour=bank_pred+he[how]
duration.append(score_duration('base+bics+utc_hour_of_week',bank_hour[te]))
pair=bank['sender'].astype('int64')*nb+bank['receiver'].astype('int64')
u,pe,pc=sparse_effect(pair,ylog-bank_hour,tr,50);pa,known=sparse_apply(pair[te],u,pe)
duration.append(score_duration('base+bics+hour+pair',bank_hour[te]+pa))
pd.DataFrame(duration).to_csv(OUT/'duration_model_scores.csv',index=False)
stability=[]
def dense_stability(name,key,residual,min_n):
    n=int(key.max())+1;ktr=key[tr].astype('int64');kte=key[te].astype('int64')
    cn=np.bincount(ktr,minlength=n);cs=np.bincount(ktr,weights=residual[tr],minlength=n)
    tn=np.bincount(kte,minlength=n);ts=np.bincount(kte,weights=residual[te],minlength=n)
    ok=(cn>=min_n)&(tn>=min_n);a=cs[ok]/cn[ok];b=ts[ok]/tn[ok]
    stability.append({'effect':name,'min_n_each_period':min_n,'cells':int(ok.sum()),
      'correlation':float(np.corrcoef(a,b)[0,1]),'median_abs_change':float(np.median(abs(a-b)))})
dense_stability('sender_bic_log_residual',bank['sender'],res,500)
dense_stability('receiver_bic_after_sender_log_residual',bank['receiver'],r2,500)
# Pair comparison uses the residual after bank and hour effects, common exact pairs only.
ut,vt,ct=sparse_effect(pair,ylog-bank_hour,te,0);common=np.intersect1d(u,ut)
ip=np.searchsorted(u,common);it=np.searchsorted(ut,common);ok=(pc[ip]>=100)&(ct[it]>=100)
stability.append({'effect':'directed_pair_after_bics_hour_log_residual','min_n_each_period':100,'cells':int(ok.sum()),
 'correlation':float(np.corrcoef(pe[ip][ok],vt[it][ok])[0,1]),
 'median_abs_change':float(np.median(abs(pe[ip][ok]-vt[it][ok])))})
pd.DataFrame(stability).to_csv(OUT/'duration_effect_stability.csv',index=False)

curr_names=np.unique(num['currency']);curr=np.searchsorted(curr_names,num['currency']).astype('int16');nc=len(curr_names)
def fit_modes(key,topn=3):
    combo=key[tr].astype('int64')*nc+curr[tr].astype('int64');cu,ct=np.unique(combo,return_counts=True)
    g=cu//nc;c=(cu%nc).astype('int16');order=np.lexsort((c,-ct,g));g=g[order];c=c[order];ct=ct[order]
    starts=np.r_[0,np.flatnonzero(np.diff(g))+1];ends=np.r_[starts[1:],len(g)];ug=g[starts];total=np.add.reduceat(ct,starts)
    modes=np.full((len(ug),topn),-1,dtype='int16')
    for rank in range(topn):
        pos=starts+rank;ok=pos<ends;modes[ok,rank]=c[pos[ok]]
    return ug,modes,total
def apply_modes(key,u,modes,total):
    k=key[te].astype('int64');pos=np.searchsorted(u,k);safe=np.minimum(pos,len(u)-1);ok=(pos<len(u))&(u[safe]==k)
    mm=np.full((len(te),modes.shape[1]),-1,dtype='int16');nn=np.zeros(len(te),dtype='int64')
    mm[ok]=modes[pos[ok]];nn[ok]=total[pos[ok]];return mm,nn,ok
def currency_row(name,m,counts,coverage_mask=None):
    actual=curr[te];known=m[:,0]>=0;cov=known if coverage_mask is None else coverage_mask
    return {'model':name,'test_n':len(te),'coverage_n':int(cov.sum()),
      'top1_correct':int((cov&(m[:,0]==actual)).sum()),'top1_accuracy_all':float((cov&(m[:,0]==actual)).sum()/len(te)),
      'top1_accuracy_covered':float((m[cov,0]==actual[cov]).mean()) if cov.any() else None,
      'top2_accuracy_all':float((cov&((m[:,0]==actual)|(m[:,1]==actual))).sum()/len(te)),
      'top3_accuracy_all':float((cov&((m[:,0]==actual)|(m[:,1]==actual)|(m[:,2]==actual))).sum()/len(te)),
      'median_train_cell_n_covered':float(np.median(counts[cov])) if cov.any() else None}

globalkey=np.zeros(len(num),dtype='int8');ug,mg,ng=fit_modes(globalkey);gm,gn,gok=apply_modes(globalkey,ug,mg,ng)
usc,msc,nsc=fit_modes(sc);smc,snc,sokc=apply_modes(sc,usc,msc,nsc)
us,ms,ns=fit_modes(bank['sender']);smb,snb,sokb=apply_modes(bank['sender'],us,ms,ns)
ur,mr,nr=fit_modes(bank['receiver']);rmb,rnb,rokb=apply_modes(bank['receiver'],ur,mr,nr)
urc,mrc,nrc=fit_modes(rc);rmc,rnc,rokc=apply_modes(rc,urc,mrc,nrc)
up,mp,npair=fit_modes(pair);pmb,pnb,pok=apply_modes(pair,up,mp,npair)
currency_scores=[currency_row('global',gm,gn),currency_row('sender_country',smc,snc),currency_row('sender_bic',smb,snb),currency_row('receiver_country',rmc,rnc),currency_row('receiver_bic',rmb,rnb)]
actual=curr[te]
for minimum in [5,20,100]:
    use=pok&(pnb>=minimum);hy=smb.copy();hy[use]=pmb[use]
    currency_scores.append(currency_row(f'pair_mode_n>={minimum}_else_sender_bic',hy,np.where(use,pnb,snb)))
pd.DataFrame(currency_scores).to_csv(OUT/'currency_model_scores.csv',index=False)
sender_miss=smb[:,0]!=actual;alt=[]
for name,m,n,ok in [('global',gm,gn,gok),('receiver_country',rmc,rnc,rokc),('receiver_bic',rmb,rnb,rokb),('pair',pmb,pnb,pok)]:
    for minimum in [1,5,20,100]:
        use=sender_miss&ok&(n>=minimum)
        alt.append({'model':name,'min_train_n':minimum,'sender_mode_miss_n':int(sender_miss.sum()),
         'covered_miss_n':int(use.sum()),'correct_n':int((use&(m[:,0]==actual)).sum()),
         'accuracy_covered':float((m[use,0]==actual[use]).mean()) if use.any() else None})
pd.DataFrame(alt).to_csv(OUT/'alternative_currency_scores.csv',index=False)
summary={'status':'complete','train_rows':len(tr),'july_rows':len(te),'currencies':nc,'banks':nb,
 'duration_pair_train_cells':len(u),'duration_pair_july_known':int(known.sum()),'elapsed_seconds':time.monotonic()-start,
 'limits':['Pre-July/July is retrospective validation.','Target encodings show prediction, not causal direction.',
 'Pair modes fall back to sender BIC and are thresholded to expose sparsity.','Duration is evaluated as conditional mean on log scale; mixtures remain possible.']}
(OUT/'duration_currency_manifest.json').write_text(json.dumps(summary,indent=2));print(pd.DataFrame(duration).to_string(index=False));print(pd.DataFrame(currency_scores).to_string(index=False));print(pd.DataFrame(alt).to_string(index=False));print(json.dumps(summary,indent=2))
