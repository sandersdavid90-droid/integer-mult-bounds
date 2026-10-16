# A paid boundary for multiplication as exponent addition

**Outcome: scoped conversion results and a complete exact reference codec;
no new kappa.** The user-assigned first target is kappa = 1/100, meaning
`O(n (log n)^0.99)` for a complete binary-input/binary-output algorithm on the
repository's fixed finite-tape model. Targets 1/10 and 1/2 remain stretch goals.
This replaces another refinement of the selected finite circuit.

The signed-power-of-five representation is classical. This package adds a
specific conversion decision: an exponent-sum-only reader needs almost the
full product precision, even a reader augmented with the ordinary input sum
and almost all low input bits has explicit collisions, and independent binary
block tables have the sharp precision threshold proved below. These are
written scoped proofs supported by exact executable evidence, not an
algorithmic lower bound for general number representations. No literature
priority or independent author review is claimed.

## The complete boundary and proposed saving

Inputs are arbitrary integers `0 <= x,y < 2^n`, including leading-zero padded
inputs. Output is the ordinary exact `2n`-bit product. Zero is handled directly.
For a nonzero input write `x = 2^v u`, with `u` odd. At precision `N >= 3`,
encode an odd residue as

\[
 u\equiv(-1)^\epsilon5^e\pmod {2^N},\qquad
 \epsilon\in\{0,1\},\quad 0\le e<2^{N-2}.
\]

Multiplication of units then consists of sign XOR and exponent addition modulo
`2^(N-2)`. The work one hopes to remove is the nonlinear multiplication core.
Both binary-to-code conversions, code-to-binary decoding, constant preparation,
movement and final output still have to be paid. Unknown costs are not zero.

Existence and uniqueness follow from

\[
 v_2(5^{2^j}-1)=j+2.
\]

The formula follows by induction by squaring, beginning with `5 = 1+4`.
For an odd multiplier `r`, the quotient
`(z^r-1)/(z-1)` is odd when `z` is odd; consequently
`v_2(5^e-1)=2+v_2(e)` for every nonzero positive `e`.
Thus 5 has order `2^(N-2)` modulo `2^N` and its powers are exactly the residues
congruent to 1 modulo 4. Negation supplies the other odd residues.

`codec.py` constructs the exponent one bit at a time by cancelling inverse
powers of 5. Decoding uses ordinary modular exponentiation. For a full product
it uses `N = max(3, 2n-v_x-v_y)` and restores the power of two. Since the odd
product is less than `2^(2n-v_x-v_y)`, there is no wraparound at that precision.
This is a complete correctness implementation, with no fast-conversion claim.

For example, modulo 256, `7 = -5^10` and `11 = -5^21`; adding exponents and
decoding gives `5^31 = 77`. At only four output bits the result is 13.

## Near-full precision is necessary for the compressed reader

The reader in this section receives only `n` and the combined pair
`(epsilon_x XOR epsilon_y, (e_x+e_y) mod 2^(N-2))`. In particular, it does not
retain the two full encodings or the original input pair. Its summary is in
bijection with the odd product modulo `2^N`.

**Proposition 1.** For every even `n >= 4`, the precision `N=2n-2` is
insufficient for this reader. For odd `n >= 5`, `N=2n-4` is insufficient.
In either case, exact reading needs product precision within a constant of
`2n`; halving the precision is not a valid conversion saving in this model.

**Proof.** Set `m=2 floor(n/2)`, `b=2^((m-2)/2)` and

\[
 A=2b^2-2b+1,\quad B=2b^2+2b+1.
\]

Both positive odd factors fit in `m <= n` bits, and the classical factorization

\[
 AB=(2b^2+1)^2-(2b)^2=1+4b^4=1+2^{2m-2}
\]

makes `(A,B)` and `(1,1)` indistinguishable at precision `N=2m-2`, although
their products differ. Any smaller precision also collides. One additional
bit distinguishes these particular products; this does not prove that it
distinguishes every pair of possible products. Full precision `2n` is sufficient.
For even `n`, the exponent field must therefore have at least `2n-3` bits;
for odd `n`, at least `2n-5`. These are necessary bounds, not exact optima. QED.

The smallest fixture is `5*13=65` versus `1*1=1`, both encoded as `(0,0)`
modulo 64. The argument uses a classical Sophie Germain factorization; no
novelty for that identity is claimed.

## An ordinary sum and separate low bits do not repair the reader

**Proposition 2.** For every `n >= 4`, even giving the reader `x+y` and the
individual residues `x mod 2^(n-2)`, `y mod 2^(n-2)` leaves a collision at
product precision `N=2n-3`.

