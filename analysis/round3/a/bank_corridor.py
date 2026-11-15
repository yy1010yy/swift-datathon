"""Independent full-file bank/corridor and intermediary models.

Two raw scans: pre-July training aggregates, then July scoring. Exact BIC-pair models
use a stable pandas uint64 hash modulo64 and retain every occurrence of selected pairs.
"""
from pathlib import Path
from collections import defaultdict, Counter
import json, math, time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
DATA=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
CUT=1688169600
ALPHA=100.0
COLS=['epoch_seconds','currency_code','usd_amount','ordering_bic8','beneficiary_bic8',
      'bic8_path','total_duration','continuity_qflag','currency_conversion_count',
      'participant_count','transaction_type_code','ordering_type','beneficiary_type']

def pair_sample(d):
    h=pd.util.hash_pandas_object(d[['ordering_bic8','beneficiary_bic8']],index=False).to_numpy('uint64')
    return h%64==0

def add_counter(store, keys, targets):
    z=pd.DataFrame({'key':keys,'target':targets}).groupby(['key','target'],sort=False).size()
    for (k,t),n in z.items(): store[k][t]+=int(n)

def add_stats(store, keys, values):
    z=pd.DataFrame({'key':keys,'y':values}).groupby('key',sort=False).y.agg(['count','sum',lambda x:float(np.dot(x,x))])
    for k,row in z.iterrows():
        cur=store[k]; cur[0]+=int(row['count']); cur[1]+=float(row['sum']); cur[2]+=float(row['<lambda_0>'])

def key_series(parts):
    return pd.Series(list(zip(*[p.astype(str) for p in parts])),index=parts[0].index)

cur={m:defaultdict(Counter) for m in ['global','sender_country','sender_bic','receiver_bic','pair']}
tim={m:defaultdict(Counter) for m in ['global','sender_country','sender_bic']}
cov={m:defaultdict(Counter) for m in ['base','sender_country','sender_bic','receiver_bic','pair']}
amt={m:defaultdict(lambda:[0,0.0,0.0]) for m in ['base','sender_country','sender_bic','receiver_bic','pair']}
dur={m:defaultdict(lambda:[0,0.0,0.0]) for m in ['base','sender_country','sender_bic','receiver_bic','pair']}
mid={m:defaultdict(Counter) for m in ['base','sender_country','sender_bic','pair']}
intermediate_occ=Counter(); rows=train_rows=0; start=time.monotonic()

