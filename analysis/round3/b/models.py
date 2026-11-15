"""Earlier-fit/later-score bank, corridor, timing and intermediary models."""
from pathlib import Path
import json,time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round3/b';CACHE=ROOT/'outputs/round3/b'
x=np.load(CACHE/'rows.npy',mmap_mode='r'); B=len(json.loads((CACHE/'bic_map.json').read_text()))
C=155; cutoff=1688169600; may1=1682899200; jul31=1690761600; sentinel=np.iinfo('u2').max
early=x['epoch']<cutoff;july=x['epoch']>=cutoff

def lookup(keys,vals,q,default=0.0):
    pos=np.searchsorted(keys,q);ok=pos<len(keys);good=np.zeros(len(q),bool);good[ok]=keys[pos[ok]]==q[ok]
    out=np.full(len(q),default,dtype='f8');out[good]=vals[pos[good]];return out,good

def cat_score(name,y,tr,te,key=None,K=None,alpha=100.0):
    yt=y[tr].astype('i8');yv=y[te].astype('i8');K=int(K or (max(int(yt.max()),int(yv.max()))+1))
    gy=np.bincount(yt,minlength=K).astype('f8');gp=(gy+.5)/(gy.sum()+.5*K)
    if key is None:
        p=gp[yv];pred=np.full(len(yv),int(np.argmax(gp)));known=np.ones(len(yv),bool);cells=1
    else:
        kt=key[tr].astype('i8');kv=key[te].astype('i8')
        uk,tot=np.unique(kt,return_counts=True);tot=tot.astype('f8')
        comp=kt*K+yt;uc,cnt=np.unique(comp,return_counts=True);cnt=cnt.astype('f8')
        joint,_=lookup(uc,cnt,kv*K+yv,0);den,known=lookup(uk,tot,kv,0)
        p=(joint+alpha*gp[yv])/(den+alpha);p[~known]=gp[yv[~known]]
        cy=uc%K;ck=uc//K;order=np.lexsort((cy,-cnt,ck));sck=ck[order];first=np.r_[True,sck[1:]!=sck[:-1]]
        mk=sck[first];my=cy[order][first];pred=np.full(len(yv),int(np.argmax(gp)))
        pos=np.searchsorted(mk,kv);ok=pos<len(mk);hit=np.zeros(len(kv),bool);hit[ok]=mk[pos[ok]]==kv[ok];pred[hit]=my[pos[hit]];cells=len(uk)
    return {'model':name,'train_n':int(tr.sum()),'test_n':int(te.sum()),'cells':int(cells),'alpha':alpha,
      'test_nll':float(-np.log(np.maximum(p,1e-300)).mean()),'test_accuracy':float((pred==yv).mean()),
      'known_key_share':float(known.mean()),'mean_true_probability':float(p.mean())}

def means(keys,y,mask):
    k=keys[mask].astype('i8');v=y[mask].astype('f8');order=np.argsort(k,kind='stable');ks=k[order];vs=v[order]
    starts=np.r_[0,np.flatnonzero(ks[1:]!=ks[:-1])+1];return ks[starts],np.add.reduceat(vs,starts),np.diff(np.r_[starts,len(ks)])

def continuous_scores(label,y,tr,te,basekey,extras,alpha=100.0):
    bk,bs,bn=means(basekey,y,tr);bm=bs/bn
    btr,_=lookup(bk,bm,basekey[tr].astype('i8'),float(y[tr].mean()));bte,_=lookup(bk,bm,basekey[te].astype('i8'),float(y[tr].mean()))
    resid=y[tr]-btr;rows=[{'outcome':label,'model':'baseline','train_n':int(tr.sum()),'test_n':int(te.sum()),'cells':len(bk),'alpha':0,
      'test_rmse':float(np.sqrt(np.mean((y[te]-bte)**2))),'test_mae':float(np.mean(abs(y[te]-bte))),'known_key_share':1.0}]
    for name,key in extras:
        gk,gs,gn=means(key,resid,np.ones(len(resid),bool)) if len(key)==len(resid) else (None,None,None)
        # extras are supplied as full arrays; fit against train residual directly.
        if len(key)!=len(resid):
            kt=key[tr].astype('i8');order=np.argsort(kt,kind='stable');sk=kt[order];rv=resid[order]
            st=np.r_[0,np.flatnonzero(sk[1:]!=sk[:-1])+1];gk=sk[st];gs=np.add.reduceat(rv,st);gn=np.diff(np.r_[st,len(sk)])
        corr=(gs/(gn+alpha));ct,known=lookup(gk,corr,key[te].astype('i8'),0)
        pred=bte+ct
        rows.append({'outcome':label,'model':name,'train_n':int(tr.sum()),'test_n':int(te.sum()),'cells':len(gk),'alpha':alpha,
          'test_rmse':float(np.sqrt(np.mean((y[te]-pred)**2))),'test_mae':float(np.mean(abs(y[te]-pred))),
          'known_key_share':float(known.mean())})
    return rows

