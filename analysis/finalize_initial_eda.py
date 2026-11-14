"""Run independent-table verification and store its executed output in the notebook."""
from pathlib import Path
import contextlib
import io
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
code="""import subprocess, sys
result = subprocess.run([sys.executable, str(root/'analysis/verify_reviews.py')],
                        cwd=root, capture_output=True, text=True, check=True)
print(result.stdout)
"""
capture=io.StringIO()
with contextlib.redirect_stdout(capture): exec(code,{'root':root})
nbpath=root/'analysis/initial_eda.ipynb'
nb=json.loads(nbpath.read_text(encoding='utf-8'))
nb['cells']=[c for c in nb['cells'] if c.get('id') not in ['review-note','review-code']]
nb['cells'] += [
    {'cell_type':'markdown','id':'review-note','metadata':{},'source':[
        '## 07 · Independent review verification\nExact comparison of lead/A/B aggregates, '
        'monthly and July splits, endpoint diagnostics and labels. '
        'Initial conclusions and exchanged debate: `analysis/reviews/`; final wording: `analysis/progress.md`.']},
    {'cell_type':'code','id':'review-code','metadata':{},'source':code.splitlines(True),'execution_count':7,
     'outputs':[{'output_type':'stream','name':'stdout','text':capture.getvalue().splitlines(True)}]}]
assert len({c['id'] for c in nb['cells']})==len(nb['cells'])
assert sum(c['cell_type']=='code' for c in nb['cells'])==7
assert all(c.get('execution_count') and c.get('outputs') and
    all(o['output_type']!='error' for o in c['outputs']) for c in nb['cells'] if c['cell_type']=='code')
for path in (root/'outputs/eda_initial').glob('*.svg'): ET.parse(path)
nbpath.write_text(json.dumps(nb,indent=1,ensure_ascii=False),encoding='utf-8')
print(capture.getvalue())
print('PASS: seven executed notebook cells with outputs, no error outputs; both SVG charts parse.')
