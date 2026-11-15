"""Activity-preserving challenge to ordinary directed-pair recurrence.

Uses the completed blank-label pair summary, preserving exact raw account strings.
All senders are summarized. Receiver-side pair tests use a deterministic 1/64 exact
receiver-account sample retaining every pair and payment for selected receivers.
"""
from pathlib import Path
from collections import defaultdict
import json, math, time
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
PAIR=ROOT/'outputs/round2/c/counterparty_population/pair_summary.csv'
N=9_992_994

def chosen_receiver(s):
    return (pd.util.hash_pandas_object(pd.DataFrame({'receiver':s}),index=False).to_numpy('uint64')%64)==0

def update(store, grouped):
    for key,row in grouped.iterrows():
        x=store[key]; x[0]+=int(row['payments']); x[1]+=int(row['pairs']); x[2]+=int(row['repeated']); x[3]=max(x[3],int(row['maxn']))

send=defaultdict(lambda:[0,0,0,0]); recv=defaultdict(lambda:[0,0,0,0])
rows=payments=sample_pairs=sample_payments=0; start=time.monotonic()
for d in pd.read_csv(PAIR,dtype={'sender':str,'receiver':str,'party':str},chunksize=200000):
    rows+=len(d); payments+=int(d.n.sum())
    g=d.assign(repeated=d.n.gt(1).astype(int)).groupby('sender').agg(payments=('n','sum'),pairs=('n','size'),repeated=('repeated','sum'),maxn=('n','max'))
    update(send,g)
    mask=chosen_receiver(d.receiver)
    q=d.loc[mask].copy(); sample_pairs+=len(q); sample_payments+=int(q.n.sum())
    if len(q):
        g=q.assign(repeated=q.n.gt(1).astype(int)).groupby('receiver').agg(payments=('n','sum'),pairs=('n','size'),repeated=('repeated','sum'),maxn=('n','max'))
        update(recv,g)
    if rows%2000000<200000: print('PASS1_PAIRS',rows,round(time.monotonic()-start,1),flush=True)

assert rows==8_258_480 and payments==N
sdf=pd.DataFrame([(k,*v) for k,v in send.items()],columns=['account','payments','degree','repeat_pairs','max_pair_n'])
rdf=pd.DataFrame([(k,*v) for k,v in recv.items()],columns=['account','payments','degree','repeat_pairs','max_pair_n'])
sdf['repeat_pair_share']=sdf.repeat_pairs/sdf.degree; rdf['repeat_pair_share']=rdf.repeat_pairs/rdf.degree
sdf.to_csv(OUT/'sender_activity_summary.csv.gz',index=False,compression='gzip')
rdf.to_csv(OUT/'receiver_sample_activity_summary.csv.gz',index=False,compression='gzip')
smap=dict(zip(sdf.account,sdf.payments)); rmap=dict(zip(rdf.account,rdf.payments))

def cond_repeat(lam):
    lam=np.asarray(lam,float); out=np.empty_like(lam)
    small=lam<50; out[small]=1-lam[small]/np.expm1(lam[small]); out[~small]=1.0
    return np.clip(out,0,1)

# Fixed activity bins from sampled-pair endpoint volumes, then second-pass null test.
allcells=[]; overall=[]; role_acc=defaultdict(lambda:[0,0.0,0,0.0])
for d in pd.read_csv(PAIR,dtype={'sender':str,'receiver':str,'party':str},chunksize=200000):
    q=d.loc[chosen_receiver(d.receiver)].copy()
    if not len(q): continue
    q['sender_payments']=q.sender.map(smap).astype(float); q['receiver_payments']=q.receiver.map(rmap).astype(float)
    q['lambda_independence']=q.sender_payments*q.receiver_payments/N
    q['expected_repeat_cond_observed']=cond_repeat(q.lambda_independence.to_numpy())
    q['observed_repeat']=q.n.gt(1).astype(int)
    # log2 activity bins are interpretable and fixed, unlike sample-selected quantiles.
    q['sender_bin']=np.floor(np.log2(q.sender_payments)).clip(0,20).astype(int)
    q['receiver_bin']=np.floor(np.log2(q.receiver_payments)).clip(0,20).astype(int)
    z=q.groupby(['party','sender_bin','receiver_bin']).agg(pairs=('n','size'),observed_repeat=('observed_repeat','sum'),expected_repeat=('expected_repeat_cond_observed','sum'),payments=('n','sum')).reset_index()
    allcells.append(z)
    for party,g in q.groupby('party'):
        x=role_acc[party]; x[0]+=len(g); x[1]+=float(g.observed_repeat.sum()); x[2]+=int(g.n.sum()); x[3]+=float(g.expected_repeat_cond_observed.sum())

cells=pd.concat(allcells).groupby(['party','sender_bin','receiver_bin'],as_index=False).sum()
cells['observed_repeat_share']=cells.observed_repeat/cells.pairs
cells['expected_repeat_share_activity_null']=cells.expected_repeat/cells.pairs
cells.to_csv(OUT/'activity_null_cells.csv',index=False)
for party,x in sorted(role_acc.items()):
    overall.append({'party':party,'sample_pairs':x[0],'observed_repeated_pairs':x[1],'sample_payments':x[2],'expected_repeated_pairs_activity_null':x[3],'observed_repeat_share':x[1]/x[0],'expected_repeat_share_activity_null':x[3]/x[0],'observed_over_expected':x[1]/x[3] if x[3] else None})
pd.DataFrame(overall).to_csv(OUT/'activity_null_summary.csv',index=False)

def dist_summary(df,side):
    return {'side':side,'accounts':len(df),'payments_median':float(df.payments.median()),'payments_p99':float(df.payments.quantile(.99)),'payments_max':int(df.payments.max()),'degree_median':float(df.degree.median()),'degree_p99':float(df.degree.quantile(.99)),'degree_max':int(df.degree.max()),'corr_log_payments_log_degree':float(np.corrcoef(np.log1p(df.payments),np.log1p(df.degree))[0,1]),'accounts_with_repeat_pair':int(df.repeat_pairs.gt(0).sum())}
manifest={'status':'complete','pair_rows':rows,'blank_payments':payments,'all_sender_accounts':len(sdf),'sample_receiver_accounts':len(rdf),'sample_pairs':sample_pairs,'sample_payments':sample_payments,'receiver_sample':'pandas stable uint64 hash exact receiver account modulo64 equals0; all pairs retained','activity_summaries':[dist_summary(sdf,'sender'),dist_summary(rdf,'receiver_sample')],'elapsed_seconds':time.monotonic()-start,'limits':['Configuration-style independence uses observed blank-payment endpoint volumes and conditions on an observed edge; it is a challenge model, not a fitted generator.','Finite-window censoring and omitted labelled payments remain.','Receiver statistics are a deterministic account sample; sender statistics are full population.','Exact account strings may not identify real people and beneficiary strings can occur with multiple BICs.']}
(OUT/'entity_network_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2)); print(pd.DataFrame(overall).to_string(index=False))
