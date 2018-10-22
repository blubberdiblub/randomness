#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import rdrand as _rdrand

except ImportError:
    _rdrand = None


if _rdrand is not None and _rdrand.HAS_RAND:
    try:
        from rdrand import RdRandom as RdRand

    except ImportError:
        pass


if _rdrand is not None and _rdrand.HAS_SEED:
    try:
        from rdrand import RdSeedom as RdSeed

    except ImportError:
        pass
