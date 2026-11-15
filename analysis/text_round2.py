"""Full-population text-pattern census; actual outputs indexed in round2/text/."""
from pathlib import Path
from collections import Counter
import re,json,time
import pandas as pd
root=Path(__file__).resolve().parents[1]
out=root/'analysis/round2/text';out.mkdir(parents=True,exist_ok=True)
cols=['ordering_details','ordering_tokens','beneficiary_details','beneficiary_tokens',
      'ordering_type','beneficiary_type','ordering_bic8','beneficiary_bic8','epoch_seconds']
counts=Counter(); families=Counter(); rows=0;started=time.monotonic()
for d in pd.read_csv(root/'outputs/cleaned/payments_cleaned.csv.gz',usecols=cols,dtype=str,keep_default_na=False,chunksize=100000):
    period=pd.to_datetime(d.epoch_seconds.astype('int64'),unit='s',utc=True).dt.strftime('%Y-%m')
    for side in ['ordering','beneficiary']:
        z=d[[side+'_details',side+'_tokens',side+'_type',side+'_bic8']].copy()
        z['month']=period
        # Unique combinations per chunk preserve exact frequency while avoiding repeated parsing.
        for (detail,tokens,party,bic,month),n in z.value_counts(sort=False).items():
            cc=re.findall(r'<country_code:([^>]+)>',tokens)
            fs=set(re.findall(r'<([^:>]+)(?=[:>])',tokens))
            parts=re.split(r'\\n|\n',detail)
            nonfirst=parts[1:]
            counts[(side,party,month,'line35_token','yes' if '<line_break:35>' in tokens else 'no')]+=n
            counts[(side,party,month,'newline_style',('literal' if '\\n' in detail else '')+('actual' if '\n' in detail else '') or 'none')]+=n
            counts[(side,party,month,'starts_slash',str(detail.startswith('/')))]+=n
            counts[(side,party,month,'country_token_count',str(len(cc)))]+=n
            if cc:
                counts[(side,party,month,'country_matches_bank',str(cc[-1]==bic[4:6]))]+=n
            counts[(side,party,month,'line35_vs_lengths',str(('<line_break:35>' in tokens,any(len(p)==35 for p in nonfirst),max(map(len,parts)))))]+=n
            for f in fs:families[(side,party,month,f)]+=n
    rows+=len(d)
    if rows%1000000==0:print(rows,round(time.monotonic()-started,1),flush=True)
assert rows==10000000
pd.DataFrame([(*k,v) for k,v in counts.items()],columns=['side','party','month','feature','value','records']).to_csv(out/'patterns.csv',index=False)
pd.DataFrame([(*k,v) for k,v in families.items()],columns=['side','party','month','token_family','records']).to_csv(out/'families.csv',index=False)
(out/'manifest.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-started,'scope':'full file; both sides, no exclusions','method':'token families count once per detail field; country comparison uses last country_code token and bank BIC characters5-6; line lengths split literal backslash-n OR newline'},indent=2))
print('COMPLETE',rows,flush=True)
