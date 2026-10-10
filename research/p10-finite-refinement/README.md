# PR317: eight finite levels and an independent moment check

On the unchanged PR317 circuit, the conditional exponent saving is

    kappa = 768170078151184046974713 / 10^27
          = 0.000768170078151184046974713.

The pinned predecessor is eumemic's PR317 at
`0a0b61a7f4601a96036af8bb6a6338c58f035d2e`, with
`kappa = 0.000768170077817590`.
The absolute gain is approximately **3.33594e-13**, or **4.34271e-8 percent**
of the predecessor's saving. This is a tiny finite-parameter refinement,
not a new circuit mechanism or a practical speed improvement. No claim of
the strongest current public result is made.

The useful additional evidence is an independently implemented exact
moment check, explicit cutoffs for all eight finite levels, and a rigorous
bound on how little room remains in arithmetic tuning of this fixed
profile and assembly. Larger improvements must change something outside
that restricted family.
The certified remaining headroom is less than **3.893e-27** in kappa.

## What changes

- Recount the normalized paid profile from PR317's actual emitted binary.
- Bracket its fallback-inclusive bit root on the 10^-27 grid with a new
  rational checker; cross-check both endpoints in both inherited engines.
- Extend the finite ordinary chain from three to eight levels.
- Tighten eta from 10^-12 to 10^-24; retain beta=10^-9.
- Recheck all 47 strict assembly inequalities and reject the next headline
  grid point. Keep the complete 10^-16 bad-class fallback.

The word, scalar coefficients, frames, bank allocation, complex supplier,
physical invoice and prime assumptions are unchanged. The new verifier's
default mode executes the full immutable PR317 verifier, including PR315,
before accepting the refinement. See [PROOF.md](PROOF.md) for the finite
cutoffs and the restricted upper bound, and [NOTICE.md](NOTICE.md) for credits.

## Reproduce

Python 3.11+, SymPy 1.14.0, a C++17 compiler and Boost headers are required.
Fetch the exact source from the repository root:

```sh
git fetch https://github.com/eumemic/integer-mult-bounds.git 0a0b61a7f4601a96036af8bb6a6338c58f035d2e
git worktree add --detach ../pr317 0a0b61a7f4601a96036af8bb6a6338c58f035d2e
python3 -m pip install sympy==1.14.0
python3 -B research/p10-finite-refinement/verify.py \
  --source-root ../pr317 --output /tmp/p10-finite-refinement
```

The output directory must be fresh. If Boost is installed outside the
compiler's standard paths, add `--boost-include /path/to/include`.
Verification runs offline after dependencies are installed. It authenticates
every source file before and after execution. `--reuse-replay PATH` is an
explicit optional mode for a previously completed full PR317 replay; its
certificate is labeled as reused execution.

The output contains `certificate.json` and, by default, the entire fresh
source replay. The committed certificate is an example result, never a
substitute for execution. Source execution timings make its provenance
hash run-specific; the exact arithmetic fields are deterministic.

## Limits

This is conditional on the source's all-size compiler, common weighted
charts, restored rows, routing, prime supply, complex lifting,
precision/recovery and analytic transfer. Physical admission uses the
upstream verifier; the new independent implementation checks arithmetic.
There is no new Lean proof or multiplication benchmark. Displayed cutoffs
use the counted primitive coefficient; full inherited constants must be
inserted using the explicit rule in the proof.
