"""Reconcile B/C independent counterparty regrouping and model summaries."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

P = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

c_count = pd.read_csv(P / "c/counterparty_count_summary.csv").sort_values(["party", "period"]).reset_index(drop=True)
b_count = pd.read_csv(P / "b/counterparty_count_summary.csv").sort_values(["party", "period"]).reset_index(drop=True)
b_count = b_count.rename(columns={"mean": "mean_payments", "singletons": "singleton_pairs"})
common_count = ["party", "period", "pairs", "payments", "mean_payments", "singleton_pairs", "repeated_pairs", "max_payments"]
pd.testing.assert_frame_equal(c_count[common_count], b_count[common_count], check_dtype=False, rtol=1e-14, atol=1e-10)

c_int = pd.read_csv(P / "c/counterparty_interval_summary.csv").sort_values(["party", "period"]).reset_index(drop=True)
b_int = pd.read_csv(P / "b/counterparty_interval_summary.csv").sort_values(["party", "period"]).reset_index(drop=True)
common_int = ["party", "period", "n", "mean_seconds", "sd_seconds", "p01", "p10", "median", "p90", "p99"]
b_int = b_int.rename(columns={"mean": "mean_seconds", "sd": "sd_seconds"})
pd.testing.assert_frame_equal(c_int[common_int], b_int[common_int], check_dtype=False, rtol=1e-13, atol=1e-8)

c_cohort = pd.read_csv(P / "c/counterparty_cohorts.csv").sort_values(["party", "cohort"]).reset_index(drop=True)
b_cohort = pd.read_csv(P / "b/counterparty_cohorts.csv").sort_values(["party", "cohort"]).reset_index(drop=True)
pd.testing.assert_frame_equal(c_cohort, b_cohort, check_dtype=False)

with open(P / "c/counterparty_manifest.json", encoding="utf-8") as f:
    cm = json.load(f)
with open(P / "b/counterparty_initial.json", encoding="utf-8") as f:
    bm = json.load(f)
assert cm["blank_rows"] == bm["records"] == 9_992_994
assert cm["pairs"] == bm["pairs"] == 8_258_480
assert cm["strict_prior_rows"] == bm["strict_prior_rows"] == 1_734_514
assert cm["pairs"] + cm["strict_prior_rows"] == cm["blank_rows"]
assert int(c_count.loc[c_count.period.eq("full"), "repeated_pairs"].sum()) == 628_578
assert int(c_count.loc[c_count.period.eq("full"), "singleton_pairs"].sum()) == 7_629_902

# Independently recompute count-model total variation from C's observed/expected cells
# and compare it with B's summary values.
cells = pd.read_csv(P / "c/counterparty_count_models.csv")
b_models = pd.read_csv(P / "b/counterparty_count_models.csv")
checks = []
for (party, period), g in cells.groupby(["party", "period"], sort=True):
    n = float(g.observed.sum())
    for model, expected_col in [("zt_poisson", "zt_poisson_expected"), ("positive_geometric", "positive_geometric_expected")]:
        tv = 0.5 * np.abs(g.observed.to_numpy(float) / n - g[expected_col].to_numpy(float) / n).sum()
        reported = float(b_models.loc[(b_models.party.eq(party)) & (b_models.period.eq(period)) & (b_models.model.eq(model)), "tv"].iloc[0])
        assert abs(tv - reported) < 1e-12
        checks.append({"party": party, "period": period, "model": model, "tv": tv})

result = {
    "status": "PASS",
    "blank_rows": cm["blank_rows"],
    "directed_pairs": cm["pairs"],
    "singleton_pairs": 7_629_902,
    "repeated_pairs": 628_578,
    "strict_prior_rows": cm["strict_prior_rows"],
    "equal_time_extra_rows": cm["equal_time_adjacent_pairs"],
    "matched_count_cells": len(c_count),
    "matched_interval_cells": len(c_int),
    "matched_cohort_cells": len(c_cohort),
    "recomputed_count_model_tv_cells": len(checks),
    "shared_input_limit": "B and C independently regrouped/scored C's same 32 raw blank-label partitions; raw filtering was not independently replicated.",
    "final_scope": "Homogeneous observed-pair count and exponential waiting families fail; the data do not identify whether sender activity, receiver popularity, corridor mix, pair affinity, or several mechanisms create the heterogeneity."
}
(OUT / "verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
pd.DataFrame(checks).to_csv(OUT / "count_model_tv_recomputed.csv", index=False)
print(json.dumps(result, indent=2))
