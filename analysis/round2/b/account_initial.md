# B independent account/detail construction initial

Full10Mraw records tested independently before seeing lead account/detail results.
Both account fields begin `_FAKE_` on all10Mrows per side. Let identifier be the exact
account text after that prefix, preserving spaces, punctuation and leading slashes.
Do not normalize this identifier.

| Exact test | Ordering side | Beneficiary side |
|---|---:|---:|
| First detail line = one slash + identifier |8643632|8531258|
| Strip all leading slashes from first line, then equals identifier |9308991|9274369|
| First line = one-or-more slashes + exact identifier |9436890|9390618|
| Identifier occurs anywhere in detail text |9436890|9390618|
| Detail contains an actual linefeed |9764612|9750969|
| Detail contains literal backslash+n |0|0|

Thus the exact account-derived identifier is exposed in the first detail line on
approximately94%of payments, with slash-format variations. The universal rule that
every detail contains its account is false:563110ordering/609382beneficiaryrows
do not contain that exact identifier anywhere. Preview counterexamples include
source47,59,62,91 with ordering details consisting only of a bank-likeBIC, andsource9
with name/address but noaccount. These examples demonstrate exceptions, not their
population breakdown. Stripping all slashes can erase a meaningful leading slash
inside the identifier, explaining why that shortcut matches fewer rows than the
one-or-more-prefix formulation.

## Exact identity consistency on a selected account subset

Choose accounts deterministically when SHA256(rawaccount UTF8)'s firstbyte<3 (3/256
selection); retain **all** their occurrences and compare exact raw details/BIC/type.
This covers34884unique(side,rawaccount)keys and114253ordering/113951beneficiaryrows.
Different exact details occur on8500selectedside/accountkeys; differentbankBICs on731;
differentB/Ctypes on0. These are sample-only counts, not a census of all accountkeys.
They refute universal rawaccount→oneimmutabletext andrawaccount→onebankfunctions
within observedselectedcases, while no role inconsistency was found in this subset.
Do not infer global humanidentity, account-bank uniqueness or unchanged details from
the fakeaccountstring alone. Source-record conflict examples are saved for inspection.

Code:account_details.py. Actual fullscan354.94seconds; jointmonth/type/formatcounts
account_detail_joint.csv, sampleconflict examples and account_details_initial.json.
No rawidentity formatting or historical inputs were modified. No claim that missing
account text or differing bank fields automatically represents bad data or fraud.
