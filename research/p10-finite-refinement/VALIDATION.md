# Validation record — 2026-10-10

Environment: Python 3.12.14, SymPy 1.14.0, g++ 13.3.0, Boost 1.83 headers.
The repository base is `12a4934d15006e8c10f9b2264f13f8f341be802b`.

## Passed

- The complete immutable PR317 verifier ran locally from the exact pinned
  source. All 21 driver stages completed in 263.3 seconds, including all
  nine fresh PR315 stages and their omission controls. Package input
  hashes were unchanged before and after execution.
- The final word's scalar/dirty restoration, both reflected ledgers,
  exact changed charts, actual bank assignments, prime guards, full
  finite invoice and original assembly passed. The original result was
  reproduced exactly before refining it.
- The new default wrapper completed that full replay and the refinement.
  A final arithmetic rerun used the same authenticated replay after
  explicit recurrence-slack reporting was added. The committed certificate
  therefore honestly says `authenticated prior replay`; it does not call
  that last arithmetic-only rerun another fresh physical execution.
- The independently written rational moment implementation and both
  unchanged inherited implementations agree: the refined bit root is
  admitted and the adjacent 10^-27 point is rejected. The independent
  implementation also admits the unchanged complex saving.
- All eight finite levels have strictly positive exact gaps and checked
  sufficient cutoff inequalities. The refined recurrence slack is
  recomputed, not inherited from the lower predecessor saving.
- All 47 outer constraints and seven margins pass. Controls reject the
  next headline point, a zero ordinary gap, a zero outer reservation and
  reuse of the predecessor's three-level leaf for the new headline.
- `make gen4-bank-verify` passed on the repository base, including the
  selected-record check and all nine unchanged gen4 stages.

## Boundaries

The independent implementation covers the moment, finite-level arithmetic
and fixed-profile headroom bound. Physical and geometric admission runs
the attributed upstream checkers. There was no independent human review,
new Lean build, or practical multiplication benchmark.

Two initial environment attempts did not complete: first SymPy was absent,
then Boost headers were absent. After installing SymPy and unpacking Boost
headers locally, the successful full run above started in a new output
directory. Failed attempts are not counted as verification passes.

The broad inherited `make verify` suite is separate from the successful
source replay and selected-result target. Its final status is recorded
below; no incomplete run is represented as a pass.

`timeout 600 make verify` exited 124 at the ten-minute limit while running
the inherited paired-cube producer. It had not reached the complete suite's
end, and is **not a full-suite pass**. No tracked predecessor file changed.
The successful complete PR317 replay and `make gen4-bank-verify` above are
separate runs with their own completed results.
