"""Full-census account/detail tests with disk-backed exact reuse counts."""
from pathlib import Path
from collections import Counter
import pandas as pd,numpy as np,sqlite3,re,time,json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'analysis/round2/a';CACHE=ROOT/'outputs/round2/a'
database=CACHE/'account_reuse.sqlite'
if database.exists():raise FileExistsError('Refusing to overwrite existing account-reuse DB')
con=sqlite3.connect(database);con.execute('PRAGMA journal_mode=WAL');con.execute('PRAGMA synchronous=NORMAL')
con.execute('CREATE TABLE reuse(side TEXT,account TEXT,bic TEXT,n INTEGER,PRIMARY KEY(side,account,bic)) WITHOUT ROWID')
cols=['source_record','epoch_seconds']+[s+'_'+f for s in ['ordering','beneficiary'] for f in ['account','details','bic8','type']]
counts=Counter();examples=[];n=0;start=time.monotonic()
for d in pd.read_csv(ROOT/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
 month=pd.to_datetime(d.epoch_seconds.astype('int64'),unit='s',utc=True).dt.strftime('%Y-%m')
 for side in ['ordering','beneficiary']:
  acc=d[side+'_account'];details=d[side+'_details'];bic=d[side+'_bic8'];prefix=acc.str.startswith('_FAKE_');suffix=acc.str.removeprefix('_FAKE_')
  first=details.str.split('\n',n=1).str[0].str.rstrip('\r');after=first.str.lstrip('/')
  exact=prefix & suffix.eq(after)
  anywhere=pd.Series([bool(s) and s in txt for s,txt in zip(suffix,details)],index=d.index)
  normalized=pd.Series([bool(s) and re.sub('[^A-Za-z0-9]','',s).upper() in re.sub('[^A-Za-z0-9]','',txt).upper() for s,txt in zip(suffix,details)],index=d.index)
  iban=suffix.str.fullmatch('[A-Z]{2}[0-9]{2}[A-Z0-9]{10,30}')
  t=pd.DataFrame({'side':side,'month':month,'type':d[side+'_type'],'fake_prefix':prefix,'exact_firstline':exact,'literal_anywhere':anywhere,'normalized_anywhere':normalized,'iban_looking':iban,'iban_prefix_matches_bank':iban & suffix.str[:2].eq(bic.str[4:6])})
  counts.update(t.value_counts(sort=False).to_dict())
  # Examples illustrate failure classes only; never considered representative.
  for key,g in t.groupby(['fake_prefix','exact_firstline','literal_anywhere','iban_looking','iban_prefix_matches_bank'],sort=False):
   have=sum(e['side']==side and e['class']==list(key) for e in examples)
   for idx in list(g.index)[:max(0,2-have)]:
    examples.append({'side':side,'class':list(key),'source_record':d.at[idx,'source_record'],'account':acc.at[idx],'bic':bic.at[idx],'firstline':first.at[idx]})
  vc=pd.DataFrame({'account':acc,'bic':bic}).value_counts(sort=False)
  con.executemany('INSERT INTO reuse(side,account,bic,n) VALUES(?,?,?,?) ON CONFLICT(side,account,bic) DO UPDATE SET n=n+excluded.n',[(side,k[0],k[1],int(v)) for k,v in vc.items()])
 con.commit();n+=len(d)
 if n%1000000==0:print(n,round(time.monotonic()-start,1),flush=True)
table=pd.DataFrame([list(k)+[v] for k,v in counts.items()],columns=list(t.columns)+['n']);table.to_csv(OUT/'account_detail_joint.csv',index=False)
summary={}
for side in ['ordering','beneficiary']:
 summary[side]={}
 summary[side]['distinct_account_bic_pairs']=con.execute('SELECT count(*) FROM reuse WHERE side=?',(side,)).fetchone()[0]
 summary[side]['distinct_accounts']=con.execute('SELECT count(DISTINCT account) FROM reuse WHERE side=?',(side,)).fetchone()[0]
 summary[side]['accounts_multiple_bics']=con.execute('SELECT count(*) FROM (SELECT account FROM reuse WHERE side=? GROUP BY account HAVING count(*)>1)',(side,)).fetchone()[0]
 summary[side]['repeated_accounts']=con.execute('SELECT count(*) FROM (SELECT account FROM reuse WHERE side=? GROUP BY account HAVING sum(n)>1)',(side,)).fetchone()[0]
 summary[side]['max_account_occurrences']=con.execute('SELECT max(total) FROM (SELECT sum(n) total FROM reuse WHERE side=? GROUP BY account)',(side,)).fetchone()[0]
summary['combined_accounts_multiple_bics']=con.execute('SELECT count(*) FROM (SELECT account FROM reuse GROUP BY account HAVING count(DISTINCT bic)>1)').fetchone()[0]
pd.DataFrame([{'side':e['side'],'class':str(e['class']),'source_record':e['source_record'],'account':e['account'],'bic':e['bic'],'firstline':e['firstline']} for e in examples]).to_csv(OUT/'account_detail_examples.csv',index=False)
(OUT/'account_reuse_summary.json').write_text(json.dumps(summary,indent=2));con.close()
print('ROWS',n);print(json.dumps(summary,indent=2));print(table.groupby(['side','fake_prefix','exact_firstline','literal_anywhere','normalized_anywhere','iban_looking','iban_prefix_matches_bank']).n.sum().to_string())
