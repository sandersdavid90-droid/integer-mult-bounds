#!/usr/bin/env python3
"""Read-only replay of one kappa=1/2 structural experiment; no new bound."""
import argparse
import json
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def load_candidate():
    path = HERE / 'collapse.py'
    module = ModuleType('gaussian_collapse')
    # Compile current source explicitly; -B alone does not disable .pyc reads.
    exec(compile(path.read_bytes(), str(path), 'exec', dont_inherit=True), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    actual = load_candidate().receipt()
    expected = json.loads((HERE / 'RESULT.json').read_bytes(), object_pairs_hook=unique)
    if canonical(actual) != canonical(expected):
        raise ValueError('complete typed receipt mismatch')
    if args.out:
        with args.out.open('x', encoding='utf-8') as out:
            out.write(json.dumps(actual, indent=2) + '\n')
    print(json.dumps(actual, indent=2))


if __name__ == '__main__':
    main()
