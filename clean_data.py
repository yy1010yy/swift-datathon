"""Conservatively clean and profile the datathon payment CSV in bounded chunks.

Requires Python 3.10+ and pandas 2+: pip install pandas
Run: python clean_data.py
Use --max-rows 10000 --output-dir outputs/preview for a quick trial.
CSV parsing respects quoted multiline fields. No records are deduplicated,
imputed, filtered for outliers, or removed because of an anomaly label.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import time

import numpy as np
import pandas as pd


DEFAULT_INPUT = "swift_umdac_datathon_2026_fictitious_payment_data.csv"
NUMERIC = ["epoch_seconds", "usd_amount", "total_duration",
           "currency_conversion_count", "participant_count"]
INTEGER = set(NUMERIC) - {"usd_amount"}
CATEGORIES = ["currency_code", "continuity_qflag", "transaction_type_code",
              "ordering_type", "beneficiary_type", "anomaly_type"]
REQUIRED = NUMERIC + CATEGORIES + ["ordering_bic8", "beneficiary_bic8", "bic8_path",
    "ordering_account", "beneficiary_account", "ordering_details", "ordering_tokens",
    "beneficiary_details", "beneficiary_tokens", "disclaimer"]
STRUCTURED = NUMERIC + CATEGORIES + ["ordering_bic8", "beneficiary_bic8", "bic8_path"]


def run(args: argparse.Namespace) -> None:
    source = args.input.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cleaned_path = out / "payments_cleaned.csv.gz"
    if source == cleaned_path:
        raise ValueError("The output cannot overwrite the input.")
    # A rerun should be explicit so a partial trial cannot replace a full result.
    if any(out.iterdir()):
        raise FileExistsError(f"Output directory must be empty: {out}")
    started = time.monotonic()
    missing_raw, missing_clean, changes, issues = Counter(), Counter(), Counter(), Counter()
    categories = {c: Counter() for c in CATEGORIES}
    numeric_stats = {c: {"count": 0, "missing": 0, "invalid": 0,
                         "min": None, "max": None, "mean": 0.0, "m2": 0.0}
                     for c in NUMERIC}
    disclaimers: set[str] = set()
    rows = flagged = sampled = 0
    date_min = date_max = None
    header = None
    reader = pd.read_csv(source, dtype="string", keep_default_na=False,
        encoding="utf-8-sig", chunksize=args.chunk_size, nrows=args.max_rows,
        on_bad_lines="error")
    with reader, gzip.open(cleaned_path, "wt", encoding="utf-8", newline="", compresslevel=1) as dest, \
         (out / "quality_issues.csv").open("w", encoding="utf-8", newline="") as quality:
        for chunk in reader:
            chunk.columns = [str(c).strip().lower() for c in chunk.columns]
            if header is None:
                header = list(chunk.columns)
                if len(set(header)) != len(header) or set(header) != set(REQUIRED):
                    raise ValueError(f"Unexpected schema: {header}")
            offset = rows
            missing_raw.update(chunk.eq("").sum().to_dict())
            # Only structured fields lose surrounding whitespace. Account and
            # multiline text formatting may carry useful anomaly evidence.
            for c in STRUCTURED:
                old = chunk[c]
                new = old.str.strip()
                if c in {"currency_code", "ordering_bic8", "beneficiary_bic8",
                          "continuity_qflag", "ordering_type", "beneficiary_type"}:
                    new = new.str.upper()
                changes[c] += int(old.ne(new).sum())
                chunk[c] = new
            missing_clean.update(chunk.eq("").sum().to_dict())
            disclaimers.update(chunk.loc[chunk.disclaimer.ne(""), "disclaimer"].unique())
            chunk = chunk.drop(columns="disclaimer")
            chunk.insert(0, "source_record", np.arange(offset + 1, offset + len(chunk) + 1))
            # Record numbers count logical CSV records, not physical text lines.
            flags = pd.Series("", index=chunk.index, dtype="string")

            def flag(mask: pd.Series, name: str) -> None:
                nonlocal flags
                mask = mask.fillna(False)
                issues[name] += int(mask.sum())
                flags.loc[mask] = flags.loc[mask] + name + ";"

            parsed = {}
            for c in NUMERIC:
                values = pd.to_numeric(chunk[c], errors="coerce")
                finite = pd.Series(np.isfinite(values.to_numpy(dtype=float, na_value=np.nan)), index=chunk.index)
                invalid = chunk[c].ne("") & ~finite
                flag(chunk[c].eq(""), f"missing_{c}")
                flag(invalid, f"invalid_{c}")
                valid = values.where(finite)
                parsed[c] = valid
                flag(valid.lt(0), f"negative_{c}")
                if c in INTEGER:
                    flag(valid.mod(1).ne(0) & valid.notna(), f"non_integer_{c}")
                stat = numeric_stats[c]
                stat["missing"] += int(chunk[c].eq("").sum())
                stat["invalid"] += int(invalid.sum())
                array = valid.dropna().to_numpy(dtype=float)
                if len(array):
                    n, old_n = len(array), stat["count"]
                    mean = float(array.mean())
                    delta = mean - stat["mean"]
                    stat["mean"] += delta * n / (old_n + n)
                    stat["m2"] += float(np.square(array - mean).sum()) + delta**2 * old_n * n / (old_n + n)
                    stat["count"] += n
                    lo, hi = float(array.min()), float(array.max())
                    stat["min"] = lo if stat["min"] is None else min(stat["min"], lo)
                    stat["max"] = hi if stat["max"] is None else max(stat["max"], hi)

            # pandas 3 can represent years beyond Python strftime's range.
            # Reject these for the derived ISO timestamp, retaining source text.
            epoch = parsed["epoch_seconds"]
            dates = pd.to_datetime(epoch.where(epoch.between(-62135596800, 253402300799)),
                                   unit="s", utc=True, errors="coerce")
            flag(parsed["epoch_seconds"].notna() & dates.isna(), "timestamp_out_of_range")
            chunk["payment_datetime_utc"] = dates.dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ").fillna("")
            if dates.notna().any():
                lo, hi = dates.min(), dates.max()
                date_min = lo if date_min is None else min(date_min, lo)
                date_max = hi if date_max is None else max(date_max, hi)
            flag(~chunk.currency_code.str.fullmatch(r"[A-Z]{3}"), "currency_format")
            flag(~chunk.continuity_qflag.isin(["Y", "N"]), "unknown_continuity_flag")
            for c in ["ordering_bic8", "beneficiary_bic8"]:
                flag(~chunk[c].str.fullmatch(r"[A-Z0-9]{8}"), f"invalid_{c}_format")
            path = chunk.bic8_path.str.split(";")
            flag(path.str.len().ne(parsed["participant_count"]) & parsed["participant_count"].notna(), "path_participant_count_mismatch")
            flag(path.str[0].ne(chunk.ordering_bic8), "path_ordering_endpoint_mismatch")
            flag(path.str[-1].ne(chunk.beneficiary_bic8), "path_beneficiary_endpoint_mismatch")
            for c in ["ordering_account", "beneficiary_account", "ordering_details", "beneficiary_details", "bic8_path"]:
                flag(chunk[c].str.strip().eq(""), f"missing_{c}")
            chunk["quality_flags"] = flags.str.rstrip(";")
            bad = chunk.quality_flags.ne("")
            chunk.loc[bad, ["source_record", "quality_flags"]].to_csv(quality, index=False, header=rows == 0)
            flagged += int(bad.sum())
            for c in CATEGORIES:
                categories[c].update(chunk[c].value_counts(dropna=False).to_dict())
            chunk.to_csv(dest, index=False, header=rows == 0)
            if sampled < 1000:
                sample = chunk.head(1000 - sampled)
                sample.to_csv(out / "payments_sample.csv", index=False, mode="w" if sampled == 0 else "a", header=sampled == 0)
                sampled += len(sample)
            rows += len(chunk)
            print(f"Processed {rows:,} records ({time.monotonic() - started:.0f}s)", flush=True)

    if rows == 0:
        raise ValueError("No data records found.")
    for stat in numeric_stats.values():
        stat["std"] = (stat.pop("m2") / (stat["count"] - 1)) ** 0.5 if stat["count"] > 1 else None
        if not stat["count"]:
            stat["mean"] = None
    profile = {
        "source": str(source), "source_bytes": source.stat().st_size,
        "scope": "full file" if args.max_rows is None else f"first {args.max_rows:,} records at most",
        "records": rows, "original_columns": header, "cleaned_columns": len(header) + 2,
        "flagged_records": flagged, "issue_counts": dict(issues),
        "missing_before": dict(missing_raw), "missing_after": dict(missing_clean),
        "normalized_cells": dict(changes), "numeric_statistics": numeric_stats,
        "date_range_utc": [str(date_min), str(date_max)],
        "category_counts": {c: dict(v) for c, v in categories.items()},
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "limitations": ["No unique transaction ID provided; duplicates retained and not measured.",
            "Blank anomaly labels retained; their meaning is undocumented.",
            "The case brief defines duration in seconds, B as business and C as consumer.",
            "Numeric summaries use floating-point arithmetic, not accounting reconciliation.",
            "Sample contains the first 1,000 records and is not a random sample."]}
    (out / "profile.json").write_text(json.dumps(profile, indent=2, allow_nan=False), encoding="utf-8")
    (out / "dataset_disclaimer.txt").write_text("\n\n".join(sorted(disclaimers)), encoding="utf-8")
    pd.DataFrame([{"column": c, "missing_before": missing_raw[c], "missing_after": missing_clean[c],
                   "normalized_cells": changes[c]} for c in header]).to_csv(out / "column_profile.csv", index=False)
    pd.DataFrame([{"column": c, "value": k, "count": n} for c, counts in categories.items()
                  for k, n in counts.most_common()]).to_csv(out / "category_counts.csv", index=False)
    labels = categories["anomaly_type"]
    labeled = rows - labels.get("", 0)
    report = ["# Payment data: initial profile", "", f"Scope: {profile['scope']}.",
        f"Records: {rows:,}. Original columns: {len(header)}. Flagged records: {flagged:,}.",
        f"UTC timestamp range: {date_min} to {date_max}.",
        f"Nonblank anomaly labels: {labeled:,} ({labeled / rows:.4%}).", "",
        "## Cleaning applied", "",
        "Column names use lowercase. Structured fields are trimmed, and currency/BIC/flag codes use uppercase. "
        "The source disclaimer is saved separately. source_record, payment_datetime_utc and quality_flags are added. "
        "Original numeric text is retained, including invalid values. No missing values are imputed, "
        "no records are removed, and account/text/token fields retain original formatting.", "",
        "## Numeric summary", "", "| Column | Valid | Missing | Invalid | Min | Mean | Max |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for c, s in numeric_stats.items():
        report.append(f"| {c} | {s['count']:,} | {s['missing']:,} | {s['invalid']:,} | {s['min']} | {s['mean']} | {s['max']} |")
    for c in CATEGORIES:
        report += ["", f"## {c}", ""]
        report += [f"- {k or '(blank)'}: {n:,} ({n / rows:.4%})" for k, n in categories[c].most_common(20)]
    report += ["", "## Quality checks", ""]
    report += [f"- {name}: {count:,}" for name, count in issues.items() if count] or ["No issues detected by the implemented checks."]
    report += ["", "Checks are structural diagnostics, not proof of fraud or incorrect payments. "
               "Path mismatches may reflect transaction routing semantics and are preserved for review.",
               "", "## Interpretation and limits", ""]
    report += [f"- {note}" for note in profile["limitations"]]
    report += ["- ANOMALY_TYPE is a potential target label. Exclude it from model inputs. "
               "Review synthetic token fields for leakage before modeling.",
               "- The file is fictitious and generated by rules, random numbers and Faker. "
               "Findings describe this synthetic dataset.", "",
               "## Outputs", "", "payments_cleaned.csv.gz: all cleaned records (pandas can read gzip directly).",
               "quality_issues.csv: flagged record numbers and reasons.",
               "profile.json, column_profile.csv, category_counts.csv: full-scope profiling results.",
               "payments_sample.csv: first 1,000 cleaned records for inspection."]
    (out / "data_overview.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Done: {rows:,} records; {flagged:,} flagged. Report: {out / 'data_overview.md'}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "outputs" / "cleaned")
    parser.add_argument("--chunk-size", type=int, default=25000)
    parser.add_argument("--max-rows", type=int, default=None)
    options = parser.parse_args()
    if options.chunk_size <= 0 or (options.max_rows is not None and options.max_rows <= 0):
        parser.error("chunk-size and max-rows must be positive")
    run(options)
