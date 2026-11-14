"""Independent routing challenge. Run from project root; full selected-column scan."""
from pathlib import Path
from collections import Counter
import json, re, time
import pandas as pd

OUT = Path('analysis/reviews/b')
OUT.mkdir(parents=True, exist_ok=True)
counts = Counter()
labels = Counter()
examples = []
rows = 0
started = time.monotonic()
cols = ['source_record', 'epoch_seconds', 'continuity_qflag', 'transaction_type_code',
        'participant_count', 'bic8_path', 'ordering_bic8', 'beneficiary_bic8', 'anomaly_type']
for chunk in pd.read_csv('outputs/cleaned/payments_cleaned.csv.gz', usecols=cols,
                         dtype=str, keep_default_na=False, chunksize=100000):
    labels.update(chunk.anomaly_type)
    # This independent implementation checks syntax before counting visible entries.
    for rec in chunk[cols].itertuples(index=False, name=None):
        source, epoch, continuity, route, participants, path, sender, receiver, label = rec
        entries = path.split(';')
        visible = [p for p in entries if re.fullmatch('[A-Z0-9]{8}', p)]
        distinct = len(set(visible))
        gaps = entries.count('...')
        invalid = len(entries) - len(visible) - gaps
        p = int(participants)
        period = 'early' if int(epoch) < 1688169600 else 'late'  # July 1 UTC
        key = (continuity, route, period, p, len(entries), len(visible), distinct,
               gaps, invalid, entries[0] != sender, entries[-1] != receiver)
        counts[key] += 1
        if len(examples) < 24 and (distinct != len(visible) or invalid or
                                    (len(visible) != p and continuity == 'Y')):
            examples.append(dict(source_record=source, path=path, participants=p,
                                 continuity=continuity, route=route))
    rows += len(chunk)
    if rows % 1000000 == 0:
        print(f'{rows:,} records, {time.monotonic()-started:.1f}s', flush=True)

fields = ['continuity', 'route', 'period', 'participants', 'entries', 'visible',
          'distinct_visible', 'gaps', 'invalid', 'sender_mismatch', 'receiver_mismatch']
table = pd.DataFrame([dict(zip(fields, k), n=n) for k,n in counts.items()])
table.to_csv(OUT/'joint_counts.csv', index=False)
pd.DataFrame([{'label': k or 'no recorded anomaly label', 'n': n} for k,n in labels.items()]).to_csv(OUT/'labels.csv', index=False)
summary=[]
for (continuity, route), sub in table.groupby(['continuity','route']):
    def n(mask): return int(sub.loc[mask,'n'].sum())
    summary.append(dict(continuity=continuity, route=route, rows=int(sub.n.sum()),
        visible_equal=n(sub.visible==sub.participants), distinct_equal=n(sub.distinct_visible==sub.participants),
        entries_equal=n(sub.entries==sub.participants), gapped=n(sub.gaps>0),
        repeated_visible=n(sub.visible!=sub.distinct_visible), invalid=n(sub.invalid>0),
        sender_mismatch=n(sub.sender_mismatch), receiver_mismatch=n(sub.receiver_mismatch)))
pd.DataFrame(summary).to_csv(OUT/'summary.csv',index=False)
(OUT/'examples.json').write_text(json.dumps(examples,indent=2),encoding='utf-8')
(OUT/'run.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-started,'split_epoch':1688169600},indent=2),encoding='utf-8')
print(pd.DataFrame(summary).to_string(index=False))
print(labels)
