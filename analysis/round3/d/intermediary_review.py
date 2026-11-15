"""Blind non-Direct intermediary and Covered-choice later-period prediction."""
from pathlib import Path
import json, time, re
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
CACHE = ROOT / 'outputs/round3/d'
CACHE.mkdir(parents=True, exist_ok=True)
SRC = ROOT / 'outputs/cleaned/payments_cleaned.csv.gz'
CUTOFF = 1688169600
bankmap, currmap, countrymap = {}, {}, {}

def code(mapping, value):
    if value not in mapping:
        mapping[value] = len(mapping)
    return mapping[value]

rows, seen = [], 0
start = time.monotonic()
cols = ['epoch_seconds','currency_code','ordering_bic8','beneficiary_bic8','bic8_path','transaction_type_code','currency_conversion_count']
for d in pd.read_csv(SRC, usecols=cols, dtype=str, keep_default_na=False, chunksize=100000):
    seen += len(d)
    for r in d[d.transaction_type_code.ne('Direct')].itertuples(index=False):
        visible = [x for x in r.bic8_path.split(';') if re.fullmatch('[A-Z0-9]{8}', x)]
        if len(visible) < 3:
            continue
        sender, receiver = r.ordering_bic8, r.beneficiary_bic8
        rows.append((int(r.epoch_seconds), code(currmap,r.currency_code), code(bankmap,sender), code(bankmap,receiver), code(countrymap,sender[4:6]), code(countrymap,receiver[4:6]), code(bankmap,visible[1]), code(bankmap,visible[-2]), int(r.currency_conversion_count), int(r.transaction_type_code=='Covered')))
    if seen % 1000000 == 0:
        print('source', seen, 'nondirect', len(rows), round(time.monotonic()-start,1), flush=True)

DT = np.dtype([('epoch','i8'),('currency','u2'),('sender','u2'),('receiver','u2'),('sc','u2'),('rc','u2'),('first','u2'),('last','u2'),('fx','u1'),('covered','u1')])
a = np.array(rows, dtype=DT)
np.save(CACHE/'intermediaries.npy', a)
del rows
train, test = a['epoch'] < CUTOFF, a['epoch'] >= CUTOFF
nb, nc, ncountry = len(bankmap), len(currmap), len(countrymap)

def categorical(target, model, key, alpha=10.0):
    ytr, yte = a[target][train].astype('int64'), a[target][test].astype('int64')
    ktr, kte = key[train].astype('int64'), key[test].astype('int64')
    gp = np.bincount(ytr, minlength=nb).astype(float); gp /= gp.sum()
    fallback = int(gp.argmax())
    z = pd.DataFrame({'k':ktr,'y':ytr}).groupby(['k','y'],sort=False).size().rename('n').reset_index()
    totals_s = z.groupby('k').n.sum(); modes_s = z.loc[z.groupby('k').n.idxmax()].set_index('k').y
    counts = {(int(k),int(y)):int(v) for k,y,v in z.itertuples(index=False)}
    totals = {int(k):int(v) for k,v in totals_s.items()}; modes = {int(k):int(v) for k,v in modes_s.items()}
    known = np.fromiter((int(k) in totals for k in kte), bool, len(kte))
    pred = np.fromiter((modes.get(int(k),fallback) for k in kte), 'i8', len(kte))
    probs = np.empty(len(kte))
    for i,(k,y) in enumerate(zip(kte,yte)):
        probs[i] = (counts.get((int(k),int(y)),0)+alpha*gp[int(y)])/(totals.get(int(k),0)+alpha)
    return dict(target=target,model=model,train_n=int(train.sum()),test_n=len(yte),cells=len(totals),alpha=alpha,known_share=float(known.mean()),accuracy=float((pred==yte).mean()),nll=float(-np.log(np.maximum(probs,1e-300)).mean()))

def binary(model, key, alpha=10.0):
    ytr, yte = a['covered'][train].astype('int64'), a['covered'][test].astype('int64')
    ktr, kte = key[train].astype('int64'), key[test].astype('int64')
    global_rate = float(ytr.mean())
    z = pd.DataFrame({'k':ktr,'y':ytr}).groupby('k').y.agg(['sum','count'])
    rates = ((z['sum']+alpha*global_rate)/(z['count']+alpha)).to_dict()
    known = np.fromiter((int(k) in rates for k in kte), bool, len(kte))
    p = np.fromiter((rates.get(int(k),global_rate) for k in kte), float, len(kte))
    return dict(model=model,train_n=len(ytr),test_n=len(yte),cells=len(z),alpha=alpha,known_share=float(known.mean()),accuracy=float(((p>=.5)==yte).mean()),nll=float(-(yte*np.log(p)+(1-yte)*np.log1p(-p)).mean()),train_rate=global_rate,test_rate=float(yte.mean()))

base = np.zeros(len(a), dtype='int64')
keys = {
    'global':base,
    'currency':a['currency'].astype('i8'),
    'sender_country_currency':a['sc'].astype('i8')*nc+a['currency'],
    'country_pair_currency':(a['sc'].astype('i8')*ncountry+a['rc'])*nc+a['currency'],
    'sender_bic_currency':a['sender'].astype('i8')*nc+a['currency'],
    'endpoint_pair_currency':(a['sender'].astype('i8')*nb+a['receiver'])*nc+a['currency'],
    'endpoint_pair_currency_fx':((a['sender'].astype('i8')*nb+a['receiver'])*nc+a['currency'])*18+a['fx'],
}
output = []
for target in ['first','last']:
    for name,key in keys.items():
        print('fit',target,name,flush=True)
        output.append(categorical(target,name,key))
pd.DataFrame(output).to_csv(OUT/'intermediary_models.csv',index=False)

covered = []
covered_keys = {'global':base,'sender_country':a['sc'].astype('i8'),'sender_bic':a['sender'].astype('i8'),'country_pair':a['sc'].astype('i8')*ncountry+a['rc'],'endpoint_pair':a['sender'].astype('i8')*nb+a['receiver']}
for name,key in covered_keys.items():
    print('covered',name,flush=True)
    covered.append(binary(name,key))
pd.DataFrame(covered).to_csv(OUT/'covered_models.csv',index=False)

manifest = {'status':'complete','source_rows':seen,'rows':len(a),'train':int(train.sum()),'july':int(test.sum()),'banks_including_path':len(bankmap),'currencies':len(currmap),'countries':len(countrymap),'elapsed_seconds':time.monotonic()-start,'limits':['Visible intermediaries only; gaps do not reveal hidden banks.','Earlier/July is retrospective.','Target encoding prediction does not prove selection order.']}
(OUT/'intermediary_manifest.json').write_text(json.dumps(manifest,indent=2))
print(pd.DataFrame(output).to_string(index=False));print(pd.DataFrame(covered).to_string(index=False));print(json.dumps(manifest,indent=2))