for d in pd.read_csv(DATA,usecols=COLS,dtype=str,keep_default_na=False,chunksize=100000):
    rows+=len(d); ep=d.epoch_seconds.astype('int64'); e=d.loc[ep<CUT].copy()
    if len(e):
        train_rows+=len(e); ebic=e.ordering_bic8; rbic=e.beneficiary_bic8
        ec=ebic.str[4:6]; rc=rbic.str[4:6]; ps=pair_sample(e)
        add_counter(cur['global'],pd.Series([()] * len(e),index=e.index),e.currency_code)
        add_counter(cur['sender_country'],ec,e.currency_code); add_counter(cur['sender_bic'],ebic,e.currency_code)
        add_counter(cur['receiver_bic'],rbic,e.currency_code)
        add_counter(cur['pair'],key_series([ebic[ps],rbic[ps]]),e.loc[ps,'currency_code'])
        dt=pd.to_datetime(e.epoch_seconds.astype('int64'),unit='s',utc=True)
        wh=(dt.dt.weekday*24+dt.dt.hour).astype(str)
        add_counter(tim['global'],pd.Series([()] * len(e),index=e.index),wh)
        add_counter(tim['sender_country'],ec,wh); add_counter(tim['sender_bic'],ebic,wh)
        nd=e.transaction_type_code.ne('Direct')
        if nd.any():
            q=e.loc[nd]; qb=q.ordering_bic8; qr=q.beneficiary_bic8; qc=qb.str[4:6]; qps=pair_sample(q)
            base=key_series([q.ordering_type,q.beneficiary_type,q.currency_conversion_count])
            target=q.transaction_type_code.eq('Covered').astype(str)
            add_counter(cov['base'],base,target)
            add_counter(cov['sender_country'],key_series([qc,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),target)
            add_counter(cov['sender_bic'],key_series([qb,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),target)
            add_counter(cov['receiver_bic'],key_series([qr,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),target)
            add_counter(cov['pair'],key_series([qb[qps],qr[qps],q.loc[qps,'ordering_type'],q.loc[qps,'beneficiary_type'],q.loc[qps,'currency_conversion_count']]),target[qps])
        abase=key_series([e.currency_code,e.ordering_type,e.beneficiary_type]); y=np.log(e.usd_amount.astype(float))
        add_stats(amt['base'],abase,y)
        add_stats(amt['sender_country'],key_series([ec,e.currency_code,e.ordering_type,e.beneficiary_type]),y)
        add_stats(amt['sender_bic'],key_series([ebic,e.currency_code,e.ordering_type,e.beneficiary_type]),y)
        add_stats(amt['receiver_bic'],key_series([rbic,e.currency_code,e.ordering_type,e.beneficiary_type]),y)
        add_stats(amt['pair'],key_series([ebic[ps],rbic[ps],e.loc[ps,'currency_code'],e.loc[ps,'ordering_type'],e.loc[ps,'beneficiary_type']]),y[ps])
        dbase=key_series([e.transaction_type_code,e.participant_count,e.currency_conversion_count,e.continuity_qflag]); yd=np.log(e.total_duration.astype(float))
        add_stats(dur['base'],dbase,yd)
        add_stats(dur['sender_country'],key_series([ec,e.transaction_type_code,e.participant_count,e.currency_conversion_count,e.continuity_qflag]),yd)
        add_stats(dur['sender_bic'],key_series([ebic,e.transaction_type_code,e.participant_count,e.currency_conversion_count,e.continuity_qflag]),yd)
        add_stats(dur['receiver_bic'],key_series([rbic,e.transaction_type_code,e.participant_count,e.currency_conversion_count,e.continuity_qflag]),yd)
        add_stats(dur['pair'],key_series([ebic[ps],rbic[ps],e.loc[ps,'transaction_type_code'],e.loc[ps,'participant_count'],e.loc[ps,'currency_conversion_count'],e.loc[ps,'continuity_qflag']]),yd[ps])
        # first visible intermediate, complete non-Direct paths only
        ok=e.transaction_type_code.ne('Direct') & e.continuity_qflag.eq('Y')
        if ok.any():
            q=e.loc[ok]; entries=q.bic8_path.str.split(';'); target=entries.str[1]
            qb=q.ordering_bic8; qr=q.beneficiary_bic8; qc=qb.str[4:6]; qps=pair_sample(q)
            mbase=key_series([q.currency_code,q.transaction_type_code])
            add_counter(mid['base'],mbase,target)
            add_counter(mid['sender_country'],key_series([qc,q.currency_code,q.transaction_type_code]),target)
            add_counter(mid['sender_bic'],key_series([qb,q.currency_code,q.transaction_type_code]),target)
            add_counter(mid['pair'],key_series([qb[qps],qr[qps],q.loc[qps,'currency_code'],q.loc[qps,'transaction_type_code']]),target[qps])
            intermediate_occ.update(target.value_counts().to_dict())
    if rows%1000000==0: print('TRAIN_SCAN',rows,round(time.monotonic()-start,1),flush=True)

def parent_key(model, key, family):
    if family=='currency':
        if model=='sender_bic': return key[4:6]
        if model=='receiver_bic': return key[4:6]
        if model=='pair': return key[0]
        return ()
    return None

score=defaultdict(lambda:{'n':0,'correct':0,'nll':0.0,'sse':0.0,'unseen':0})

def score_class(name, store, parent, groups, alpha=ALPHA):
    out=score[name]
    for (k,t),n in groups.items():
        c=store.get(k); pc=parent(k) if callable(parent) else parent
        if c is None: c=Counter(); out['unseen']+=int(n)
        pcount=sum(pc.values()); p0=(pc.get(t,0)+0.5)/(pcount+0.5*max(2,len(pc)))
        prob=(c.get(t,0)+alpha*p0)/(sum(c.values())+alpha)
        pred=max(c,key=c.get) if c else (max(pc,key=pc.get) if pc else None)
        out['n']+=int(n); out['correct']+=int(n)*(t==pred); out['nll']-=int(n)*math.log(max(prob,1e-15))

def score_stats(name, store, base_store, groups, base_from_key, alpha=ALPHA):
    out=score[name]
    for k,row in groups.iterrows():
        n=float(row['count']); sy=float(row['sum']); sy2=float(row['sq'])
        b=base_store.get(base_from_key(k)); bm=b[1]/b[0] if b and b[0] else sy/n
        g=store.get(k)
        if g: pred=(g[1]+alpha*bm)/(g[0]+alpha)
        else: pred=bm; out['unseen']+=int(n)
        out['n']+=int(n); out['sse']+=sy2-2*pred*sy+n*pred*pred

rows2=july_rows=0
for d in pd.read_csv(DATA,usecols=COLS,dtype=str,keep_default_na=False,chunksize=100000):
    rows2+=len(d); ep=d.epoch_seconds.astype('int64'); j=d.loc[ep>=CUT].copy()
    if not len(j): continue
    july_rows+=len(j); sb=j.ordering_bic8; rb=j.beneficiary_bic8; sc=sb.str[4:6]; rc=rb.str[4:6]; ps=pair_sample(j)
    # class scoring via compact July grouped cells
    for model,key,parent in [
        ('sender_country',sc,lambda k:cur['global'][()]),
        ('sender_bic',sb,lambda k:cur['sender_country'].get(k[4:6],cur['global'][()])),
        ('receiver_bic',rb,lambda k:cur['global'][()])]:
        g=pd.DataFrame({'key':key,'target':j.currency_code}).groupby(['key','target']).size()
        score_class('currency_'+model,cur[model],parent,g)
    if ps.any():
        key=key_series([sb[ps],rb[ps]]); g=pd.DataFrame({'key':key,'target':j.loc[ps,'currency_code']}).groupby(['key','target']).size()
        score_class('currency_pair_sample',cur['pair'],lambda k:cur['sender_bic'].get(k[0],cur['global'][()]),g)
    dt=pd.to_datetime(j.epoch_seconds.astype('int64'),unit='s',utc=True); wh=(dt.dt.weekday*24+dt.dt.hour).astype(str)
    for model,key,parent in [('sender_country',sc,lambda k:tim['global'][()]),('sender_bic',sb,lambda k:tim['sender_country'].get(k[4:6],tim['global'][()]))]:
        g=pd.DataFrame({'key':key,'target':wh}).groupby(['key','target']).size(); score_class('timing_'+model,tim[model],parent,g)
    nd=j.transaction_type_code.ne('Direct')
    if nd.any():
        q=j.loc[nd]; qb=q.ordering_bic8; qr=q.beneficiary_bic8; qc=qb.str[4:6]; qps=pair_sample(q); target=q.transaction_type_code.eq('Covered').astype(str)
        base=key_series([q.ordering_type,q.beneficiary_type,q.currency_conversion_count])
        specs=[('base',base,lambda k:Counter({'True':0,'False':1})),('sender_country',key_series([qc,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),lambda k:cov['base'].get(k[1:],Counter())),('sender_bic',key_series([qb,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),lambda k:cov['sender_country'].get((k[0][4:6],)+k[1:],cov['base'].get(k[1:],Counter()))),('receiver_bic',key_series([qr,q.ordering_type,q.beneficiary_type,q.currency_conversion_count]),lambda k:cov['base'].get(k[1:],Counter()))]
        for model,key,parent in specs:
            g=pd.DataFrame({'key':key,'target':target}).groupby(['key','target']).size(); score_class('covered_'+model,cov[model],parent,g)
        if qps.any():
            key=key_series([qb[qps],qr[qps],q.loc[qps,'ordering_type'],q.loc[qps,'beneficiary_type'],q.loc[qps,'currency_conversion_count']]); g=pd.DataFrame({'key':key,'target':target[qps]}).groupby(['key','target']).size(); score_class('covered_pair_sample',cov['pair'],lambda k:cov['sender_bic'].get((k[0],)+k[2:],cov['base'].get(k[2:],Counter())),g)
    # numeric group scores
    abase=key_series([j.currency_code,j.ordering_type,j.beneficiary_type]); y=np.log(j.usd_amount.astype(float))
    specs=[('base',abase,lambda k:k),('sender_country',key_series([sc,j.currency_code,j.ordering_type,j.beneficiary_type]),lambda k:k[1:]),('sender_bic',key_series([sb,j.currency_code,j.ordering_type,j.beneficiary_type]),lambda k:k[1:]),('receiver_bic',key_series([rb,j.currency_code,j.ordering_type,j.beneficiary_type]),lambda k:k[1:])]
    for model,key,bk in specs:
        g=pd.DataFrame({'key':key,'y':y}).groupby('key').y.agg(count='count',sum='sum',sq=lambda x:float(np.dot(x,x))); score_stats('amount_'+model,amt[model],amt['base'],g,bk)
    if ps.any():
        key=key_series([sb[ps],rb[ps],j.loc[ps,'currency_code'],j.loc[ps,'ordering_type'],j.loc[ps,'beneficiary_type']]); yy=y[ps]; g=pd.DataFrame({'key':key,'y':yy}).groupby('key').y.agg(count='count',sum='sum',sq=lambda x:float(np.dot(x,x))); score_stats('amount_pair_sample',amt['pair'],amt['base'],g,lambda k:k[2:])
    dbase=key_series([j.transaction_type_code,j.participant_count,j.currency_conversion_count,j.continuity_qflag]); yd=np.log(j.total_duration.astype(float))
    specs=[('base',dbase,lambda k:k),('sender_country',key_series([sc,j.transaction_type_code,j.participant_count,j.currency_conversion_count,j.continuity_qflag]),lambda k:k[1:]),('sender_bic',key_series([sb,j.transaction_type_code,j.participant_count,j.currency_conversion_count,j.continuity_qflag]),lambda k:k[1:]),('receiver_bic',key_series([rb,j.transaction_type_code,j.participant_count,j.currency_conversion_count,j.continuity_qflag]),lambda k:k[1:])]
    for model,key,bk in specs:
        g=pd.DataFrame({'key':key,'y':yd}).groupby('key').y.agg(count='count',sum='sum',sq=lambda x:float(np.dot(x,x))); score_stats('duration_'+model,dur[model],dur['base'],g,bk)
    if ps.any():
        key=key_series([sb[ps],rb[ps],j.loc[ps,'transaction_type_code'],j.loc[ps,'participant_count'],j.loc[ps,'currency_conversion_count'],j.loc[ps,'continuity_qflag']]); yy=yd[ps]; g=pd.DataFrame({'key':key,'y':yy}).groupby('key').y.agg(count='count',sum='sum',sq=lambda x:float(np.dot(x,x))); score_stats('duration_pair_sample',dur['pair'],dur['base'],g,lambda k:k[2:])
    ok=j.transaction_type_code.ne('Direct') & j.continuity_qflag.eq('Y')
    if ok.any():
        q=j.loc[ok]; target=q.bic8_path.str.split(';').str[1]; qb=q.ordering_bic8; qr=q.beneficiary_bic8; qc=qb.str[4:6]; qps=pair_sample(q)
        specs=[('base',key_series([q.currency_code,q.transaction_type_code]),lambda k:Counter()),('sender_country',key_series([qc,q.currency_code,q.transaction_type_code]),lambda k:mid['base'].get(k[1:],Counter())),('sender_bic',key_series([qb,q.currency_code,q.transaction_type_code]),lambda k:mid['sender_country'].get((k[0][4:6],)+k[1:],mid['base'].get(k[1:],Counter())))]
        for model,key,parent in specs:
            g=pd.DataFrame({'key':key,'target':target}).groupby(['key','target']).size(); score_class('intermediary_'+model,mid[model],parent,g)
        if qps.any():
            key=key_series([qb[qps],qr[qps],q.loc[qps,'currency_code'],q.loc[qps,'transaction_type_code']]); g=pd.DataFrame({'key':key,'target':target[qps]}).groupby(['key','target']).size(); score_class('intermediary_pair_sample',mid['pair'],lambda k:mid['sender_bic'].get((k[0],)+k[2:],mid['base'].get(k[2:],Counter())),g)
    if rows2%1000000==0: print('SCORE_SCAN',rows2,round(time.monotonic()-start,1),flush=True)

records=[]
for name,v in sorted(score.items()):
    rec={'model':name,**v}
    if v['n']:
        if 'sse' in v and (name.startswith('amount_') or name.startswith('duration_')): rec['rmse_log']=math.sqrt(max(0,v['sse'])/v['n'])
        if name.startswith(('currency_','timing_','covered_','intermediary_')):
            rec['accuracy']=v['correct']/v['n']; rec['mean_nll']=v['nll']/v['n']
    records.append(rec)
pd.DataFrame(records).to_csv(OUT/'bank_corridor_scores.csv',index=False)
top=pd.DataFrame(intermediate_occ.most_common(),columns=['bic8','early_intermediate_occurrences'])
top['share']=top.early_intermediate_occurrences/top.early_intermediate_occurrences.sum(); top['cumulative_share']=top['share'].cumsum(); top.head(500).to_csv(OUT/'intermediary_hubs_top500.csv',index=False)
manifest={'status':'complete','source_rows':rows,'train_rows':train_rows,'july_rows':july_rows,'second_scan_rows':rows2,'cutoff_utc':'2023-07-01','alpha':ALPHA,'pair_sample':'pandas stable uint64 hash exact BIC pair modulo64 equals0; all occurrences retained','pair_sample_july_n':score['currency_pair_sample']['n'],'elapsed_seconds':time.monotonic()-start,'limits':['July is a retrospective stability period, not untouched discovery.','Pair results are deterministic sample estimates; exact-bank categories remain sparse.','Categorical smoothing is fixed alpha100; not claimed optimal.','First visible intermediate on continuous non-Direct paths is an encoded path position, not proof of legal correspondent role.']}
(OUT/'bank_corridor_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2)); print(pd.DataFrame(records).to_string(index=False))
