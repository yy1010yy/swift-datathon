"""Run documented EDA blocks and save their actual outputs in an executed notebook.

Run from any directory: .venv/Scripts/python.exe analysis/run_initial_eda.py
Only pandas/numpy required. No Jupyter installation needed to generate the notebook.
"""
from pathlib import Path
import contextlib
import io
import json
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = [
("01 · Setup and provenance", """All input rows are retained. Full-file aggregates, never the first-1,000 preview, drive comparisons. Account identifiers remain strings. Amount is USD; duration is seconds; UTC is not customer local time. Blank labels mean no recorded anomaly label. Definitions: case brief appendix pp. 3–4. Questions and untested theories: analysis/questions.md. Independent reviews: analysis/reviews/.""", r'''
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, platform, sys, time
import pandas as pd
import numpy as np
root = Path(ROOT)
out = root / 'outputs/eda_initial'
out.mkdir(parents=True, exist_ok=True)
source = root / 'outputs/cleaned/payments_cleaned.csv.gz'
profile = json.loads((root / 'outputs/cleaned/profile.json').read_text())
manifest = {'started_utc': datetime.now(timezone.utc).isoformat(),
 'input': str(source), 'input_bytes': source.stat().st_size,
 'input_mtime_ns': source.stat().st_mtime_ns, 'python': sys.version,
 'pandas': pd.__version__, 'numpy': np.__version__,
 'script_sha256': hashlib.sha256((root/'analysis/run_initial_eda.py').read_bytes()).hexdigest(),
 'scope': 'full cleaned file; no exclusions; no deduplication',
 'definitions_source': 'case brief appendix pp. 3–4',
 'note': 'File identity uses size/mtime, not a content checksum; profile retained unchanged.'}
print(json.dumps(manifest, indent=2))
print('Historical profile limitation is stale: duration and B/C meanings ARE defined by appendix.')
'''),
("02 · Full-file scan", """Question R1 (relationship/comparison): within each route type and continuity flag, does visible BIC entry count equal participant_count? Count entries matching [A-Z0-9]{8}; count literal ... separately; retain unknown tokens and repeated BICs. Difference = reported participants minus visible entries. Cross-tabulate all existing routing diagnostics before interpreting them. Month is a descriptive stability check, not a pre-registered holdout.""", r'''
cols = ['source_record','epoch_seconds','bic8_path','participant_count','continuity_qflag',
 'transaction_type_code','quality_flags','currency_conversion_count','anomaly_type',
 'ordering_type','beneficiary_type','currency_code','usd_amount','total_duration',
 'ordering_bic8','beneficiary_bic8']
route = Counter(); monthly = Counter(); diagnostics = Counter(); labels = Counter()
party = Counter(); hours = Counter(); fx = Counter(); examples = []
rows = 0; minimum = None; maximum = None; bad_tokens = 0; quality_rows = 0
numeric = {c: {'count': 0, 'sum': 0.0, 'min': float('inf'), 'max': float('-inf')}
           for c in ['usd_amount','total_duration']}
started = time.monotonic()
for d in pd.read_csv(source, usecols=cols, dtype=str, keep_default_na=False, chunksize=100000):
    dates = pd.to_datetime(pd.to_numeric(d.epoch_seconds, errors='raise'), unit='s', utc=True)
    p = pd.to_numeric(d.participant_count, errors='raise').astype(int)
    paths = d.bic8_path.str.split(';')
    v = paths.map(lambda a: sum(bool(__import__('re').fullmatch('[A-Z0-9]{8}', t)) for t in a))
    gaps = paths.map(lambda a: a.count('...'))
    unknown = paths.str.len() - v - gaps
    unique = paths.map(lambda a: len({t for t in a if __import__('re').fullmatch('[A-Z0-9]{8}', t)}))
    x = pd.DataFrame({'continuity': d.continuity_qflag, 'route_type': d.transaction_type_code,
        'visible_entries': v, 'gap_entries': gaps, 'unknown_entries': unknown,
        'participant_count': p, 'distinct_visible_bics': unique, 'difference': p-v})
    route.update(x.value_counts(sort=False).to_dict())
    m = x[['continuity','route_type','difference']].copy()
    m['month_utc'] = dates.dt.strftime('%Y-%m')
    monthly.update(m.value_counts(sort=False).to_dict())
    base = ['continuity','route_type']
    for flag in ['path_participant_count_mismatch','path_ordering_endpoint_mismatch',
                 'path_beneficiary_endpoint_mismatch']:
        f = x[base].copy(); f['present'] = d.quality_flags.str.split(';').map(lambda a: flag in a)
        diagnostics.update({(flag,)+k: n for k,n in f.value_counts(sort=False).items()})
    labels.update(d.anomaly_type.value_counts().to_dict())
    party.update(d[['ordering_type','beneficiary_type']].value_counts().to_dict())
    h = pd.DataFrame({'hour_utc': dates.dt.hour, 'weekday_utc': dates.dt.dayofweek,
                      'ordering_type': d.ordering_type, 'beneficiary_type': d.beneficiary_type})
    hours.update(h.value_counts(sort=False).to_dict())
    f = x[base+['participant_count']].copy()
    f['fx_steps'] = pd.to_numeric(d.currency_conversion_count, errors='raise').astype(int)
    fx.update(f.value_counts(sort=False).to_dict())
    for c in numeric:
        a = pd.to_numeric(d[c], errors='raise')
        numeric[c]['count'] += len(a); numeric[c]['sum'] += float(a.sum())
        numeric[c]['min'] = min(numeric[c]['min'], float(a.min()))
        numeric[c]['max'] = max(numeric[c]['max'], float(a.max()))
    # Deterministic illustrative examples: first two per continuity/type/difference class.
    for key, ix in x.groupby(['continuity','route_type','difference'], sort=False).groups.items():
        have = sum(e['_class'] == list(key) for e in examples)
        for idx in list(ix)[:max(0,2-have)]:
            e = d.loc[idx,['source_record','bic8_path','participant_count','continuity_qflag',
                'transaction_type_code','ordering_bic8','beneficiary_bic8','quality_flags']].to_dict()
            e['_class'] = list(key); examples.append(e)
    bad_tokens += int(unknown.sum()); quality_rows += int(d.quality_flags.ne('').sum())
    rows += len(d)
    minimum = dates.min() if minimum is None else min(minimum,dates.min())
    maximum = dates.max() if maximum is None else max(maximum,dates.max())
    if rows % 1000000 == 0: print(f'{rows:,} rows scanned; {time.monotonic()-started:.1f}s')
print(f'Completed {rows:,} logical records; UTC range {minimum} to {maximum}')
print(f'Unknown path entries: {bad_tokens:,}; records with any existing diagnostic: {quality_rows:,}')
'''),
("03 · Label coverage and population controls", """Question A0 (composition): how many rows have each recorded label, including blank? Six observed nonblank labels versus five documented; CUSTOMER_RECALL has no supplied definition. This reconciles coverage, not the anomaly-generating mechanism. Numeric means are full-population floating-point summaries, not robust descriptions of typical amounts.""", r'''
def save_counter(counter, names, filename):
    table = pd.DataFrame([list(k if isinstance(k,tuple) else (k,))+[int(n)] for k,n in counter.items()],
                         columns=names+['records']).sort_values(names).reset_index(drop=True)
    table.to_csv(out/filename,index=False)
    return table
label_table = save_counter(labels,['anomaly_type'],'labels.csv')
label_table['meaning'] = label_table.anomaly_type.map(lambda x: 'no recorded anomaly label' if x=='' else
    ('not defined in supplied appendix' if x=='CUSTOMER_RECALL' else 'defined in appendix'))
label_table['percent_all_rows'] = 100*label_table.records/rows
label_table.to_csv(out/'labels.csv',index=False)
print(label_table.to_string(index=False))
print('\nParty pair composition (not an inferred business rule):')
print(save_counter(party,['ordering_type','beneficiary_type'],'party_pairs.csv').to_string(index=False))
for c,s in numeric.items(): s['mean'] = s['sum']/s['count']
print('\nFull-population numeric controls:',json.dumps(numeric,indent=2))
'''),
("04 · Routing cross-tabs and stability", """Report denominators explicitly. Tables retain sparse and disagreeing cells. A match describes an observed encoding relationship; it cannot establish economic causality or recover the hidden institutions. Endpoint diagnostics are checked separately from participant discrepancies.""", r'''
routes = save_counter(route,['continuity','route_type','visible_entries','gap_entries','unknown_entries',
    'participant_count','distinct_visible_bics','difference'],'route_counts.csv')
months = save_counter(monthly,['continuity','route_type','difference','month_utc'],'route_month.csv')
flags = save_counter(diagnostics,['diagnostic','continuity','route_type','present'],'route_diagnostics.csv')
save_counter(hours,['hour_utc','weekday_utc','ordering_type','beneficiary_type'],'time_composition.csv')
save_counter(fx,['continuity','route_type','participant_count','fx_steps'],'routing_fx.csv')
summary = routes.assign(equal_records=lambda t: t.records*t.difference.eq(0),
    gap_records=lambda t: t.records*t.gap_entries.gt(0),
    repeated_bic_records=lambda t: t.records*t.visible_entries.ne(t.distinct_visible_bics),
    reported_minus_visible_sum=lambda t: t.records*t.difference).groupby(['continuity','route_type']).agg(
    records=('records','sum'), equal_records=('equal_records','sum'),
    gap_records=('gap_records','sum'), repeated_bic_records=('repeated_bic_records','sum'),
    reported_minus_visible_sum=('reported_minus_visible_sum','sum')).reset_index()
summary['equal_percent'] = 100*summary.equal_records/summary.records
summary['mean_reported_minus_visible'] = summary.reported_minus_visible_sum/summary.records
summary.to_csv(out/'route_summary.csv',index=False)
print(summary.to_string(index=False))
print('\nAll observed participant-minus-visible differences:')
print(routes.groupby(['continuity','difference']).records.sum().to_string())
print('\nDiagnostics by continuity/type (both present and absent):')
print(flags.to_string(index=False))
print('\nMonthly comparison:')
print(months.to_string(index=False))
pd.DataFrame([{k:v for k,v in e.items() if k!='_class'} for e in examples]).to_csv(out/'route_examples.csv',index=False)
'''),
("05 · Reconciliation and completion", """Assertions validate counts against the existing full profile. No corrections are written into the cleaned data or historical profile. Separate metadata records the appendix corrections. See analysis/progress.md for reviewed wording and remaining tests; this notebook intentionally stops at initial EDA.""", r'''
assert rows == profile['records'] == 10000000
assert dict(labels) == profile['category_counts']['anomaly_type']
assert labels['CUSTOMER_RECALL'] == 317
assert quality_rows == profile['flagged_records']
assert routes.records.sum() == months.records.sum() == rows
assert sum(party.values()) == sum(hours.values()) == sum(fx.values()) == rows
for flag in flags.diagnostic.unique():
    a = flags[flags.diagnostic.eq(flag)]
    assert a.records.sum() == rows
    assert int(a.loc[a.present,'records'].sum()) == profile['issue_counts'][flag]
manifest.update({'records': rows, 'date_min_utc':str(minimum),'date_max_utc':str(maximum),
 'elapsed_scan_seconds': round(time.monotonic()-started,2), 'all_controls_passed':True,
 'completed_utc': datetime.now(timezone.utc).isoformat(),
 'definition_corrections': {'total_duration':'seconds','B':'business','C':'consumer',
 'usd_amount':'normalized USD','tokens':'derived text patterns',
 'gap':'literal ... is not a visible institution','blank_label':'no recorded anomaly label'}})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('PASS: row counts, labels, diagnostics and all aggregate denominators reconcile with full profile.')
print('Saved tables:', ', '.join(p.name for p in sorted(out.glob('*.csv'))))
'''),
]

