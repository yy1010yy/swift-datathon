"""Compact consistency checks for A's completed entity/activity challenge."""
from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent
m=json.loads((P/'entity_network_manifest.json').read_text())
s=pd.read_csv(P/'activity_null_summary.csv')
assert m['status']=='complete'
assert m['pair_rows']==8_258_480 and m['blank_payments']==9_992_994
assert m['sample_pairs']==int(s.sample_pairs.sum())
assert m['sample_payments']==int(s.sample_payments.sum())
assert set(s.party)=={'BB','BC','CB','CC'}
assert (s.observed_repeat_share>s.expected_repeat_share_activity_null).all()
result={'status':'PASS','pairs':m['pair_rows'],'payments':m['blank_payments'],
        'sample_pairs':m['sample_pairs'],
        'observed_over_expected_range':[float(s.observed_over_expected.min()),float(s.observed_over_expected.max())],
        'scope':'Exact denominator checks and all four activity-null effect directions.'}
(P/'entity_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
