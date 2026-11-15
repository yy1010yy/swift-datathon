# C debate response — after independent A/B initials

Read A and B initial conclusions only after C's first two full scans and initial
record were saved. C's history summaries were communicated to the lead before A/B
reimplemented scoring. Cross-review of exact tables is the lead's deciding check.

## V2: approximate multiplicative party effect

A/B's strongest evidence is the within-currency log-mean shift of approximately two
natural-log units per business endpoint, rather than only pooled medians. C independently
finds the same currency-controlled direction. With at least 1,000 observations in
each comparison cell, BB/BC median ratios across currencies are 7.368 before July
(74 currencies) and 7.603 in July (48 currencies). CB/CC ratios are 7.140 (42) and
7.184 (20). Those are median *amount ratios*, not means of log shifts; different
summary definitions must not be confused.

Currency mix cannot fully explain this conditional result, but exact multipliers are
not recovered. Within-currency comparisons vary considerably, especially changing
sender type. C's BB/CB ratios range 3.95–12.45 in pre-July cells. Different bank/corridor
populations or currency distributions may alter the effects. A universal exact factor
7.39 should be rejected; a shared approximate role-dependent sampling scale remains
a useful candidate, with wide overlapping distributions.

Important wording: all amounts are measured in USD. C's median 40,194 for BB is
specifically payment-currency USD, whereas A/B's 22,880 pools payment currencies.
These are different populations and consistent results, not a numeric discrepancy.
Rounding and changing populations can alter medians, so exact distribution normality
or a unique causal direction is unproved. Deciding checks: exact cross-review
currency/party/period moments and quantiles, then matched bank-pair comparisons.

## V3: strong USD whole-dollar concentration

B's strongest alternative is a rounding process before USD normalization. C independently
reproduces all USD/EUR whole-dollar counts from its full raw-data scan. Party-type mix
does not explain the difference: all eight USD party/period cells have whole-dollar
shares 38.26–38.81%, versus 0.91–1.00% for EUR. These exact controlled counts are
`rounding_controlled.csv`. No original local-currency amounts or conversion rate field
is available, so prior-to-conversion rounding is plausible but not uniquely identified.
Currency-specific templates or different amount mixtures remain alternatives.

## A2: label sender restrictions

All three reviewers independently get identical full-file compositions: CEO sender
B in 945/945; romance sender C in 2,476/2,476; romance receiver B in 665. Exact
composition is supported. A literal both-consumer romance restriction fails. Nothing
here proves how the fraud was injected or that the text accurately describes intent.

## A3: past-payment replay and decimal-shift tests

C's strict-past replay results await A/B's independent scoring of the shared full-file
history extract. Repeated amount by itself is insufficient, because legitimate payments
also repeat. The deciding contrast is the fraction and lag for DUPLICATE_PAYMENT
versus unlabelled controls with observed history and comparable history depth. C finds
493/515 history-eligible duplicates match an earlier amount versus 209/14,788 controls;
duplicate lags are much shorter (median 1,100s versus 32,794s). These are selected-pair
controls, not a randomized experiment. Shared extraction remains a common dependence;
independent raw extraction is preferable before calling a generator program proven.

FAT_FINGER same-pair power-of-ten matching is uncommon and lower than control rates;
that is a useful negative result, not proof of absence of a decimal-error injection.
Most labelled rows lack same-pair history, and errors may refer to unobserved intended
amounts. Replacement needs a same-sender/different-beneficiary test, now being run.
Recall's name alone does not explain its mechanism.
