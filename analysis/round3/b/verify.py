"""Compact denominator and artifact consistency checks for round-3 B initial."""
from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent
scan=json.loads((P/'scan_manifest.json').read_text());act=json.loads((P/'activity_independence.json').read_text())
c=pd.read_csv(P/'currency_bank_models.csv');r=pd.read_csv(P/'covered_bank_models.csv');m=pd.read_csv(P/'first_intermediary_models.csv')
assert scan['rows']==10_000_000 and scan['status']=='complete'
assert c.train_n.nunique()==c.test_n.nunique()==1 and c.train_n.iloc[0]+c.test_n.iloc[0]==10_000_000
assert r.train_n.iloc[0]+r.test_n.iloc[0]==3_676_720
assert m.train_n.iloc[0]+m.test_n.iloc[0]==3_676_720
assert act['observed_pairs']==8_258_480 and act['blank_payments']==9_992_994
assert act['actual_repeated_pairs']==628_578
out={'status':'PASS','raw_rows':scan['rows'],'non_direct_rows':int(r.train_n.iloc[0]+r.test_n.iloc[0]),
 'currency_test_rows':int(c.test_n.iloc[0]),'blank_pair_rows':act['blank_payments'],
 'observed_pairs':act['observed_pairs'],'repeated_pairs':act['actual_repeated_pairs'],
 'scope':'denominators and artifact consistency; model interpretation independently debated later'}
(P/'verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