**Proof.** Put `c=2^(n-1)+1`, `u=2^(n-3)` and compare the ordered pairs

\[
 (c-u,c+u),\qquad(c-3u,c+3u).
\]

All four factors are positive odd integers less than `2^n`. Corresponding
inputs differ by `2u=2^(n-2)`, so their stated low bits and individual signs
agree. Both sums equal `2c`, whereas the products differ by

\[
 (c^2-u^2)-(c^2-9u^2)=8u^2=2^{2n-3}.
\]

Their combined exponent summaries therefore agree at precision `2n-3`.
Any deterministic reader with exactly this information returns the same answer
on both pairs and must fail on one. QED.

At `n=5`, `(13,21)` and `(5,29)` both have sum 34, both inputs have low three
bits equal to 5, and both combined codes are `(0,28)` modulo 128. Their exact
products are 273 and 145. This is an information collision under the named
reader contract, independent of how its code is implemented.

## One bounded pivot: independent tables on binary blocks

Write a principal unit as `a + 2^k b`, with `k >= 3`, `a < 2^k`, `a=1 mod 4`
and `0 <= b < 2^(N-k)`. Let `E_N` denote its canonical exponent modulo
`2^(N-2)`. Could small separate tables supply

\[
 E_N(a+2^k b)=F(a)+G(b)\pmod {2^{N-2}}?
\]

**Proposition 3 (sharp threshold).** For `k < N <= k+2`, such tables exist:
take `F(a)=E_N(a)` and `G(b)=E_N(1+2^k b)`. For every `N >= k+3`, no such
separate tables exist, even on the four inputs `a in {1,5}`, `b in {0,1}`.

**Proof, positive direction.** The ratio

\[
 \frac{a+2^k b}{a(1+2^k b)}-1
 =\frac{2^k b(1-a)}{a(1+2^k b)}
\]

is divisible by `2^(k+2)` because `a=1 mod 4`. Thus the proposed multiplicative
factorization, and hence the additive encoding, holds at these precisions.

**Proof, failure at higher precision.** Any separate additive tables must have
zero mixed difference. For the four stated inputs that difference is

\[
 D=E_N(1)+E_N(5+2^k)-E_N(1+2^k)-E_N(5).
\]

The corresponding unit ratio satisfies

\[
 5^D-1\equiv
 \frac{5+2^k}{5(1+2^k)}-1
 =\frac{-2^{k+2}}{5(1+2^k)}\pmod {2^N}.
\]

Its valuation is exactly `k+2` when `N >= k+3`. By the order/valuation formula
above, the canonical representative of `D` has valuation exactly `k` and is
nonzero. At the first failing precision `N=k+3`, it is exactly `2^k` modulo
`2^(k+1)`. This contradicts separability. QED.

An actual failure occurs at `k=3,N=6`: separately encoding low block 5 and
high block 1 gives `E_6(5)+E_6(9)=1+6=7`, which decodes to 45 rather than 13.
The correct exponent of 13 is 15.

The changed-premise positive control `dependent_block_encode` implements

\[
 E_N(a+2^k b)=E_N(a)+E_N(1+2^k b a^{-1}).
\]

It correctly returns 13 in that example and passes the broader checks. It
requires a low-dependent inverse and modular arithmetic; those operations
are paid. This theorem excludes independent additive block tables for the
canonical exponent, not overlapping tables, dependent/shared corrections,
different encodings, or a fused consumer that avoids forming these words.

## Complete cost decision

For odd inputs, let `C_E(n,N)` include all work needed to convert an arbitrary
`n`-bit input to precision `N`, and let `C_D(N)` include full binary decoding.
The proposed unfused algorithm needs

\[
 2C_E(n,2n)+C_D(2n)+P(2n)+O(n),
\]

where `P` is any constant preparation not already included in the conversions.
A shared preparation is charged once. Each term must be implemented in the
fixed finite-tape model; random access and enormous precomputed advice are not
free. A fused replacement must give its actual complete recurrence instead.

| Obligation | Evidence / status |
|---|---|
| Exact group law and full unsigned product | Proved above; complete reference implementation and finite replay |
| Valuation/sign handling, exponent addition, shifts and ordinary output | Constructively linear bit work by scans; Python timing is not evidence of the full tape bound |
| Sufficient uniform precision | `2n` suffices; Propositions 1–2 prevent the stated truncated readers from making it much smaller |
| Reference conversion and decoding | Uses linearly many ordinary modular arithmetic steps; no fast conversion bound follows |
| Independent additive block conversion | Sharp threshold in Proposition 3; full product precision crosses it |
| Low-dependent corrected conversion | Exact construction supplied; favorable complete cost unknown |
| Full explicit conversion lookup | Works, but already has `2^(n-2)` keys for principal-unit inputs and product-size exponent entries; its preparation/storage is exponential |
| General shared/fused conversion | Unknown; not rejected by the preceding scoped statements |
| Complete `O(n (log n)^0.99)` algorithm | Not supplied; no new kappa claim |

