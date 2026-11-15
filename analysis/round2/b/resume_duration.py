"""Resume B postprocessing from completed numeric cache after logged uint8 overflow.

The initial scan and amount results are retained. This executes the corrected suffix
of investigate.py without a second raw-data scan.
"""
from pathlib import Path
import json, time, hashlib,re
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
CACHE=ROOT/'outputs/eda_round2'
source=ROOT/'outputs/cleaned/payments_cleaned.csv.gz'
a=np.load(CACHE/'b_rows.npy',mmap_mode='r')
assert len(a)==10000000
n=len(a);start=time.monotonic()
routes=['Direct','Indirect','Covered']
period=(a['epoch']>=1688169600).astype('u1')
text=(OUT/'investigate.py').read_text()
suffix=text[text.index('# Exact route/fx/participant/period duration summaries:'):]
exec(compile(suffix,str(OUT/'investigate.py')+' corrected duration suffix','exec'))
manifest=json.loads((OUT/'manifest.json').read_text())
manifest['duration_postprocess_seconds']=manifest.pop('elapsed_seconds')
scan=re.search(r'10,000,000 rows / ([0-9.]+)s',(OUT/'run.log').read_text())
manifest['full_scan_seconds']=float(scan.group(1)) if scan else None
manifest['execution_correction']='Full scan and amount outputs completed, uint8 duration key overflow retained in run.log; corrected suffix resumed from full10M cache in duration_run.log.'
manifest['corrected_suffix_source_sha256']=hashlib.sha256((OUT/'investigate.py').read_bytes()).hexdigest()
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
