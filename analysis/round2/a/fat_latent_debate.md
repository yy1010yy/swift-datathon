# A latent fat-finger debate and same-input consistency

A and C independently fit early blank-label currency+business-role baseline means
from separate full scans. The same1940 FAT records have adjusted residuals matching
to max1.25×10−13. Early1351 mean3.553931; July589 mean3.724928. Their broad spread
near5.1 natural-log units is much larger than blank baseline residual spread≈2.15.
No unseen currency was excluded. Lead's baseline agreement and A's independent
`fat_latent_verify.py` confirm matching populations and row-level arithmetic.

Apparent likelihood differences are explained by assumptions: A uses currency-specific
baseline spreads, C one pooled spread. For example A July unchanged NLL5.97710
versus C5.96262, decimal mixtures≈2.9591 versus≈2.9587. To distinguish methodology
from a calculation error, A recomputed every C model's early/July likelihood on C's
same residual vector and fixed sigma; maximum discrepancy8.9×10−16. See
`fat_latent_common_input_verification.csv` and actual verification log. This comparison
uses shared post-exchange inputs, explicitly not a new independent fit.

Strongest competing explanation: FAT amounts may simply come from a larger and wider
distribution, without discrete decimal errors. The free mean/extra-variance alternative
scores3.04286 July in A, versus fitted decimal mixture2.95913 (gain≈.08373nats/row).
C independently obtains3.04278 vs2.95871. This improvement supports decimal-shift
families but does not uniquely identify them: alternative continuous mixtures, heaping
and selection could yield similar densities. The dramatic gain over unchanged baseline
is strong; the gain over broad selection is smaller and must be communicated separately.

Negative-control check: deterministic blank sample July2960 rows favors unchanged
baseline NLL2.17194 over FAT decimal mixture3.35356. This shows the FAT model is
not a universal amount distribution. Sampling is every997th blank record, not a claim
of population matching; other label comparisons retain all their observed records.

Mixture weights change with allowed powers and convergence limits; adjacent components
overlap substantially at baseline logSD≈2.15. Do not publish fitted weights as generator
probabilities, nor infer a row's actual intended amount. A post-inspection equal-weight
example at powers{−2,1,2,3,4} predictsJuly well too (NLL2.95551), illustrating weak
identifiability of detailed weights rather than proving that exact factor set.

Final wording: **After adjusting for currency and customer types, fat-finger-labelled
amounts are shifted upward and much more dispersed than payments with no recorded
label. A model that multiplies a latent baseline amount by powers of ten predicts
the later-period distribution better than an unchanged baseline or one broad shifted
normal distribution. The exact error factors, their probabilities and original intended
amounts remain unresolved.**

The prior visible-history negative result remains valid: only3/313 history-eligible
FAT labels have an approximate power-of-ten earlier samepair/currency amount match,
zero exact matches. A latent newly generated intended amount need never appear as
a preceding payment, so distributional evidence and the history test answer different
questions. Neither should be removed to make the narrative look simpler.
