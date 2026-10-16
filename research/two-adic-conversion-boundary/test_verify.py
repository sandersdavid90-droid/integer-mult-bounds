"""Separately coded mathematical oracles and semantic failure controls."""
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType
import unittest

ROOT = Path(__file__).resolve().parent
C = ModuleType("codec_under_test")
exec(compile((ROOT / "codec.py").read_bytes(), str(ROOT / "codec.py"), "exec", dont_inherit=True), C.__dict__)


class ConversionTests(unittest.TestCase):
    def test_group_against_exhaustive_power_oracle(self):
        # Enumeration by multiplication by 5 shares no bit-lifting algorithm.
        for precision in range(3, 12):
            modulus = 1 << precision
            value = 1
            seen = set()
            for exponent in range(1 << (precision - 2)):
                self.assertNotIn(value, seen)
                seen.add(value)
                self.assertEqual(C.encode(value, precision), (0, exponent))
                self.assertEqual(C.encode((-value) % modulus, precision), (1, exponent))
                value = value * 5 % modulus
            self.assertEqual(value, 1)
            self.assertEqual(seen, set(range(1, modulus, 4)))

    def test_full_products_at_larger_sizes(self):
        rng = random.Random(51005)
        for bits in (8, 15, 32, 65, 128, 257):
            top = (1 << bits) - 1
            pairs = [(0, top), (1, top), (top, top), (top - 1, top - 3)]
            pairs += [(rng.getrandbits(bits), rng.getrandbits(bits)) for _ in range(8)]
            for x, y in pairs:
                self.assertEqual(C.multiply(x, y, bits), x * y)

    def test_collision_formulas_without_logarithms(self):
        # Direct residue equality proves the summary collision independently.
        for n in range(4, 160):
            a, b, precision = C.precision_collision(n)
            product_a, product_b = a[0] * a[1], b[0] * b[1]
            self.assertEqual(product_a - product_b, 1 << precision)
            self.assertEqual(product_a % (1 << precision), product_b % (1 << precision))
            self.assertNotEqual(product_a % (2 << precision), product_b % (2 << precision))
            self.assertLess(max(a), 1 << n)
            a, b, precision = C.augmented_collision(n)
            self.assertEqual(a[0] * a[1] - b[0] * b[1], 1 << precision)
            self.assertEqual(sum(a), sum(b))
            for x, y in zip(a, b):
                self.assertEqual(x % (1 << (n - 2)), y % (1 << (n - 2)))
                self.assertEqual(x % 4, y % 4)
            self.assertGreater(min(b), 0)
            self.assertLess(max(b), 1 << n)

    def test_sharp_block_boundary_and_dependent_repair(self):
        for k in range(3, 8):
            q = 1 << k
            for precision in (k + 1, k + 2):
                for low in range(1, q, 4):
                    for high in range(1 << (precision - k)):
                        expected = C.encode(low + q * high, precision)
                        independent = C.combine(C.encode(low, precision), C.encode(1 + q * high, precision), precision)
                        self.assertEqual(independent, expected)
            precision = k + 3
            self.assertEqual(C.block_defect(k, precision), 1 << k)
            # A multiplicative rectangle oracle: independent additive tables
            # would require diagonal products to agree modulo 2^precision.
            self.assertNotEqual((5 + q) % (1 << precision), (5 * (1 + q)) % (1 << precision))
            for low in range(1, q, 4):
                for high in range(8):
                    corrected = C.dependent_block_encode(low, high, k, 2 * k + 3)
                    self.assertEqual(C.decode(corrected, 2 * k + 3), low + q * high)

    def test_semantic_faults_and_invalid_domains(self):
        # Omitting a sign, omitting powers of two, and dropping product bits
        # each changes a real required result.
        left, right = C.encode(7, 8), C.encode(5, 8)
        bad = (0, (left[1] + right[1]) % 64)
        self.assertNotEqual(C.decode(bad, 8), 35)
        self.assertEqual(C.multiply(7, 5, 3), 35)
        self.assertNotEqual(C.decode(C.combine(C.encode(3, 6), C.encode(5, 6), 6), 6), 60)
        self.assertEqual(C.multiply(6, 10, 4), 60)
        self.assertEqual(C.decode(C.combine(C.encode(7, 4), C.encode(11, 4), 4), 4), 13)
        self.assertEqual(C.multiply(7, 11, 4), 77)
        for value, precision in ((0, 8), (2, 8), (257, 8), (True, 8), (1, 2)):
            with self.assertRaises(ValueError):
                C.encode(value, precision)
        for code in ((2, 0), (0, 64), (0, -1), (False, 0), (0,)):
            with self.assertRaises(ValueError):
                C.decode(code, 8)

    def test_optimized_export_and_typed_receipt_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for filename in ("codec.py", "verify.py", "RESULT.json"):
                shutil.copyfile(ROOT / filename, root / filename)
            command = [sys.executable, "-I", "-O", "-B", str(root / "verify.py")]
            run = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("PASS_TWO_ADIC_CONVERSION_BOUNDARY", run.stdout)
            path = root / "RESULT.json"
            data = json.loads(path.read_text())
            data["pure_example"]["summary"][0] = False  # False == 0 in Python.
            path.write_text(json.dumps(data))
            run = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("receipt mismatch", run.stderr)
            shutil.copyfile(ROOT / "RESULT.json", path)
            output = root / "new.json"
            run = subprocess.run(command + ["--out", str(output)], capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 0, run.stderr)
            before = output.read_bytes()
            run = subprocess.run(command + ["--out", str(output)], capture_output=True, text=True, timeout=30)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
