"""Render two initial EDA charts and append their executed code/output to the notebook.

Run after run_initial_eda.py; only pandas and Python standard library required.
Charts are SVG, so text and counts remain inspectable without plotting dependencies.
"""
from pathlib import Path
import json

CODE = r'''
from pathlib import Path
from html import escape
import pandas as pd
root = Path(ROOT)
out = root/'outputs/eda_initial'
summary = pd.read_csv(out/'route_summary.csv', keep_default_na=False)
labels = pd.read_csv(out/'labels.csv', keep_default_na=False)
import json
run = json.loads((out/'manifest.json').read_text())
def bars(title, subtitle, names, values, axis_note, path, formatter):
    width, height = 1040, 170+len(names)*55
    maximum = max(values) or 1
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Arial, sans-serif" fill="#172f43">',
        f'<text x="24" y="34" font-size="23">{escape(title)}</text>',
        f'<text x="24" y="65" font-size="14">{escape(subtitle)}</text>']
    for i,(name,value) in enumerate(zip(names,values)):
        y=100+i*55
        parts += [f'<text x="24" y="{y+20}" font-size="14">{escape(str(name))}</text>',
            f'<rect x="295" y="{y}" width="{540*value/maximum:.3f}" height="28" fill="#227b82"/>',
            f'<text x="{305+540*value/maximum:.3f}" y="{y+20}" font-size="14">{escape(formatter(value))}</text>']
    parts += [f'<text x="24" y="{height-22}" font-size="13">{escape(axis_note)}</text>','</g></svg>']
    path.write_text('\n'.join(parts),encoding='utf-8')
    return '\n'.join(parts)
svg_route = bars('R1: Reported participants equal visible BIC entries in every stratum',
    f"10,000,000 payments; {run['date_min_utc'][:10]} to {run['date_max_utc'][:10]} UTC. Gaps excluded from BIC counts.",
    [f'{r.continuity} / {r.route_type} (n={r.records:,})' for r in summary.itertuples()],
    summary.equal_percent.tolist(),'Bar axis: matching records within stratum (%); all bars start at zero.',
    out/'R1_visible_participants.svg',lambda v:f'{v:.1f}%')
nonblank = labels[labels.anomaly_type.ne('')].sort_values('records',ascending=False)
svg_labels = bars('A0: Six recorded nonblank anomaly labels; recall is undefined',
    '10,000,000 payments: 7,006 recorded labels; 9,992,994 blank = no recorded anomaly label (not proven normal).',
    nonblank.anomaly_type.tolist(),nonblank.records.tolist(),
    'Bar axis: records (linear, zero baseline). CUSTOMER_RECALL is not described in the supplied appendix.',
    out/'A0_label_counts.svg',lambda v:f'{int(v):,}')
print('Saved R1_visible_participants.svg and A0_label_counts.svg; counts come from executed full-file aggregates.')
'''

def main():
    root = Path(__file__).resolve().parents[1]
    env={'ROOT':str(root)}
    exec(CODE,env)
    path=root/'analysis/initial_eda.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    nb['cells']=[c for c in nb['cells'] if c.get('id') not in ['charts-note','charts-code']]
    nb['cells'] += [
        {'cell_type':'markdown','id':'charts-note','metadata':{},'source':[
            '## 06 · Initial charts\nR1 is an observed encoding relationship, not proof of the hidden generator. '
            'A0 is label coverage, not an anomaly mechanism. Review: `analysis/progress.md`.']},
        {'cell_type':'code','id':'charts-code','metadata':{},'source':CODE.splitlines(True),
         'execution_count':6,'outputs':[
             {'output_type':'display_data','metadata':{},'data':{'image/svg+xml':env['svg_route']}},
             {'output_type':'display_data','metadata':{},'data':{'image/svg+xml':env['svg_labels']}}]}]
    path.write_text(json.dumps(nb,indent=1,ensure_ascii=False),encoding='utf-8')
    print('Added executed chart cell to',path)

if __name__=='__main__': main()
