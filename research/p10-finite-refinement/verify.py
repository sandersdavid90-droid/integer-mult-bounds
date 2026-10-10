#!/usr/bin/env python3
"""Exact finite refinement of the unchanged, source-bound PR317 construction.

Apache-2.0. Prepared for David with substantial OpenAI Codex assistance.
Construction and inherited verifier authorship are recorded in NOTICE.md.
"""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys

if not __debug__:
    raise SystemExit("Assertions required; refusing -O")
sys.dont_write_bytecode = True
sys.set_int_max_str_digits(0)
HEAD = "0a0b61a7f4601a96036af8bb6a6338c58f035d2e"
MANIFEST = "97c731bdb7ecb3c1957bef11f90f824a586ee7bc8a41fa79c12bd39b08fe9a6f"
WORD = "e6ad3590e6ad83a6df4f202adda6fe899ed0c60b20822f608db3de670468f61e"
OLD = Q(76817007781759, 10**17)
GRID = Q(1, 10**27)
ETA = Q(1, 10**24)
BETA = Q(1, 10**9)  # Retain PR317's complex reservation.
DYAD = 2**256


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serial(v) for v in x]
    return x


def floor_dyad(x):
    return Q(x.numerator * DYAD // x.denominator, DYAD)


def ceil_dyad(x):
    return -floor_dyad(-x)


def log_small(x):
    """2 atanh((x-1)/(x+1)); positive terms with an explicit tail."""
    assert 1 <= x <= 2
    z = (x - 1) / (x + 1)
    term, total = z, Q(0)
    for j in range(100):
        total += 2 * term / (2*j + 1)
        term *= z*z
    tail = 2 * term / (201 * (1-z*z))
    return floor_dyad(total), ceil_dyad(total + tail)


@lru_cache(None)
def log_interval(x):
    assert x >= 1
    power = 0
    while x >= 2:
        x /= 2
        power += 1
    lo, hi = log_small(x)
    l2, h2 = log_small(Q(2))
    return lo + power*l2, hi + power*h2


def exp_interval(lo, hi):
    assert 0 <= lo <= hi < Q(1, 100)
    def poly(x):
        term = total = Q(1)
        for j in range(1, 33):
            term = term*x/j
            total += term
        return total, term
    low, _ = poly(lo)
    high, last = poly(hi)
    tail = last*hi/33/(1-hi/34)
    return floor_dyad(low), ceil_dyad(high+tail)


def moment(histogram, width, stock, saving):
    lo = hi = Q(0)
    counts = Counter(histogram)
    counts[1] += Q(32*width*width*sum(histogram.values()), 10**16)
    for rank, count in counts.items():
        assert 0 < rank < width and count > 0
        l, h = log_interval(Q(width, rank))
        el, eh = exp_interval(saving*l, saving*h)
        weight = Q(rank*count, width*stock)
        lo += weight*el
        hi += weight*eh
    return floor_dyad(lo), ceil_dyad(hi)


def root_floor(histogram, width, stock, previous):
    low = int(previous / GRID)
    high = int((previous + Q(1, 10**18)) / GRID)
    assert moment(histogram, width, stock, low*GRID)[1] < 1
    assert moment(histogram, width, stock, high*GRID)[0] > 1
    while high-low > 1:
        mid = (low+high)//2
        lower, upper = moment(histogram, width, stock, mid*GRID)
        if upper < 1:
            low = mid
        elif lower > 1:
            high = mid
        else:
            raise AssertionError("Interval straddles one; increase precision")
    return low*GRID


def cutoff(gap, coefficient):
    assert 0 < gap <= 1 and isinstance(coefficient, int) and coefficient >= 1
    ceil = lambda q: -((-q.numerator)//q.denominator)
    bits = (coefficient-1).bit_length()
    n = max(1, ceil(36/gap**2), ceil(2*(4+bits)/gap))
    assert n*gap*gap >= 36 and n*gap >= 2*(4+bits)
    return n


def bootstrap(c, levels, coefficient):
    start = Q(384599, 10**10)
    chain, cuts = [start], []
    for j in range(levels):
        old = chain[-1]
        new = (1-c)*c+c*old
        # A second derivation of the geometric convergence, not a float check.
        assert new == c-c**(j+1)*(c-start)
        gaps = dict(atom=c-new, borrowing=1-new-c,
                    remainder=1-new-c*(1-old), stock=1-c)
        assert old < new < c and min(gaps.values()) > 0
        chain.append(new)
        cuts.append(dict(level=j+1, gaps=gaps,
                         counted_coefficient_cutoff_log2=cutoff(min(gaps.values()), coefficient)))
    return chain, cuts


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_source(root):
    assert sha(root/'MANIFEST.json') == MANIFEST, "Wrong pinned package"
    expected = read(root/'MANIFEST.json')['files']
    actual = {}
    for p in root.rglob('*'):
        assert not p.is_symlink()
        if p.is_file() and p != root/'MANIFEST.json':
            actual[p.relative_to(root).as_posix()] = sha(p)
    assert actual == expected, "Missing, changed or unpinned source"


def verify(root, replay):
    check_source(root)
    certificate = read(replay/'CERTIFICATE.json')
    execution = read(replay/'VERIFICATION.json')
    assert certificate['status'] == 'PASS_SOURCE_BOUND_P10_KERNEL_TARGET_PLATEAU_RESTORE_REORDER_CONDITIONAL_CONSTRUCTION'
    assert execution['status'] == certificate['status'] and execution['inputs_unchanged']
    assert execution['manifest_sha256'] == MANIFEST
    assert execution['word_sha256'] == certificate['word_sha256'] == WORD
    assert Q(certificate['kappa']) == Q(execution['kappa']) == OLD
    for name, digest in certificate['fresh_receipt_hashes'].items():
        assert sha(replay/name) == digest, ("Changed receipt", name)
    raw = replay/'candidate/COHORT249-RECORDS.bin'
    assert sha(raw) == WORD
    local = Counter()
    for op, a, b, c, f, z in struct.iter_unpack('<6i', raw.read_bytes()):
        if op == 0 and f:
            local[f] += 1
        elif op == 2:
            local[z] += 1
    histogram = Counter({r: 60*n for r, n in local.items()})
    histogram.update({r: 23040 for r in (4, 19, 38, 42)})
    stock = 132138
    assert sum(r*n for r,n in histogram.items()) == 13189320
    assert 100*stock-sum(r*n for r,n in histogram.items()) == 24480
    price = read(replay/'PRICE.json')
    assert dict(histogram) == {int(r):n for r,n in price['cohort_candidate']['histogram'].items()}
    invoice = read(replay/'INVOICE.json')
    coefficient = int(invoice['full_counted_primitive_coefficient'])
    assert coefficient == certificate['finite_coefficient'] == 25350779320984001
    assert invoice['payload_bits'] == 90
    old_c = Q(price['bit_root'])
    c = root_floor(histogram, 100, stock, old_c)
    interval = moment(histogram, 100, stock, c)
    next_interval = moment(histogram, 100, stock, c+GRID)
    assert interval[1] < 1 < next_interval[0]
    delta_tau = 1-interval[1]
    delta_linear = 1-Q(sum(r*n for r,n in histogram.items()),100*stock)-Q(3200*sum(histogram.values()),10**16*stock)
    assert delta_tau > 0 and delta_linear == Q(invoice['linear_moment_slack']) > 0

    # Cross-check the new grid in both unchanged inherited moment engines.
    vendor = root/'vendor/pr315'
    mercator = load('pr317_mercator', vendor/'moment.py')
    base_two = load('pr317_base_two', vendor/'base_two_moment.py')
    cross = {}
    for label, saving in [('accepted', c), ('rejected', c+GRID)]:
        first = mercator.moment(histogram, 100, stock, saving, True)
        ordinary = base_two.moment(100, stock, list(histogram.items()), saving)
        bad = base_two.moment(100, stock, [(1, 320000*sum(histogram.values()))], saving)
        second = tuple(x+Q(1,10**16)*y for x,y in zip(ordinary,bad))
        assert (first[1] < 1 and second[1] < 1) if label == 'accepted' else (first[0] > 1 and second[0] > 1)
        cross[label] = dict(mercator=first, base_two=second)

    complex_hist = {int(r):n for r,n in read(replay/'baseline/complex.json')['five_stage_histogram'].items()}
    b = Q(price['complex_saving'])
    assert moment(complex_hist, 110, 14316, b)[1] < 1
    assert c < (1-BETA)*b
    chain, cuts = bootstrap(c, 8, coefficient)
    a = chain[-1]
    q = (1-2*ETA)*a
    minimum = (1-ETA)*q/(1+q)
    ticks = minimum / GRID
    kappa = ((ticks.numerator-1)//ticks.denominator)*GRID
    outer = load('pr317_outer', vendor/'outer.py')
    bridge = dict(semantic=dict(strict_literal_gap=1, C0=dict(base=2, exponent=210000)),
                  rows=dict(degree_gap=Q(10**6)-Q(51*20161,25)))
    assembly = outer.assembly(a, b, bridge, kappa, eta=ETA, beta=BETA)
    assert assembly['minimum_margin'] == minimum
    assert len(assembly['strict_constraints']) == 47
    assert min(assembly['strict_constraints'].values()) > 0
    assert kappa < minimum <= kappa+GRID and kappa > OLD
    # Reconstruct the published baseline before crediting the change.
    old_chain, _ = bootstrap(old_c, 3, coefficient)
    old_q = old_chain[-1]*(1-2*Q(1,10**12))
    old_min = (1-Q(1,10**12))*old_q/(1+old_q)
    assert OLD < old_min <= OLD+Q(1,10**18)
    # A bound for this unchanged histogram and this assembly, not all circuits.
    upper = (c+GRID)/(1+c+GRID)
    assert kappa < upper
    controls = []
    for name, action in [
        ('adjacent headline', lambda: outer.assembly(a,b,bridge,kappa+GRID,eta=ETA,beta=BETA)),
        ('zero ordinary gap', lambda: cutoff(Q(0),coefficient)),
        ('zero outer reservation', lambda: outer.assembly(a,b,bridge,kappa,eta=Q(0),beta=BETA)),
        ('unreduced three-level leaf', lambda: outer.assembly(old_chain[-1],b,bridge,kappa,eta=ETA,beta=BETA)),
    ]:
        try:
            action()
        except AssertionError:
            controls.append(name)
        else:
            raise AssertionError(('Mutation was accepted',name))
    check_source(root)
    with localcontext() as ctx:
        ctx.prec = 50
        decimal = str(Decimal(kappa.numerator)/Decimal(kappa.denominator))
    return dict(status='PASS_UNCHANGED_PR317_EIGHT_LEVEL_FINITE_REFINEMENT', source_head=HEAD,
                source_manifest_sha256=MANIFEST, word_sha256=WORD,
                baseline_kappa=OLD, kappa=kappa, kappa_decimal=decimal,
                gain=kappa-OLD, relative_gain=(kappa-OLD)/OLD,
                bit_saving=c, bit_interval=interval, next_bit_interval=next_interval,
                recurrence_slacks=dict(delta_tau_lower=delta_tau, delta_linear=delta_linear,
                                       multiplier=1+1/delta_tau+1/delta_linear),
                inherited_moment_crosschecks=cross, complex_saving=b,
                histogram=dict(histogram), normalized_stock=stock, fallback_density=Q(1,10**16),
                eta=ETA, beta=BETA, ordinary_chain=chain, ordinary_cutoffs=cuts,
                finite_coefficient=coefficient, assembly=assembly,
                same_profile_assembly_upper=upper, headroom_upper=upper-kappa,
                rejected_controls=controls,
                full_constant_rule='At every level use C_full bounding the counted coefficient, inherited primitive, wrapper and preceding-level constants in max(1, ceil(36/delta^2), ceil(2*(4+ceil(log2(C_full)))/delta)). Counted-coefficient cutoffs do not instantiate C_full.',
                scope='Conditional finite refinement only; unchanged PR317 circuit, physical admission, banks, compiler, charts, restored rows, prime supply, precision/recovery, complex lifting and analytic-transfer hypotheses. No new circuit mechanism, optimality over other profiles, Lean proof, or runtime claim.')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root', type=Path, required=True, help='Pinned PR317 repository checkout')
    ap.add_argument('--output', type=Path, required=True, help='Fresh output directory')
    ap.add_argument('--reuse-replay', type=Path, help='Explicitly reuse authenticated prior full replay; does not claim fresh execution')
    ap.add_argument('--cxx', default='c++')
    ap.add_argument('--boost-include', type=Path)
    args = ap.parse_args()
    root = args.source_root.resolve()/'research/p10-composed-stages'
    check_source(root)
    out = args.output.resolve()
    assert not out.exists() and not out.is_relative_to(root)
    out.mkdir(parents=True)
    replay = args.reuse_replay.resolve() if args.reuse_replay else out/'source-replay'
    if not args.reuse_replay:
        command = [sys.executable,'-B',str(root/'verify.py'),'--output',str(replay),'--cxx',args.cxx]
        if args.boost_include:
            command += ['--boost-include',str(args.boost_include.resolve())]
        subprocess.run(command,check=True)
    result = verify(root,replay)
    result['source_replay_mode'] = 'authenticated prior replay' if args.reuse_replay else 'fresh full replay'
    result['source_execution_sha256'] = sha(replay/'VERIFICATION.json')
    (out/'certificate.json').write_text(json.dumps(serial(result),sort_keys=True,indent=2)+'\n')
    print('PASS conditional kappa = '+result['kappa_decimal'],flush=True)
    print('Absolute gain = '+str(result['gain']),flush=True)


if __name__ == '__main__':
    main()
