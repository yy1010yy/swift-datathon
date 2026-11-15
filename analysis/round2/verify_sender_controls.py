"""Exact reconciliation of independent sender-history/control scoring."""
from pathlib import Path
import json
import pandas as pd
P=Path(__file__).resolve().parent
b=pd.read_csv(P/'b/sender_independent_summary.csv').sort_values(['label','role']).reset_index(drop=True)
c=pd.read_csv(P/'c/sender_controls_summary.csv').sort_values(['label','role']).reset_index(drop=True)
pd.testing.assert_frame_equal(b,c,check_dtype=False)
assert b.loc[b.role.eq('target'),'n'].sum()==7006
result={'status':'PASS','cells':len(b),'labelled_targets':int(b.loc[b.role.eq('target'),'n'].sum()),
 'checks':'B/C n, usable earlier history, exact same/different-beneficiary amounts, and exact power-of-ten matches agree by label and target/control role.',
 'shared_input':'C full sender-history extraction; B scoring independent, extraction not independently replicated.',
 'limits':['Nearest earlier blank controls may be reused and are not randomized.',
  'An absent observed predecessor cannot refute an unobserved intended invoice or amount.',
  'B/C debate is complete; these are narrow observed-history tests, not tests of latent invoices or intended amounts.']}
(P/'sender_control_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print(b.to_string(index=False))