start=time.monotonic();pair=x['sender'].astype('i8')*B+x['receiver'];country_pair=x['sender_country'].astype('i8')*256+x['receiver_country']
currency=[]
for alpha in [10.,100.,1000.]:
 for name,key in [('sender_country',x['sender_country']),('country_pair',country_pair),('sender_bic',x['sender']),('receiver_bic',x['receiver']),('bic_pair',pair)]:
  currency.append(cat_score(name,x['currency'],early,july,key,C,alpha))
currency.append(cat_score('global',x['currency'],early,july,None,C,0))
pd.DataFrame(currency).to_csv(OUT/'currency_bank_models.csv',index=False)

nd=x['route']>0;cover=[]
for alpha in [10.,100.,1000.]:
 for name,key in [('sender_country',x['sender_country']),('country_pair',country_pair),('sender_bic',x['sender']),('receiver_bic',x['receiver']),('bic_pair',pair)]:
  cover.append(cat_score(name,(x['route']==2).astype('u1'),early&nd,july&nd,key,2,alpha))
cover.append(cat_score('global',(x['route']==2).astype('u1'),early&nd,july&nd,None,2,0))
pd.DataFrame(cover).to_csv(OUT/'covered_bank_models.csv',index=False)

unlabel=x['labelled']==0;base_amount=x['currency'].astype('i8')*4+x['party'];continuous=[]
continuous+=continuous_scores('log_amount',x['log_amount'].astype('f8'),early&unlabel,july&unlabel,base_amount,
 [('sender_bic',x['sender']),('receiver_bic',x['receiver']),('bic_pair',pair)],100.)
base_duration=(((x['route'].astype('i8')*2+x['continuous'])*32+x['participants'])*32+x['fx'])
continuous+=continuous_scores('log_duration',x['log_duration'].astype('f8'),early,july,base_duration,
 [('sender_bic',x['sender']),('receiver_bic',x['receiver']),('bic_pair',pair)],100.)
pd.DataFrame(continuous).to_csv(OUT/'continuous_bank_models.csv',index=False)

# Complete dates only; 168 UTC hour-of-week outcomes.
dt=pd.to_datetime(x['epoch'],unit='s',utc=True);how=(dt.dayofweek.to_numpy()*24+dt.hour.to_numpy()).astype('u1')
timetrain=(x['epoch']>=may1)&(x['epoch']<cutoff);timetest=(x['epoch']>=cutoff)&(x['epoch']<jul31)
timing=[]
for alpha in [100.,1000.]:
 for name,key in [('sender_country',x['sender_country']),('sender_bic',x['sender']),('bic_pair',pair)]:
  timing.append(cat_score(name,how,timetrain,timetest,key,168,alpha))
timing.append(cat_score('global',how,timetrain,timetest,None,168,0))
pd.DataFrame(timing).to_csv(OUT/'timing_bank_models.csv',index=False)

# First visible intermediary choice, excluding routes with <3 visible BICs.
hasmid=x['firstmid']!=sentinel; scur=x['sender'].astype('i8')*C+x['currency'];mid=[]
for alpha in [10.,100.,1000.]:
 for name,key in [('currency',x['currency']),('sender_bic',x['sender']),('receiver_bic',x['receiver']),('sender_currency',scur),('bic_pair',pair)]:
  mid.append(cat_score(name,x['firstmid'],early&hasmid,july&hasmid,key,B,alpha))
mid.append(cat_score('global',x['firstmid'],early&hasmid,july&hasmid,None,B,0))
pd.DataFrame(mid).to_csv(OUT/'first_intermediary_models.csv',index=False)

def stats(v):
 v=np.asarray(v,dtype='f8');s=np.sort(v);n=len(s);return {'categories':n,'total':int(s.sum()),'min':float(s[0]),'median':float(np.median(s)),
 'p90':float(np.quantile(s,.9)),'p99':float(np.quantile(s,.99)),'max':float(s[-1]),
 'gini':float((2*np.sum((np.arange(n)+1)*s)/(n*s.sum()))-(n+1)/n)}
bank={'sender_activity':stats(np.bincount(x['sender'],minlength=B)),'receiver_activity':stats(np.bincount(x['receiver'],minlength=B))}
m=np.bincount(x['firstmid'][hasmid],minlength=B);bank['firstmid_activity']=stats(m);bank['firstmid_rows']=int(hasmid.sum())
bank['top1_firstmid_share']=float(m.max()/m.sum());bank['top10_firstmid_share']=float(np.sort(m)[-10:].sum()/m.sum())
bank['runtime_seconds']=time.monotonic()-start
(OUT/'bank_activity.json').write_text(json.dumps(bank,indent=2));print(json.dumps(bank,indent=2),flush=True)
print('runtime',time.monotonic()-start,flush=True)
