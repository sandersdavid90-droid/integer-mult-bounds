"""Independent identities, exact rank checks and failure/escape controls."""
import copy
from fractions import Fraction as Q
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType
import unittest

HERE = Path(__file__).resolve().parent
v = ModuleType('collapse')
exec(compile((HERE / 'collapse.py').read_bytes(), str(HERE / 'collapse.py'),
             'exec', dont_inherit=True), v.__dict__)


def rank(matrix):
    rows, pivot = [[Q(x) for x in row] for row in matrix], 0
    for column in range(len(rows[0])):
        found = next((i for i in range(pivot, len(rows)) if rows[i][column]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        factor = rows[pivot][column]
        rows[pivot] = [x/factor for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot:
                factor = rows[i][column]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[pivot], strict=True)]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def eis_add(x, y):
    return x[0]+y[0], x[1]+y[1]


def eis_mul(x, y):
    a, b = x
    c, d = y
    return a*c-b*d, a*d+b*c-b*d


def omega(exponent):
    return ((1, 0), (0, 1), (-1, -1))[exponent % 3]


class CollapseTests(unittest.TestCase):
    def test_independent_direct_gaussian_identity(self):
        q = Q(1, 3)
        for length in range(2, 8):
            x = [Q(2*i-length, i+1) for i in range(length)]
            y = [Q((-1)**i, i+2) for i in range(length)]
            for k in range(2*length-1):
                a = sum((x[i]*q**((k-2*i)**2) for i in range(length)), Q(0))
                b = sum((y[j]*q**((k-2*j)**2) for j in range(length)), Q(0))
                collapsed = Q(0)
                for s in range(2*length-1):
                    coefficient = sum((x[i]*y[s-i]*q**(2*(2*i-s)**2)
                                       for i in range(length) if 0 <= s-i < length), Q(0))
                    collapsed += q**(2*(k-s)**2)*coefficient
                self.assertEqual(a*b, collapsed)
            self.assertEqual(v.pair(x, y, v.setup(length, q)), v.convolution(x, y))

    def test_gauge_completeness_and_optimality(self):
        for length in range(2, 13):
            m, n = 2*length-1, length-1
            constraints = []
            for i in range(length):
                for j in range(length):
                    row = [0] * (2*length+m)
                    row[i] = row[length+j] = row[2*length+i+j] = 1
                    constraints.append(row)
            self.assertEqual(2*length+m-rank(constraints), 3)
            for numerator in range(-4*n, 12*n+1):
                slope = Q(numerator, 2)
                gauges = v.integer_gauge(length, slope, Q(1, 3), Q(-2, 5))
                v.check_gauge(length, gauges)
                self.assertGreaterEqual(max(map(v.span, gauges)), 2*n*n)
            self.assertEqual(max(map(v.span, v.integer_gauge(length, 4*n))), 2*n*n)
            for slope in range(-4*n, 12*n+1):
                c = v.integer_gauge(length, slope)[2]
                middle = [Q(min(k+1, 2*n+1-k, length)) * Q(2)**c[k]
                          for k in range(2*n+1)]
                self.assertGreaterEqual(max(middle)/min(middle)*length,
                                        Q(2)**(2*n*n))
        bad = v.integer_gauge(5, 16)
        bad[0][2] += 1
        with self.assertRaisesRegex(ValueError, 'pair weight'):
            v.check_gauge(5, bad)

    def test_bilinear_output_rank(self):
        for length in range(2, 13):
            matrix = [[int(i+j == s) for i in range(length) for j in range(length)]
                      for s in range(2*length-1)]
            self.assertEqual(rank(matrix), 2*length-1)
            self.assertGreater((2*length-1)**2, 2*length**2)
        # A cyclic quotient is a changed, insufficient output contract.
        ordinary = v.convolution([0, 1], [0, 1])
        cyclic = [ordinary[0]+ordinary[2], ordinary[1]]
        self.assertEqual(ordinary, [0, 0, 1])
        self.assertEqual(cyclic, [1, 0])

    def test_semantic_faults_and_precision_repair(self):
        x, y = [1, 0, 0, 0], [0, 0, 0, 1]
        plan = v.setup(4)
        a, b = v.matvec(plan[0], x), v.matvec(plan[0], y)
        middle = [u*w for u, w in zip(a, b, strict=True)]
        self.assertFalse(any(v.round_grid(z, 8) for z in middle))
        unscaled = v.matvec(plan[1], middle)
        self.assertNotEqual(unscaled, v.convolution(x, y))
        wrong_inverse = v.inverse([[Q(1, 2)**((i-j)**2) for j in range(7)]
                                   for i in range(7)])
        wrong = [c*z for c, z in zip(plan[2], v.matvec(wrong_inverse, middle), strict=True)]
        self.assertNotEqual(wrong, v.convolution(x, y))
        fine = [v.round_grid(z, 72) for z in middle]
        fixed = [c*z for c, z in zip(plan[2], v.matvec(plan[1], fine), strict=True)]
        self.assertEqual(fixed, v.convolution(x, y))

    def test_unit_phase_escape_has_dense_support(self):
        # q=omega, omega^2+omega+1=0: exact arithmetic, not complex floats.
        length, m = 2, 3
        matrix = [[omega(2*(k-s)**2) for s in range(m)] for k in range(m)]
        determinant = (0, 0)
        for permutation, sign in [((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1),
                                  ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)]:
            term = (sign, 0)
            for row, column in enumerate(permutation):
                term = eis_mul(term, matrix[row][column])
            determinant = eis_add(determinant, term)
        self.assertNotEqual(determinant, (0, 0))
        for i in range(length):
            for j in range(length):
                for k in range(m):
                    lhs = eis_mul(omega((k-2*i)**2), omega((k-2*j)**2))
                    rhs = eis_mul(omega(2*(k-i-j)**2), omega(2*(i-j)**2))
                    self.assertEqual(lhs, rhs)
        # Every phase has norm one; none can be removed by a decay cutoff.
        self.assertTrue(all(a*a-a*b+b*b == 1 for row in matrix for a, b in row))

    def test_export_receipt_and_output_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            export = Path(tmp) / 'export'
            shutil.copytree(HERE, export, ignore=shutil.ignore_patterns('__pycache__'))
            command = [sys.executable, '-I', '-O', '-B', str(export / 'verify.py')]
            good = subprocess.run(command, cwd=tmp, capture_output=True, text=True, timeout=30)
            self.assertEqual(good.returncode, 0, good.stderr)
            result = json.loads((export / 'RESULT.json').read_text())
            changed = copy.deepcopy(result)
            changed['schema_version'] = True
            (export / 'RESULT.json').write_text(json.dumps(changed))
            bad = subprocess.run(command, cwd=tmp, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn('typed receipt', bad.stderr)
            (export / 'RESULT.json').write_text(json.dumps(result))
            with (export / 'RESULT.json').open('a') as out:
                out.write('garbage')
            self.assertNotEqual(subprocess.run(command, cwd=tmp, capture_output=True,
                                               text=True, timeout=30).returncode, 0)
            (export / 'RESULT.json').write_text(json.dumps(result))
            output = Path(tmp) / 'occupied.json'
            output.write_text('preserve me')
            overwrite = subprocess.run(command+['--out', str(output)], cwd=tmp,
                                       capture_output=True, text=True, timeout=30)
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertEqual(output.read_text(), 'preserve me')


if __name__ == '__main__':
    unittest.main()
