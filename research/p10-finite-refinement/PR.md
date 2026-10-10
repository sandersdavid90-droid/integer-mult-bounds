Audit PR317 and tighten its finite transfer (tiny gain; unchanged circuit)

PR317's composed p=10 construction uses three finite ordinary levels and
conservative outer parameters. This additive package reproduces its entire
immutable source-bound verifier, independently recounts its actual paid
profile, and supplies a small finite arithmetic refinement:

`kappa = 768170078151184046974713 / 10^27`
`      = 0.000768170078151184046974713`.

The absolute gain over pinned PR317 is only about `3.33594e-13`
(`4.34271e-8 percent` relative). No new circuit mechanism, practical speedup,
or strongest-current-result claim is made.

The contribution is a separate rational moment implementation with a
10^-27 root bracket, agreement with both unchanged source engines, eight
explicit positive-gap finite levels, all 47 strict assembly checks,
adjacent-point rejection, and an upper bound on remaining arithmetic
headroom for this exact profile and assembly. The complete bad-class
fallback and all physical charges remain present.

Default verification runs the full PR317 package and its PR315 dependency
fresh. Optional authenticated replay reuse is explicitly labeled. The
source is pinned at `0a0b61a7f4601a96036af8bb6a6338c58f035d2e`. The finite
refinement leaves its pinned dependency package and main's selected result
unchanged.

A separate CI repair incorporates Rohan Arun's PR318 at
`a45747d2559141a594916475f52642e4fab86e02`: three legacy joint-dual metadata
files refresh the root Makefile/README hashes and their certificate bindings.
It fixes the inherited `AssertionError: Makefile` without changing verifier
checks or mathematics. A dedicated workflow now runs this refinement and
the full pinned PR317 replay on Python 3.11 and 3.13.

Validation and its limitations are recorded in `VALIDATION.md`.
The source's all-size interfaces remain conditional; this is not a new
Lean multiplication proof. Counted-coefficient cutoffs do not instantiate
unknown full inherited constants.

Credits: eumemic's PR317; DreamingOfClouds's PR315; the finite-level and
balanced-assembly lineage, including Rohan Arun, icekylinx, Zhihao Chen and
the RaD project; all circuit and checker contributors retained in NOTICE.md.
Prepared for David (`sandersdavid90-droid`) with substantial OpenAI Codex
assistance, under Apache-2.0.
