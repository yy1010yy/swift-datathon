# A additional independent calculations and timing of exchange

## Text-token/bank alignment

Independent raw10M scan completed276.0sec; `text_initial.log` contains outputs before
the lead's exchange. Explicit country token present on6,084,595 ordering sides; all
match that side's BIC country-like code. Missing3,915,405 are kept separate. Beneficiary
country present6,107,358, of which59,826 match ownbank and88,333 match orderingbank;
missing3,892,642. Results by month/type are in `text_country_joint.csv`.
Neither missing tokens nor mismatches prove foreign residence, random assignment or
corrupt data. The token is an engineered summary, not independent customer geography.

## Internal FX zones: blind reconstruction and retrospective temporal validation

The all-Direct zero-FX-country-pair graph was computed independently before the lead
sent its same hypothesis: it predicts all6,323,280 Direct FX counts; modal-currency
heuristic had32 exceptions. This is discovery, not temporal validation.

Next, a new raw full-file pass learned connected components using only pre-July
Direct zero-FX paths, freezing229 country-like codes. Count adjacent visible code-zone
changes and compare to reported FX on all other route groups and July. All codes
were known. It predicts9,999,964/10M counts;36 are one conversion overpredictions.
July has14 exceptions (Direct4,Indirect9,Covered1), early22. Exact strata and training
map are `fx_zone_validation.csv` / `fx_training_zones.csv`. Inspecting fullDirect
zero-FX edges missing from early training reveals four later links, each observed once:
LC–GD, KN–GD, AI–LC (currencyXCD) and WF–NC (currencyXPF). No external mapping used.

This supports a currency-zone boundary mechanism rather than every geographic-border
conversion. FullDirect-trained graph applied to excluded nonDirect routes is the next
cross-group validation, recorded separately so perfect discovery never replaces the
near-exact temporal result. Do not infer hidden banks or uniquely identify causal order.

The ALLDirect-trained graph predicts3,676,707/3,676,720 excluded nonDirect rows;
13 exceptions overpredict by1 and involveFM–US/MP–US transitions lacking direct
zeroFX evidence. It resolves23/36 earlier-map failures. These are recorded limits,
not silently removed rows. See `fx_route_group_validation.csv` and
`fx_early_exception_sequences.csv`; inference uses no external currency mapping.

Residual-constraint discovery then tested candidate merging FM–US and MP–US groups.
Base fullDirect graph misses13/10M; FM–US-only misses5; MP–US-only misses8;
both merges explain10,000,000/10,000,000 FX counts, including all gap statuses and
route types. This all-data refined fit is **not** heldout validation. It must appear
alongside, not replace, the earlier frozen temporal and route-group comparisons.
Artifacts: `fx_constraint_refinement.csv`, `fx_refined_zones.csv`, actual log and script.

## Romance recurrence, independent before C recurrence findings

On shared C raw22,523-pair-history extraction, own strict-prior scorer uses exact account
strings, samecurrency, prior timestamp strictly less, latest timestamp/maxsource tie.
ROMANCE_SCAM has1973 eligible rows; latest lag q10/median/q90=32.2/215/709.8seconds.
Early(n1349) log amount-ratio mean.401378,SD.408834; July(n624) mean.403295,SD.410220.
Early lag mean313.55/median217s; July292.69/median212s. These calculations preceded
the lead's C recurrence exchange. Candidate recurrence Exp(mean≈300sec), multiplier
LogNormal(logmean≈.4,logSD≈.4). Only5 exact1.5 ratios: do not call deterministic×1.5.

Overall83.07% increase vs49.53% selected blankcontrols; controls' median lag14410.5s.
CC/CB strata still differ sharply from sameparty selectedcontrols, but their sample
sizes/history composition differ. 503 romance labels lack observed samepair/currency
history. Conditional rapid escalation supports a reconstructed injected-sequence rule
for recoverable histories, not evidence of realcustomer intent.

Artifacts: `recurrence_review.py`, `recurrence_initial.log`, `recurrence_latest_rows.csv`,
`recurrence_latest_summary.csv`, `recurrence_latest_strata.csv`, `romance_generator_fit.csv`.
