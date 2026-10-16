"""Read-only exact replay; no Git, network or third-party dependencies."""
import argparse
import json
from pathlib import Path
from types import ModuleType


def fresh_module(path):
    module = ModuleType("conversion_codec")
    exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="write a fresh receipt; refuses to overwrite")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    codec = fresh_module(root / "codec.py")
    result = codec.receipt()
    expected = json.loads((root / "RESULT.json").read_text(encoding="utf-8"))
    codec.require(codec.typed_equal(result, expected), "receipt mismatch (including field types)")
    if args.out:
        with args.out.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(result, indent=2) + "\n")
    print("PASS_TWO_ADIC_CONVERSION_BOUNDARY products=" + str(result["all_small_full_products"]) + " collisions=" + str(result["pure_collision_lengths"] + result["augmented_collision_lengths"]) + " block_defects=" + str(result["nonzero_block_defects"]) + " no_new_kappa")


if __name__ == "__main__":
    main()