For orientation, ordinary repeated-squaring implementations of this reference
codec give only an `O(N M(N))` arithmetic upper bound, where `M(N)` is an
already available multiplication cost. That unfavorable upper bound is not
a lower bound on all converters. For a principal unit the classical relation is
`E_N(u) = (log(u)/4) * (log(5)/4)^(-1) mod 2^(N-2)`. The second factor is a
unit depending only on precision; preparing it and multiplying by it are paid.
Known faster p-adic log/exp algorithms are relevant predecessors, but a
soft-linear bound hiding logarithmic factors does not certify the specific
sub-logarithmic factor sought here.

**Decision:** stop reduced-precision exponent-sum reading and independent
additive block tables for this contract. Preserve the correct codec and exact
controls. Do not scale either failed construction. Full-precision dependent
or genuinely fused conversion remains open, as does the 0.01 target.

## Reproduce and evidence limits

From the repository root, with CPython 3.12 and the standard library:

```sh
python3.12 scripts/research_package.py --package research/two-adic-conversion-boundary
```

Direct replay also works in a Git-free copy of `codec.py`, `verify.py` and
`RESULT.json`:

```sh
python3 -I -O -B research/two-adic-conversion-boundary/verify.py
python3 -I -B research/two-adic-conversion-boundary/test_verify.py
```

`RESULT.json` records 1,020 unit round trips, all 21,844 input pairs at lengths
1 through 7 (including zero/even inputs), 250 exact collision fixtures at
lengths 4 through 128 with one-more-bit repair controls, and 60 nonzero mixed
differences plus 30 low-precision positive controls. Six test groups add an
exhaustive power-enumeration oracle, larger products, independent polynomial
and residue checks, the full positive block-table domain at small cuts,
low-dependent repairs, semantic faults, and optimized Git-free replay with
receipt-corruption and overwrite controls. Current source is compiled directly
to avoid accepting a stale bytecode cache.

These tests support the written proofs; finite tests alone are not universal
proofs. No hosted CI, proof-assistant formalization, independent author review,
practical multiplication benchmark, selected supplier cold replay or complete
new multiplication-time theorem is claimed. Existing selected evidence is
historical provenance, not an input to these elementary proofs.

## Open next questions

Can a low-dependent correction be consumed jointly with output decoding without
materializing and paying for both complete exponent words? The exact missing
coupling is `b a^{-1}` at the relevant retained precision, not an unspecified
carry. A useful first step is a construction for that coupled correction and
readout with explicit operand sizes, shared-state ownership, constant preparation
and a complete recurrence. It must pass the `13 versus 45` block fixture and the
two product-collision families, and its optimistic *complete* cost must fit
`O(n (log n)^0.99)` before implementation expansion. No such construction is
presently known from this session. Simply increasing test sizes, tabulating all
input words, or renaming the classical logarithm is not a next research task.
The same question is structured in `TASK.json`.

## Sources, overlap and credit

- The group of units modulo powers of two, inverse-power bit lifting and the
  Sophie Germain factorization are classical. The proofs needed here are
  included; this is not a discovery claim for multiplication-as-addition.
- Xavier Caruso, Marc Mezzarobba, Nobuki Takayama and Tristan Vaccon,
  [*Fast evaluation of some p-adic transcendental functions*, arXiv:2106.09315](https://arxiv.org/abs/2106.09315),
  especially sections 3.1–3.2, supply the existing fast-conversion context.
  Their algorithms are not executed or imported; a soft-O statement is not
  interpreted as the required exponent saving or a fixed-tape implementation.
- Main `534de584c7c9b7abd621a0d8cec959d021e5b510`, priority revision 5;
  selected conditional kappa `0.001672660197076918`. Exact Git provenance is in
  `SOURCES.json`. No selected or upstream manuscript files are modified.
- Live targeted GitHub PR searches for discrete logarithm, logarithmic
  representation and Sophie returned no match. The earlier 2-adic results
  concern decoder valuations. Current board and hub posts were read. The
  local overlap helper covered only eight sparse records and had no usable
  remote snapshot; this is not a full survey or a novelty certificate.
- Prepared for David (`sandersdavid90-droid`) with substantial OpenAI Codex
  assistance in derivation, implementation, checking and writing. Separately
  coded test oracles are not independent author review. Apache-2.0.
