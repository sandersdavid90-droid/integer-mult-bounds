# Eight finite levels on the unchanged PR317 word

This statement is conditional on exactly the construction interfaces retained
by PR317 at `0a0b61a7f4601a96036af8bb6a6338c58f035d2e`. Its package manifest is
`97c731bdb7ecb3c1957bef11f90f824a586ee7bc8a41fa79c12bd39b08fe9a6f`.
The complete source verifier must pass. A successful arithmetic check alone
does not admit the physical construction.

## Unchanged construction and moment

The final binary word has SHA256
`e6ad3590e6ad83a6df4f202adda6fe899ed0c60b20822f608db3de670468f61e`.
We recount its MOVE ranks and COPY calls directly, multiply local counts by
60, and add 23,040 calls at each of ranks 4, 19, 38 and 42. This is PR317's
integral normalized five-stage profile, with width 100, stock 132,138,
rank mass 13,189,320 and deficit 24,480. The physical stock remains 660,690;
normalization is used only in the moment, never in the finite invoice.

For histogram H, width m and stock W, the increasing moment is

    M(s) = sum_r H[r] r/(m W) exp(s log(m/r))
           + 32 m sum_r H[r]/(10^16 W) exp(s log m).

The entire inherited bad-class fallback remains present. We do not tighten
its density or change the prime choice. A bisection on a 10^-27 grid uses
rigorous rational intervals to find c such that M(c)<1<M(c+10^-27).
The two unchanged upstream moment engines separately verify both endpoints.
The refined recurrence uses its own positive slack 1-M(c), conservatively
bounded with the new interval's upper endpoint, rather than reusing PR317's
larger old slack. The unchanged linear slack is recomputed and matched to
the physical invoice. The certificate records the resulting multiplier
1+1/delta_tau+1/delta_linear; the full constant in the cutoff rule must
include this changed recurrence constant.

The third engine here is independently written. Reduce a logarithm's
argument to [1,2), and evaluate log(x)=2 atanh((x-1)/(x+1)). After 100 terms,
with z=(x-1)/(x+1), the omitted positive tail is at most
2 z^201/(201(1-z^2)). Log 2 uses the same bound. The exponential uses terms
through degree 32; at a nonnegative argument u<1/100 its tail is at most
(u^32/32!) (u/33)/(1-u/34). Every rounding is outward to a 256-bit dyadic.
Thus no floating-point decision admits a root or an inequality.

## Finite ordinary levels

Retain the initial saving a0=384599/10^10. For j=0,...,7 choose

    a(j+1) = (1-c)c + c a(j).

Induction gives a(j)=c-c^j(c-a0), so a(j)<a(j+1)<c. At each level the
atom, borrowing, remainder and stock gaps are respectively

    c-a(j+1), 1-a(j+1)-c,
    1-a(j+1)-c(1-a(j)), 1-c.

All are checked as strictly positive rational numbers. For their minimum
delta and any full inherited constant C_full>=1, the same source absorption
rule gives a sufficient logarithmic cutoff

    L >= max(1, ceil(36/delta^2),
             ceil(2(4+ceil(log2 C_full))/delta)).

The certificate evaluates this rule at PR317's counted primitive coefficient
25,350,779,320,984,001. Those displayed cutoffs are not full numerical
algorithm thresholds: C_full must also bound the inherited primitive,
wrapper and preceding-level constants. Each is finite under the retained
interfaces, and eight applications are a fixed finite number of levels.
All physical costs, selectors, rational charts, unit-expanded additions and
the 90-bit payload bound are inherited unchanged from the freshly admitted
word. They are not set to zero or hidden by a new normalization.

## Balanced assembly and exact grid

Use a=a8, eta=10^-24 and the unchanged beta=10^-9. The complex saving remains
b=772714351296671/10^18. Its complete fallback-inclusive moment is also
checked by our third engine, and c<(1-beta)b ensures it does not bind.
Define q=(1-2 eta)a and

    K=(1-eta)q/(1+q).

Choose the largest multiple k of 10^-27 strictly below K. The unchanged
balanced assembly checks all 47 strict constraints and all seven margins;
its minimum equals K exactly. The next grid point is rejected. All-size
compiler, weighted-chart, restored-row, routing, prime-supply,
precision/recovery and analytic-transfer obligations remain conditional.

For this same paid profile and balanced assembly, every positive-reservation
finite-level choice has k<a/(1+a)<c_star/(1+c_star), where c_star is the
unique moment root. Since c_star<c+10^-27, the certificate's rational
(c+10^-27)/(1+c+10^-27) is an upper bound for this restricted family.
It does not bound alternate circuits, other assemblies, or multiplication
algorithms. Comparing our k with this upper bound measures how little room
remains in arithmetic tuning alone.

## Evidence boundary

Default verification executes PR317's entire source-bound verifier afresh,
including its immutable PR315 dependency. Explicit `--reuse-replay` mode
authenticates the source package, word and every bound receipt and labels
the result as reused execution. It never relabels saved PASS evidence as a
fresh run. Independent work here covers moments, bootstrap arithmetic and
the restricted headroom bound; physical/scalar/chart admission uses the
upstream verifier. This is not a new Lean proof or a practical benchmark.
