#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from scipy.stats import chisquare, power_divergence
from scipy.stats.distributions import chi2
from scipy import special as sc_special


def main():
    expected = np.array([10.0, 40.0, 60.0, 60.0, 25.0, 5.0], dtype=np.float_)
    observed = np.array([11.0, 38.0, 65.0, 59.0, 23.0, 4.0], dtype=np.float_)

    result1 = chisquare(observed, expected)
    result2 = power_divergence(observed, expected, lambda_=1.0)

    print(result1)
    print(result2)

    terms = (observed - expected)**2 / expected
    statistic = np.sum(terms)
    print(statistic)

    pvalue = chi2.sf(statistic, len(observed) - 1)
    print(pvalue)

    pvalue2 = sc_special.chdtrc(len(observed) - 1, statistic)
    print(pvalue2)

    pvalue3 = sc_special.gammaincc((len(observed) - 1) * 0.5, statistic * 0.5)
    print(pvalue3)

    pinv = chi2.cdf(statistic, len(observed) - 1)
    print(pinv)

    pinv2 = sc_special.chdtr(len(observed) - 1, statistic)
    print(pinv2)

    pinv3 = sc_special.gammainc((len(observed) - 1) * 0.5, statistic * 0.5)
    print(pinv3)


if __name__ == '__main__':
    main()
