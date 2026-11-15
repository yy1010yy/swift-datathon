# B endpoint-mismatch review

Input: original independently parsed B full10M joint_counts.csv, preserving both
endpointbooleanflags, route, continuity and preJuly/Julyperiod. Endpoint_model.py
fits only earlierrows: senderp=.0497998724,receiverp=.0499752067. Frozen independent
Bernoulliproduct predicts July's fourendpointcells with weightedconditionalTV.00038253
across route/continuitystrata. Earlier/July route×continuity marginal ranges are
sender.04828–.05197 andreceiver.04770–.05063; smallestgroupsareespeciallynoisy.

The lead's overall5%marginals andboth24693versusindependenceexpected24883.3 agree
with a near-independent smallperturbation mechanism. A same-singlechangeeventthat
alwaysaltersbothendpoints is contradicted by abundant sender-only/receiver-onlycases.
Strongestalternative: systematic bank/routeconstruction coincidences could produce
approximatelythe sameflags without literal independentediting. Even a literal5%
redraw may choose the originalbank, yielding observedmismatchslightlybelow5%.

Finalwording: eachendpoint disagrees with its separatelylistedbank in approximately5%
of rows, with jointfrequencies and period/route/continuity checks compatible with
largelyindependent perturbations. **The data do not identify whichfield was changed,
whether a routeorbankfieldis authoritative, or whether these records are corrupt.**
No causal editingdirection or exact5%sourceprobability is proved.

Methodlimit: B's originaljointtable has only early/lateperiods, not month. Earlier
contains thesparsepartialAprilboundary; no monthlyrange or April-excluded claimis
madefromthisfile. Use A/lead monthlyrawcensus for the separate May–Julycheck. Both
endpointflags are measurable disagreements, not rows to delete. Countoverlap rather
than summing sender+receivercountstoestimate affectedpayments.

Evidence:endpoint_model.py,endpoint_model_strata.csv,endpoint_model.json and actual
endpoint_model_run.log; original source analysis/reviews/b/joint_counts.csv.
