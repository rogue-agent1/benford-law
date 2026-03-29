#!/usr/bin/env python3
"""benford_law - Benford's Law analysis."""
import sys, argparse, json, math, re
from collections import Counter

def expected_benford(d):
    return math.log10(1 + 1/d)

def analyze(numbers):
    first_digits = []
    for n in numbers:
        s = re.sub(r"[^0-9]", "", str(n).lstrip("0").lstrip("-"))
        if s: first_digits.append(int(s[0]))
    freq = Counter(first_digits)
    total = len(first_digits)
    results = []
    chi_sq = 0
    for d in range(1, 10):
        observed = freq.get(d, 0) / total if total else 0
        expected = expected_benford(d)
        chi_sq += ((observed - expected)**2) / expected if expected else 0
        results.append({"digit": d, "observed": round(observed, 4), "expected": round(expected, 4), "count": freq.get(d, 0), "deviation": round(abs(observed - expected), 4)})
    return {"total_numbers": total, "chi_squared": round(chi_sq, 4), "conformity": "good" if chi_sq < 15.51 else "poor", "digits": results}

def main():
    p = argparse.ArgumentParser(description="Benford's Law analyzer")
    p.add_argument("input", help="Numbers (comma-sep) or @filename")
    args = p.parse_args()
    inp = args.input
    if inp.startswith("@"):
        with open(inp[1:]) as f: inp = f.read()
    numbers = re.findall(r"-?\d+\.?\d*", inp)
    print(json.dumps(analyze(numbers), indent=2))

if __name__ == "__main__": main()