def main():
    cells = []
    env = {'ROOT': str(ROOT)}
    nb = {'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{
        'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python','version':'3.10+'}},'cells':cells}
    path = ROOT/'analysis/initial_eda.ipynb'
    def write(): path.write_text(json.dumps(nb,indent=1,ensure_ascii=False),encoding='utf-8')
    cells.append({'cell_type':'markdown','metadata':{},'id':'intro','source':[
        '# Initial payment EDA\nExecuted block outputs; full 10-million-row population.\n',
        'Regenerate with `.venv/Scripts/python.exe analysis/run_initial_eda.py`.\n',
        'To run interactively from this folder, set ROOT to the project directory before cell 1.\n']})
    for i,(title,note,code) in enumerate(BLOCKS,1):
        cells.append({'cell_type':'markdown','metadata':{},'id':f'note-{i}',
                      'source':[f'## {title}\n\n{note}']})
        if i==1:
            code = "ROOT = str(__import__('pathlib').Path.cwd().parent if __import__('pathlib').Path.cwd().name == 'analysis' else __import__('pathlib').Path.cwd())\n"+code
        cell = {'cell_type':'code','metadata':{},'id':f'code-{i}', 'execution_count':i,
                'source':code.splitlines(keepends=True),'outputs':[]}
        cells.append(cell)
        captured = io.StringIO()
        print(f'Running block {i}: {title}',flush=True)
        try:
            with contextlib.redirect_stdout(captured): exec(compile(code,f'EDA block {i}','exec'),env)
        except Exception:
            cell['outputs'].append({'output_type':'stream','name':'stdout','text':captured.getvalue().splitlines(True)})
            cell['outputs'].append({'output_type':'error','ename':'ExecutionError','evalue':'block failed',
                                    'traceback':traceback.format_exc().splitlines()})
            write(); raise
        cell['outputs'].append({'output_type':'stream','name':'stdout','text':captured.getvalue().splitlines(True)})
        write()
        print(captured.getvalue(),flush=True)
    print(f'Executed notebook: {path}',flush=True)

if __name__ == '__main__': main()
