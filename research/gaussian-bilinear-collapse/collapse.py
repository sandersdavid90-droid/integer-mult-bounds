"""Exact Gaussian product-collapse experiment. Standard-library rational arithmetic.

Prepared for David with substantial OpenAI Codex assistance. Apache-2.0.
Completion of squares and Toom--Cook interpolation are classical, not new claims.
"""
from fractions import Fraction as Q


def need(condition, message):
    if not condition:
        raise ValueError(message)


def convolution(x, y):
    out = [Q(0)] * (len(x) + len(y) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i+j] += a*b
    return out


def matvec(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector, strict=True)), Q(0))
            for row in matrix]


def inverse(matrix):
    n = len(matrix)
    work = [list(row) + [Q(int(i == j)) for j in range(n)]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        need(pivot is not None, 'singular interpolation')
        work[j], work[pivot] = work[pivot], work[j]
        value = work[j][j]
        work[j] = [x/value for x in work[j]]
        for i in range(n):
            if i != j:
                value = work[i][j]
                work[i] = [x-value*y for x, y in zip(work[i], work[j], strict=True)]
    return [row[n:] for row in work]


def setup(length, q=Q(1, 2)):
    need(type(length) is int and 2 <= length <= 8, 'bounded local length')
    need(isinstance(q, Q) and 0 < q < 1, 'real damping parameter')
    n, m = length-1, 2*length-1
    # The optimal common affine recentering for the three gauge ranges.
    pre = [q**(4*n*i - 4*i*i) for i in range(length)]
    post = [q**(2*k*k - 4*n*k) for k in range(m)]
    forward = [[q**((k-2*i)**2)*pre[i] for i in range(length)] for k in range(m)]
    gaussian = [[q**(2*(k-s)**2) for s in range(m)] for k in range(m)]
    return forward, inverse(gaussian), post


def pair(x, y, plan):
    forward, backward, post = plan
    left, right = matvec(forward, x), matvec(forward, y)
    middle = [a*b for a, b in zip(left, right, strict=True)]
    return [scale*value for scale, value in
            zip(post, matvec(backward, middle), strict=True)]


def blocks(x, y, length, plan):
    """The local-recentering pivot, with actual coarse convolution calls counted."""
    kx, ky = (len(x)+length-1)//length, (len(y)+length-1)//length
    left = [matvec(plan[0], list(x[b*length:(b+1)*length]) +
                   [Q(0)] * max(0, (b+1)*length-len(x))) for b in range(kx)]
    right = [matvec(plan[0], list(y[b*length:(b+1)*length]) +
                    [Q(0)] * max(0, (b+1)*length-len(y))) for b in range(ky)]
    m = 2*length-1
    child_outputs = [convolution([row[k] for row in left],
                                 [row[k] for row in right]) for k in range(m)]
    out = [Q(0)] * ((kx+ky-2)*length + m)
    for coarse in range(kx+ky-1):
        local = matvec(plan[1], [row[coarse] for row in child_outputs])
        for s, (scale, value) in enumerate(zip(plan[2], local, strict=True)):
            out[coarse*length+s] += scale*value
    return out[:len(x)+len(y)-1], m


def round_grid(value, bits):
    scaled = value * 2**bits
    quotient, remainder = divmod(scaled.numerator, scaled.denominator)
    twice = 2*remainder
    if twice > scaled.denominator or (twice == scaled.denominator and quotient % 2):
        quotient += 1
    return Q(quotient, 2**bits)


def span(values):
    return max(values)-min(values)


def integer_gauge(length, slope, a=0, b=0):
    n = length-1
    left = [-4*i*i+slope*i+a for i in range(length)]
    right = [-4*j*j+slope*j+b for j in range(length)]
    output = [2*k*k-slope*k-a-b for k in range(2*n+1)]
    return left, right, output


def check_gauge(length, gauges):
    a, b, c = gauges
    for i in range(length):
        for j in range(length):
            need(a[i]+b[j]+c[i+j]+2*(i-j)**2 == 0, 'uncorrected pair weight')


def receipt():
    identity_cases, pair_cases, block_cases = 0, 0, 0
    profiles = []
    for length in range(2, 7):
        n, m = length-1, 2*length-1
        plan = setup(length)
        for i in range(length):
            for j in range(length):
                for k in range(m):
                    need((k-2*i)**2+(k-2*j)**2 ==
                         2*(k-i-j)**2+2*(i-j)**2, 'square identity')
                    identity_cases += 1
                x = [Q(int(s == i)) for s in range(length)]
                y = [Q(int(s == j)) for s in range(length)]
                need(pair(x, y, plan) == convolution(x, y), 'basis-pair pipeline')
                pair_cases += 1
        for count in range(1, 5):
            x = [Q((3*i+count) % 7-3) for i in range(count*length)]
            y = [Q((2*i-count) % 5-2) for i in range(count*length-1)]
            actual, calls = blocks(x, y, length, plan)
            need(actual == convolution(x, y) and calls == m, 'block pipeline')
            block_cases += 1
        check_gauge(length, integer_gauge(length, 4*n))
        need(max(map(span, integer_gauge(length, 4*n))) == 2*n*n,
             'sharp joint gauge range')
        need(m*m > 2*length*length, 'half-saving child budget')
        profiles.append({'block_length': length, 'children': m,
                         'optimistic_volume_ratio': str(Q(m, length)),
                         'optimal_log2_gauge_span_at_q_half': 2*n*n})
    # A real complete-product failure: even exact forward maps are insufficient.
    length, bits = 4, 8
    x, y = [Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(0), Q(0), Q(1)]
    plan = setup(length)
    left, right = matvec(plan[0], x), matvec(plan[0], y)
    middle = [a*b for a, b in zip(left, right, strict=True)]
    rounded = [round_grid(value, bits) for value in middle]
    need(max(middle) == Q(1, 2**18) and not any(rounded), 'lost far pair')
    need(pair(x, y, plan)[3] == 1, 'far-pair positive control')
    # A fully exact larger grid restores every measured product in this example.
    fine = [round_grid(value, 8*(length-1)**2) for value in middle]
    need(fine == middle, 'changed-precision positive control')
    # Observable data range, not just a table of potentially symbolic weights.
    dense_length = 8
    dense_plan = setup(dense_length)
    evaluated = matvec(dense_plan[0], [Q(1)] * dense_length)
    dense_middle = matvec(dense_plan[1], [z*z for z in evaluated])
    need(max(dense_middle) == 1 and min(dense_middle) == Q(1, 2**95),
         'materialized middle data range')
    need(dense_plan[2][7]*dense_middle[7] == 8 and
         dense_plan[2][7]*round_grid(dense_middle[7], 32) == 0,
         'rounded dense middle loses coefficient eight')
    # Multi-level volume lower bound: root n=2^B, block lengths <=2^s.
    depth_rows = []
    for exponent, s in [(64, 3), (256, 4), (1024, 5), (4096, 6)]:
        depth = exponent//(2*s)
        factor = Q(3, 2)**depth
        need(exponent-s*depth >= exponent//2, 'minimum surviving depth')
        need(factor*factor > exponent, 'frontier exceeds square-root-log budget')
        depth_rows.append({'root_log2_bits': exponent, 'max_log2_block': s,
                           'levels_before_half_size': depth,
                           'normalized_frontier_lower_bound': str(factor)})
    return {'schema_version': 1, 'status': 'PASS_GAUSSIAN_BILINEAR_COLLAPSE',
            'target_kappa': '1/2', 'new_kappa': None,
            'outcome': 'explicit gauges fail the precision gate; block recentering fails the child-volume gate',
            'square_identity_checks': identity_cases, 'basis_pair_pipelines': pair_cases,
            'signed_block_pipelines': block_cases, 'profiles': profiles,
            'far_pair_control': {'length': length, 'common_fractional_bits': bits,
                                 'largest_product': '1/262144',
                                 'true_middle_coefficient': 1, 'rounded_result': 0},
            'dense_middle_control': {'length': 8, 'largest_value': '1',
                                     'smallest_value': '1/'+str(2**95),
                                     'minimum_log2_range': 95,
                                     'true_middle_coefficient': 8,
                                     'after_32_bit_middle_rounding': 0},
            'depth_bounds': depth_rows,
            'scope': 'This explicit Gaussian collapse and independent local-interpolation recursion only; no general multiplication barrier.'}
