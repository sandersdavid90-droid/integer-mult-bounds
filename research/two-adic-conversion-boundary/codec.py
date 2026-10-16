"""Exact conversion experiment, Apache-2.0. No performance theorem.

Python big-integer operations are paid obligations, not unit-cost primitives.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, minimum=0):
    require(type(value) is int and value >= minimum, "integer outside domain")


def valuation(value):
    integer(value, 1)
    return (value & -value).bit_length() - 1


def encode(value, precision):
    """Odd residue -> (sign, exponent), value = (-1)^sign 5^exponent."""
    integer(precision, 3)
    integer(value, 1)
    modulus = 1 << precision
    require(value < modulus and value & 1, "expected canonical odd residue")
    sign = int(value % 4 == 3)
    residue = (-value if sign else value) % modulus
    inverse_power = pow(5, -1, modulus)
    exponent = 0
    for j in range(precision - 2):
        if (residue >> (j + 2)) & 1:
            exponent |= 1 << j
            residue = residue * inverse_power % modulus
        inverse_power = inverse_power * inverse_power % modulus
    require(residue == 1, "bit lifting failed")
    return sign, exponent


def check_code(code, precision):
    integer(precision, 3)
    require(type(code) in (tuple, list) and len(code) == 2, "bad code")
    sign, exponent = code
    integer(sign)
    integer(exponent)
    require(sign < 2 and exponent < (1 << (precision - 2)), "noncanonical code")


def decode(code, precision):
    check_code(code, precision)
    sign, exponent = code
    return ((-1 if sign else 1) * pow(5, exponent, 1 << precision)) % (1 << precision)


def combine(left, right, precision):
    check_code(left, precision)
    check_code(right, precision)
    return left[0] ^ right[0], (left[1] + right[1]) % (1 << (precision - 2))


def multiply(x, y, input_bits):
    """Full unsigned product, including zero and even inputs; correctness only."""
    integer(input_bits, 1)
    integer(x)
    integer(y)
    require(max(x, y) < (1 << input_bits), "input does not fit")
    if x == 0 or y == 0:
        return 0
    shift_x, shift_y = valuation(x), valuation(y)
    precision = max(3, 2 * input_bits - shift_x - shift_y)
    left = encode(x >> shift_x, precision)
    right = encode(y >> shift_y, precision)
    return decode(combine(left, right, precision), precision) << (shift_x + shift_y)


def summary(pair, precision, extra_bits=None):
    """The exact restricted reader boundary tested in the note."""
    x, y = pair
    core = combine(encode(x, precision), encode(y, precision), precision)
    if extra_bits is None:
        return core
    integer(extra_bits)
    mask = (1 << extra_bits) - 1
    return core, x + y, x & mask, y & mask


def precision_collision(input_bits):
    integer(input_bits, 4)
    even_bits = input_bits - input_bits % 2
    b = 1 << ((even_bits - 2) // 2)
    return (2 * b * b - 2 * b + 1, 2 * b * b + 2 * b + 1), (1, 1), 2 * even_bits - 2


def augmented_collision(input_bits):
    integer(input_bits, 4)
    center, u = (1 << (input_bits - 1)) + 1, 1 << (input_bits - 3)
    return (center - u, center + u), (center - 3 * u, center + 3 * u), 2 * input_bits - 3


def block_defect(block_bits, precision):
    """Mixed difference of the canonical exponent on a binary block cut."""
    integer(block_bits, 3)
    integer(precision, block_bits + 2)
    q = 1 << block_bits
    e00, e01, e10, e11 = (encode(x, precision)[1] for x in (1, 1 + q, 5, 5 + q))
    return (e00 + e11 - e01 - e10) % (1 << (precision - 2))


def dependent_block_encode(low, high, block_bits, precision):
    """Positive control: the correction depends on low^{-1}."""
    integer(block_bits, 3)
    integer(precision, block_bits + 1)
    integer(low, 1)
    integer(high)
    require(low < (1 << block_bits) and low % 4 == 1, "bad principal-unit low block")
    value = low + (high << block_bits)
    require(value < (1 << precision), "blocks do not fit")
    modulus = 1 << precision
    correction = (1 + (high << block_bits) * pow(low, -1, modulus)) % modulus
    return combine(encode(low, precision), encode(correction, precision), precision)


def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(typed_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def receipt():
    unit_count = 0
    for precision in range(3, 11):
        for value in range(1, 1 << precision, 2):
            require(decode(encode(value, precision), precision) == value, "round trip")
            unit_count += 1
    pair_count = 0
    for bits in range(1, 8):
        for x in range(1 << bits):
            for y in range(1 << bits):
                require(multiply(x, y, bits) == x * y, "full product")
                pair_count += 1
    pure_count = augmented_count = 0
    for bits in range(4, 129):
        first, second, precision = precision_collision(bits)
        require(max(first) < (1 << bits), "collision input width")
        require(first[0] * first[1] - 1 == (1 << precision), "pure polynomial identity")
        require(summary(first, precision) == summary(second, precision), "pure collision")
        require(summary(first, precision + 1) != summary(second, precision + 1), "precision repair")
        pure_count += 1
        first, second, precision = augmented_collision(bits)
        require(0 < min(second) <= max(second) < (1 << bits), "augmented input width")
        require(first[0] * first[1] - second[0] * second[1] == (1 << precision), "augmented identity")
        require(summary(first, precision, bits - 2) == summary(second, precision, bits - 2), "augmented collision")
        require(summary(first, precision + 1, bits - 2) != summary(second, precision + 1, bits - 2), "augmented repair")
        augmented_count += 1
    defects = 0
    for bits in range(3, 33):
        require(block_defect(bits, bits + 2) == 0, "low-precision positive control")
        for precision in (bits + 3, 2 * bits + 3):
            require(valuation(block_defect(bits, precision)) == bits, "mixed-block valuation")
            defects += 1
    independent = combine(encode(5, 6), encode(9, 6), 6)
    corrected = dependent_block_encode(5, 1, 3, 6)
    require(decode(independent, 6) == 45 and decode(corrected, 6) == 13, "block fault and repair")
    require(decode(combine(encode(7, 4), encode(11, 4), 4), 4) == 13, "short product fault")
    first, second, precision = augmented_collision(5)
    return {
        "schema_version": 1,
        "claim": "Scoped exact conversion-boundary results; no kappa improvement",
        "target_kappa": "1/100",
        "unit_round_trips": unit_count,
        "all_small_full_products": pair_count,
        "input_bits_for_full_products": [1, 7],
        "pure_collision_lengths": pure_count,
        "augmented_collision_lengths": augmented_count,
        "collision_input_bits": [4, 128],
        "nonzero_block_defects": defects,
        "zero_defect_precision_controls": 30,
        "pure_example": {"input_pairs": [[5, 13], [1, 1]], "products": [65, 1], "precision": 6, "summary": list(summary((5, 13), 6))},
        "augmented_example": {"input_pairs": [list(first), list(second)], "products": [first[0] * first[1], second[0] * second[1]], "precision": precision, "shared_summary": [list(summary(first, precision)), first[0] + first[1], first[0] & 7, first[1] & 7]},
        "block_table_example": {"low": 5, "high": 1, "block_bits": 3, "precision": 6, "intended": 13, "independent_decode": 45, "dependent_decode": 13, "mixed_exponent_defect": block_defect(3, 6)},
        "complete_codec_example": {"x": 7, "y": 11, "precision": 8, "left_code": list(encode(7, 8)), "right_code": list(encode(11, 8)), "product": multiply(7, 11, 4)},
    }
