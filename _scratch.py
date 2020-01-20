#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import sys

from collections import Counter

from scipy.stats import chisquare

from randomness.provider import JKiss


def poisson(k, lam):
    return lam ** k * math.exp(-lam) / math.factorial(k)


def bday(random, m=4096, n=1 << 32, repeat=5000):

    lam = m ** 3 / (4 * n)
    print(lam)
    stats = Counter()

    for __ in range(repeat):

        birthdays = [random.randrange(n) for __ in range(m)]
        birthdays.sort()

        spacings = [a - b for a, b in zip(
            birthdays,
            [birthdays[-1] - n, *birthdays[:-1]]
        )]
        spacings.sort()

        counts = Counter(spacings)
        duplicates = sum(1 for count in counts.values() if count > 1)

        stats[duplicates] += 1

    return stats


def fake(m=2, n=2):

    lam = m ** 3 / (4 * n)
    stats = Counter()

    distribution = [0] * m

    while True:
        birthdays = sorted(distribution)

        spacings = [a - b for a, b in zip(
            birthdays,
            [birthdays[-1] - n, *birthdays[:-1]]
        )]
        spacings.sort()

        counts = Counter(spacings)
        duplicates = sum(1 for count in counts.values() if count > 1)
        # assert duplicates == m - len(set(spacings))

        stats[duplicates] += 1

        for i in range(len(distribution)):
            v = distribution[i] = (distribution[i] + 1) % n
            if v > 0:
                break

        else:
            break

    return lam, stats


def try_combination(m=3, n=6):

    lam, stats = fake(m=m, n=n)

    print(lam)
    print(sorted(stats.items()))

    l = []
    for k in range(128):
        p = poisson(k, lam)
        # print(f"{k:3}: {p:.9f}")
        l += [p]

    print("----------------")
    print(f"     {math.fsum(l):.9f}")
    print()

    for i in range(m):
        print(f"{i:3}: {math.fsum(l[i::m]):.9f}")


def chi_square_pearson():
    expected = np.array([91.6, 366.3, 732.6, 976.8, 976.8,
                         781.5, 521.0, 297.7, 148.9, 66.2,
                         40.7], dtype=np.float_)

    observed = np.array([87, 385, 748, 962, 975,
                         813, 472, 308, 159, 61,
                         30], dtype=np.float_)

    result = chisquare(observed, expected)
    print(result.pvalue)


def main():
    chi_square_pearson()


if __name__ == '__main__':
    main()
