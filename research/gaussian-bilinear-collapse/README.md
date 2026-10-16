# A coupled Gaussian multiplication attempt toward kappa = 1/2

**The target was not reached.** A proposed cancellation of two Gaussian maps
with their nonlinear product is exactly correct algebraically. Its explicit
representation needs too much precision. One bounded repair, local recentering,
becomes ordinary interpolation with an unfavorable recursive volume bill.

This is a completed, scoped research attempt. It establishes a precise stop
for these two realizations, **not a barrier to kappa = 1/2**, Gaussian methods
in general, or integer multiplication. The completion-of-squares identity and
polynomial interpolation/rank facts below are classical. The contribution is
the explicit coupled candidate, its exact gauge/data-range calculation,
complete small executions, and the decision about whether to build it further.
There is no new supplier or kappa claim.

## Assignment and optimistic budget

The donor explicitly requested a high-risk session aimed at kappa = 1/2,
overriding weighted task allocation. Starting main is
`e24ccc79caa1943fb126c61b45032fefddf2d3f2`, priority revision 5. The selected
conditional result remains 0.001672660197076918.

The starting observation is that a historical balanced outer formula has a
Gaussian cap below 1/4; stronger inner circuits alone cannot make that formula
reach 1/2. This is already proved by the retained
[domain audit](../../docs/research/assembly-domain-audit.md) and
[BigCactusLabs/PR701](../balanced-gaussian-envelope/README.md), not new here.
DaysSky's PR657 supplies a separate historical pass-count wall. Later pending
outer changes, including Vlado Vojdanovski's
[PR1673](https://github.com/CrocSwap/integer-mult-bounds/pull/1673), have different
ledgers; no historical wall is silently transferred to them.

Our changed hypothesis is to combine two forward maps, the pointwise product,
and a **different** inverse instead of preserving the separate linear-map
contracts. A radius-R local Gaussian pass would use O(NR) scalar contacts on
an N-coordinate axis. R=O(sqrt(P)) looked potentially relevant to the desired
square-root-log work when the parent precision is P=Theta(log(input bits)).
For the first rejection screen we grant the inverse, routing, coefficient
preparation, initialization and restoration for free. A passing screen would
therefore be insufficient; a failing precision bill rejects the stated
realization before any large construction effort.

## 1. Exact product collapse

Fix a real rational 0<q<1 and vectors x,y of length N. Put n=N-1 and

```
F(x)[k] = sum_i x[i] q^((k-2i)^2),              0 <= k <= 2n,
W[s]    = sum_(i+j=s) x[i] y[j] q^(2(i-j)^2),
G[k,s]  = q^(2(k-s)^2),                       0 <= k,s <= 2n.
```

Then **F(x) pointwise-multiplied by F(y) = G W**, because

```
(k-2i)^2 + (k-2j)^2 = 2(k-i-j)^2 + 2(i-j)^2.
```

The Gaussian square matrix G is invertible: factor out q^(2k^2) from row k
and q^(2s^2) from column s. The remaining matrix is Vandermonde on the distinct
nodes q^(-4k). Thus the changed inverse exists exactly. Doubling the input
centers retains odd as well as even output sums; no half-grid outputs vanish.

This is a real algebraic collapse of the three-stage expression. Its immediate
output W is a **weighted** convolution. The weights cannot be dropped merely
because the maps are invertible.

## 2. All separable correcting gauges and their optimal range

Suppose nonzero complex input gauges r_i,s_j and an output gauge t_k correct
all coefficients independently:

```
r_i s_j t_(i+j) q^(2(i-j)^2) = 1     for all 0 <= i,j < N.
```

Every solution, with arbitrary nonzero complex R,S,z, is exactly

```
r_i = R z^(-i) q^(-4i^2),
s_j = S z^(-j) q^(-4j^2),
t_k = (RS)^(-1) z^k q^(2k^2).
```

To prove completeness, divide the equations at (i+1,j+1) and (i,j) by those
at (i+1,j) and (i,j+1). This forces
`t_(k+2) t_k / t_(k+1)^2 = q^4` for every k=0,...,2n-2.
The resulting second-order multiplicative recurrence determines t; using
j=0 and i=0 determines r and s. Substitution proves sufficiency. Complex
phases do not change the following magnitude bounds.

Write delta=log2(1/q)>0. For any array a, let its logarithmic magnitude range
be max(log2|a|)-min(log2|a|). Then

**the minimum, over all correcting gauges, of the largest of the three ranges
is exactly `2 delta n^2`.**

Indeed `t_0 t_(2n) / t_n^2 = q^(4n^2)`. The log magnitude at n differs from
the average endpoint log magnitude by 2 delta n^2, forcing that much range
in t. Choose R=S=1 and z=q^(-4n): t has precisely that range, while r and s
each have range `4 delta floor(n^2/4) <= delta n^2`. This attains the bound.
No finite search is needed for this all-gauge statement.

The replay's centered gauges are that optimal choice. Exact Gaussian
interpolation, followed by t, recovers every ordinary product coefficient.

### The range occurs in data, not just a coefficient table

Feed the corrected pipeline x_i=y_i=1. The ordinary product coefficients are
c_k=min(k+1,2n+1-k,N), so its materialized middle array is w_k=c_k/t_k.
Consequently

```
|w_n| / sqrt(|w_0 w_(2n)|) = N q^(2n^2).
```

Its logarithmic range is therefore at least
`max(0, 2 delta n^2 - log2 N)`, for **every** correcting gauge.
This survives an input-dependent common scale for the whole array. A binary
format materializing all these data values on one grid needs at least this
much total integer/fractional range, even granting the inverse exact and free.
This is not a lower bound for independently scaled records, a fused inverse
that never materializes this boundary, symbolic cancellation, or other maps.

For q=1/2, N=8 and the centered gauges, the exact middle array has maximum 1
and minimum 2^-95. Rounding that array to 32 fractional bits changes a required
coefficient **8 into 0**. Separately, for N=4, x=e_0,y=e_3, even the exact
forward-map product has maximum 2^-18; eight-bit rounding makes every measured
product zero and loses the answer's coefficient 1. Increasing precision
repairs the finite executions, confirming the failure is the stated format.

### Precision versus locality

For a Gaussian pass retaining the uniform unit-bounded-input contract, omitting
a contact at distance R with absolute error at most 2^-P requires, even for
a single unit term, `delta R^2 >= P`.
If a common middle format has at most C P bits, its necessary range condition is

```
2 delta n^2 <= C P + log2 N.
```

Together these imply

```
R^2 >= 2 n^2 P / (C P + log2 N).
```

When log2 N=O(P), this forces R=Omega(N). The contemplated
R=O(sqrt(P)) is excluded for superpolynomial-in-P axes in this explicit staged
representation. Taking q closer to one moves the cost into the interaction
radius. This does not establish a theorem about the actual source resamplers,
whose separate approximation and conditioning contracts are different.

## 3. One bounded repair: recenter on small blocks

Partition each input into length-L blocks. Compute its local F on
M=2L-1 coordinates using the centered gauges. For each evaluation coordinate,
convolve the sequence of block values over the coarse block index. Apply G
inverse and the post-gauge at each coarse output index, then overlap-add local
coefficients at offsets bL+s. This **complete** program returns the ordinary
polynomial product; `blocks()` executes it literally, including the child calls.

Local gauges now use only O(delta L^2) range. But the program makes M=2L-1
coarse convolution calls of operand length at least N/L. Ignoring every guard,
local operation, inverse and movement cost, its recursive volume ratio is

```
M/L = 2 - 1/L >= 3/2,      L >= 2.
```

The count M cannot be reduced below 2L-1 by a different rank-one local bilinear
interpolation formula: the output coefficient forms are linearly independent,
because every degree 0,...,2L-2 occurs as a monomial product. A decomposition
into M scalar products has output span dimension at most M. This is the
classical polynomial-multiplication rank floor, not a new lower bound.
A cyclic quotient would have a different output contract: z*z mod (z^2-1)=1
loses the required z^2 coefficient. It needs an additional recovery argument.

For fixed L, the literal recursion has exponent log_L(2L-1)>1. Variable
polylogarithmic block lengths do not repair this independent-child realization.
If the root bit size is 2^B and every block length is at most 2^s, after
floor(B/(2s)) levels all nodes still have at least 2^(B/2) bits, while total
operand volume has grown by at least `(3/2)^floor(B/(2s))`. With
s=O(log B), this is exp(Omega(B/log B)), larger than every fixed power of B.
Every descendant must still be read/processed. This assumes independently paid
children with at least linear leaf cost, not a new sharing or encoded-child
contract. Precision growth would only increase the bill.

Thus this local repair is an interpolation/Toom--Cook recursion and fails the
kappa=1/2 target before the omitted costs are restored.

## 4. Evidence, positive escape and reproduction

Standard-library Python 3.12:

```sh
python3 -I -O -B research/gaussian-bilinear-collapse/verify.py
python3 -I -B research/gaussian-bilinear-collapse/test_verify.py
python3 -B scripts/research_package.py --package research/gaussian-bilinear-collapse
```

The read-only receipt checks 790 square identities, all 90 basis-pair pipelines
for lengths 2..6, twenty signed/unequal-input block pipelines, both explicit
rounding failures, the fine-grid positive control, and four exact multi-level
volume certificates. A separate test implementation checks all-gauge constraint
nullity three and output flattening rank 2L-1 through L=12, alternate rational
q and signed inputs, the optimal range, formula/format faults, and isolated
optimized Git-free exports. Receipt types and overwrite refusal are checked.
No predecessor executable or floating-point acceptance decision is used.

A positive changed-premise control uses the exact third root of unity in the
Eisenstein field. Completion of squares still works, the 3-by-3 interpolation
matrix is invertible, and all coefficients have modulus one. The damping-range
obstruction disappears; every kernel entry has full magnitude, so Gaussian
locality also disappears. This control deliberately prevents interpreting the
real-damping result as an impossibility of other representations.

[RESULT.json](RESULT.json) records the complete deterministic evidence.
Sources in [SOURCES.json](SOURCES.json) are historical provenance; this new
model's mathematics is self-contained. No all-size multiplication algorithm,
selected cold replay, proof-assistant, independent-human/agent review or hosted
CI pass is claimed. Finite checks support the written scoped proofs.

## Decision

**Stop this explicit-gauge realization and its independent interpolation
recursion.** The target stays kappa=1/2; neither failure excludes it.

## Open next questions

A meaningful continuation must avoid materializing the high-range middle
**and** provide a complete consumer that does not pay 2L-1 independent coarse
products. The smallest useful next test would specify that new joint-child
interface and prove a bilinear identity with its actual operand bit volumes,
rounding/cleanup boundaries and strict recursive bill. Merely hiding gauges
symbolically, declaring inverse work free, or repeating the experiment at a
larger N would not supply that interface. No next construction round is
justified until such a changed contract is specified.

## Credit and freshness

Classical credit: Gaussian completion of squares, Vandermonde interpolation,
and Toom--Cook polynomial multiplication. Source guidance and constraints:
Douglas Colkitt's assembly-domain audit; BigCactusLabs/PR701; DaysSky/PR657;
Vlado Vojdanovski/PR1673 and the retained Harvey--van der Hoeven, semantic-bulk,
OpenAI-manuscript and community lineage. Their results are credited and are
not presented as defects or newly proved here.

Prepared for David (`sandersdavid90-droid`) with substantial OpenAI Codex
assistance in exploration, derivation, code, checking and writing. New material
is Apache-2.0; frozen predecessors and the selected frontier are unchanged.
[TASK.json](TASK.json) records the explicit moonshot override, scope, budget,
coverage limits, outcomes and final upstream check. Targeted live PR/board reads
supplemented a sparse local checkout; no complete overlap census is claimed.
GitHub upstream write permissions were unavailable in the preceding session,
so no public advance reservation is claimed.
