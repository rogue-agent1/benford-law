#!/usr/bin/env python3
"""benford_law - Benford's Law analysis for fraud detection."""
import sys,math,collections
def first_digit(n):
    n=abs(n)
    while n>=10:n/=10
    return int(n)
def benford_expected(d):return math.log10(1+1/d)
def analyze(numbers):
    counts=collections.Counter(first_digit(n) for n in numbers if n!=0)
    total=sum(counts.values());result=[]
    for d in range(1,10):
        obs=counts.get(d,0)/total if total else 0;exp=benford_expected(d)
        result.append({"digit":d,"observed":round(obs,4),"expected":round(exp,4),"deviation":round(abs(obs-exp),4)})
    chi2=sum((r["observed"]-r["expected"])**2/r["expected"] for r in result)
    return result,round(chi2,4)
if __name__=="__main__":
    if len(sys.argv)<2:
        import random;numbers=[random.randint(1,999999) for _ in range(10000)]
        print("Random data (should follow Benford's):")
    else:numbers=[float(x) for x in open(sys.argv[1]).read().split() if x.strip()]
    result,chi2=analyze(numbers)
    print(f"{'Digit':>5} {'Observed':>10} {'Expected':>10} {'Deviation':>10}")
    for r in result:print(f"{r['digit']:>5} {r['observed']:>10.4f} {r['expected']:>10.4f} {r['deviation']:>10.4f}")
    print(f"\nChi-squared: {chi2} {'(suspicious)' if chi2>15.51 else '(normal)'}")
