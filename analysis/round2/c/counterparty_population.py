"""Exact blank-label directed-pair census using bounded disk partitions.

Hashing only chooses one of32 files. Pair identity/grouping uses full raw strings,
so hash collisions do not merge accounts. Run --phase scan, analyze or all(default).
"""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,time,math,hashlib
import pandas as pd
import numpy as np

P=Path(__file__).resolve().parent;ROOT=P.parents[2]
CACHE=ROOT/'outputs/round2/c/counterparty_population';CACHE.mkdir(parents=True,exist_ok=True)
SPLIT=1688169600;BINS=[0,1,10,60,300,1800,3600,21600,86400,604800,np.inf]
def scan():
    if list(CACHE.glob('part_*.csv')):raise FileExistsError('Partition files exist; use --phase analyze or choose a new cache.')
    source=ROOT/'outputs/cleaned/payments_cleaned.csv.gz';rows=blank=0;start=time.monotonic()
    cols=['ordering_account','beneficiary_account','epoch_seconds','ordering_type','beneficiary_type','anomaly_type']
    for d in pd.read_csv(source,usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
        rows+=len(d);d=d[d.anomaly_type.eq('')].copy();blank+=len(d)
        work=pd.DataFrame({'sender':d.ordering_account,'receiver':d.beneficiary_account,
            'epoch':d.epoch_seconds.astype('int64'),'party':d.ordering_type+d.beneficiary_type})
        shard=(pd.util.hash_pandas_object(work.sender,index=False)%32).to_numpy()
        for part,g in work.groupby(shard,sort=False):
            path=CACHE/f'part_{part:02d}.csv';g.to_csv(path,index=False,mode='a',header=not path.exists())
        if rows%1000000==0:print('scan',rows,'blank',blank,'seconds',round(time.monotonic()-start,1),flush=True)
    assert rows==10000000 and blank==9992994
    manifest={'scope_rows':rows,'blank_rows':blank,'input_bytes':source.stat().st_size,
       'input_mtime_ns':source.stat().st_mtime_ns,'partition_count':32,
       'identity':'Exact raw sender/receiver strings; hash only assigns partition.',
       'scan_seconds':time.monotonic()-start}
    (CACHE/'scan_manifest.json').write_text(json.dumps(manifest,indent=2))
def analyze():
    meta=json.loads((CACHE/'scan_manifest.json').read_text());start=time.monotonic()
    hist=Counter();intervals=defaultdict(list);cohorts=Counter();rows=pairs=mixed=0;ties=0;first_timestamp_rows=0
    pairfile=CACHE/'pair_summary.csv';pairfile.unlink(missing_ok=True)
    for path in sorted(CACHE.glob('part_*.csv')):
        d=pd.read_csv(path,dtype={'sender':str,'receiver':str,'epoch':'int64','party':str},keep_default_na=False)
        d=d.sort_values(['sender','receiver','epoch']).reset_index(drop=True)
        codes=pd.factorize(pd.MultiIndex.from_frame(d[['sender','receiver']]),sort=False)[0]
        d['early']=d.epoch.lt(SPLIT).astype(int)
        g=d.groupby(codes,sort=False)
        p=g.agg(sender=('sender','first'),receiver=('receiver','first'),n=('epoch','size'),
            early_n=('early','sum'),party=('party','first'),party_variants=('party','nunique'),
            first_epoch=('epoch','min'),last_epoch=('epoch','max'))
        p['july_n']=p.n-p.early_n;p.loc[p.party_variants.gt(1),'party']='MIXED'
        first_timestamp_rows+=int(d.epoch.eq(pd.Series(codes).map(p.first_epoch)).sum())
        p.to_csv(pairfile,index=False,mode='a',header=pairs==0)
        adj=g.epoch.diff();ties+=int(adj.eq(0).sum())
        strict=adj.mask(adj.eq(0)).groupby(codes,sort=False).ffill()
        rowparty=pd.Series(codes).map(p.party)
        for party in p.party.unique():
            sub=p[p.party.eq(party)]
            for period,col in [('full','n'),('early','early_n'),('July','july_n')]:
                c=sub.loc[sub[col].gt(0),col].value_counts()
                hist.update({(party,period,int(k)):int(v) for k,v in c.items()})
            for status,mask in [('early_only',sub.early_n.gt(0)&sub.july_n.eq(0)),
                                ('both_periods',sub.early_n.gt(0)&sub.july_n.gt(0)),
                                ('July_new',sub.early_n.eq(0)&sub.july_n.gt(0))]:
                cohorts[(party,status)]+=int(mask.sum())
        for (party,period),ix in pd.DataFrame({'party':rowparty,'period':np.where(d.epoch<SPLIT,'early','July')}).groupby(['party','period']).groups.items():
            a=strict.loc[ix].dropna().to_numpy(dtype=np.int64);intervals[(party,period)].append(a)
        rows+=len(d);pairs+=len(p);mixed+=int(p.party_variants.gt(1).sum())
        print('analyze',path.name,'rows',rows,'pairs',pairs,'seconds',round(time.monotonic()-start,1),flush=True)
    assert rows==meta['blank_rows']
    counts=pd.DataFrame([dict(party=k[0],period=k[1],payments_per_pair=k[2],pairs=n) for k,n in hist.items()])
    counts.to_csv(P/'counterparty_count_histogram.csv',index=False)
    pd.DataFrame([dict(party=k[0],cohort=k[1],pairs=n) for k,n in cohorts.items()]).to_csv(P/'counterparty_cohorts.csv',index=False)
    summary=[];modelcells=[]
    for (party,period),s in counts.groupby(['party','period']):
        n=int(s.pairs.sum());payments=int((s.pairs*s.payments_per_pair).sum());mean=payments/n
        lo=1e-10;hi=max(1,mean*2)
        for _ in range(100):
            lam=(lo+hi)/2
            if lam/(-math.expm1(-lam))<mean:lo=lam
            else:hi=lam
        lam=(lo+hi)/2;prob=1/mean
        summary.append(dict(party=party,period=period,pairs=n,payments=payments,mean_payments=mean,
          singleton_pairs=int(s.loc[s.payments_per_pair.eq(1),'pairs'].sum()),
          repeated_pairs=int(s.loc[s.payments_per_pair.gt(1),'pairs'].sum()),
          max_payments=int(s.payments_per_pair.max()),zt_poisson_lambda=lam,positive_geometric_p=prob))
        for left,right in [(1,1),(2,2),(3,3),(4,4),(5,5),(6,10),(11,20),(21,50),(51,np.inf)]:
            observed=int(s.loc[s.payments_per_pair.between(left,right),'pairs'].sum())
            if right==np.inf:
                poisson=1-sum(math.exp(-lam+k*math.log(lam)-math.lgamma(k+1)) for k in range(1,51))/(-math.expm1(-lam))
                geo=(1-prob)**50
            else:
                poisson=sum(math.exp(-lam+k*math.log(lam)-math.lgamma(k+1)) for k in range(left,right+1))/(-math.expm1(-lam))
                geo=(1-prob)**(left-1)-(1-prob)**right
            modelcells.append(dict(party=party,period=period,left=left,right=right,observed=observed,
                 zt_poisson_expected=max(0,n*poisson),positive_geometric_expected=n*geo))
    pd.DataFrame(summary).to_csv(P/'counterparty_count_summary.csv',index=False)
    pd.DataFrame(modelcells).to_csv(P/'counterparty_count_models.csv',index=False)
    intervalsummary=[];intervalcells=[]
    arrays={k:np.concatenate(v) for k,v in intervals.items()}
    assert sum(map(len,arrays.values()))+first_timestamp_rows==rows
    for (party,period),a in arrays.items():
        np.save(CACHE/f'intervals_{party}_{period}.npy',a)
        if not len(a):continue
        quant=np.quantile(a,[.01,.1,.5,.9,.99]) if len(a) else [np.nan]*5
        intervalsummary.append(dict(party=party,period=period,n=len(a),mean_seconds=float(a.mean()),
            sd_seconds=float(a.std()),min_seconds=int(a.min()),max_seconds=int(a.max()),
            **dict(zip(['p01','p10','median','p90','p99'],map(float,quant)))))
        early=arrays.get((party,'early'));scale=float(early.mean()) if early is not None else float(a.mean())
        observed=np.histogram(a,bins=BINS)[0]
        for l,r,o in zip(BINS[:-1],BINS[1:],observed):
            expected=len(a)*(math.exp(-l/scale)-(math.exp(-r/scale) if np.isfinite(r) else 0))
            intervalcells.append(dict(party=party,period=period,left=l,right=r,observed=int(o),
                        early_fit_exponential_expected=expected,early_mean_seconds=scale))
    pd.DataFrame(intervalsummary).to_csv(P/'counterparty_interval_summary.csv',index=False)
    pd.DataFrame(intervalcells).to_csv(P/'counterparty_interval_models.csv',index=False)
    meta.update({'pairs':pairs,'mixed_party_pairs':mixed,'equal_time_adjacent_pairs':ties,
      'first_timestamp_rows_without_prior':first_timestamp_rows,'strict_prior_rows':sum(map(len,arrays.values())),
      'analyze_seconds':time.monotonic()-start,'complete':True,
      'interval_definition':'strict earlier distinct timestamp per directedpair; tied rows use same earlier distincttimestamp, firsttimestamp rows excluded',
      'count_models':'Conditioned on observed pairs only; no absent-pair denominator. Period models fitted separately, not a universal generator.'})
    (P/'counterparty_manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2),flush=True)
    print(pd.DataFrame(summary).to_string(index=False));print(pd.DataFrame(intervalsummary).to_string(index=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['scan','analyze','all'],default='all');args=ap.parse_args()
    if args.phase in ['scan','all']:scan()
    if args.phase in ['analyze','all']:analyze()
