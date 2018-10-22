#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any as _Any

import enum as _enum
import os as _os
import random as _random

from collections import namedtuple as _namedtuple


class Flag(_enum.Flag):
    FULLY_DETERMINISTIC = PSEUDORANDOM = PSEUDO_RANDOM = PRNG = _enum.auto()
    NONDETERMINISTIC = NON_DETERMINISTIC = TRULY_RANDOM = TRNG = _enum.auto()
    NEVER_BLOCKING = NONBLOCKING = NON_BLOCKING = _enum.auto()
    CLONEABLE = FORKABLE = RESTORABLE = SNAPSHOTTABLE = STATEFUL = _enum.auto()
    SEEDABLE = _enum.auto()
    FAST = QUICK = _enum.auto()
    CRYPTOGRAPHICALLY_SECURE = _enum.auto()
    CRYPTOGRAPHICALLY_STRONG = _enum.auto()
    PROTECTED_MEMORY = _enum.auto()
    THREADSAFE = _enum.auto()


_Provider = _namedtuple('Provider', ['precedence', 'name', 'cls', 'flags'])

PROVIDERS = [
    _Provider(
            precedence=-11,
            name='mersenne_twister',
            cls=_random.Random,
            flags=(
                    Flag.FULLY_DETERMINISTIC |
                    Flag.NEVER_BLOCKING |
                    Flag.CLONEABLE |
                    Flag.SEEDABLE |
                    Flag.FAST
            ),
    ),
    _Provider(
            precedence=9,
            name='system',
            cls=_random.SystemRandom,
            flags=Flag(0),
    ),
]


__all__ = [
    'Flag',
    'PROVIDERS',
]


try:
    from .getrandom import URandom

except ImportError:
    pass

else:
    PROVIDERS += [
        _Provider(
                precedence=49,
                name='urandom',
                cls=URandom,
                flags=(
                        Flag.CRYPTOGRAPHICALLY_SECURE
                ),
        ),
    ]

    __all__ += ['URandom']


try:
    from .getrandom import DevRandom

except ImportError:
    pass

else:
    PROVIDERS += [
        _Provider(
                precedence=99,
                name='dev_random',
                cls=DevRandom,
                flags=(
                        Flag.NONDETERMINISTIC |
                        Flag.CRYPTOGRAPHICALLY_SECURE |
                        Flag.CRYPTOGRAPHICALLY_STRONG
                ),
        ),
    ]

    __all__ += ['DevRandom']


try:
    from .rdrandseed import RdRand

except ImportError:
    pass

else:
    PROVIDERS += [_Provider(
            precedence=19,
            name='rdrand',
            cls=RdRand,
            flags=(
                    Flag.NEVER_BLOCKING |
                    Flag.FAST |
                    Flag.CRYPTOGRAPHICALLY_SECURE
            ),
    )]

    __all__ += ['RdRand']


try:
    from .rdrandseed import RdSeed

except ImportError:
    pass

else:
    PROVIDERS += [_Provider(
            precedence=69,
            name='rdseed',
            cls=RdSeed,
            flags=(
                    Flag.NONDETERMINISTIC |
                    Flag.NEVER_BLOCKING |
                    Flag.CRYPTOGRAPHICALLY_SECURE |
                    Flag.CRYPTOGRAPHICALLY_STRONG
            ),
    )]

    __all__ += ['RdSeed']


PROVIDERS.sort(reverse=True)
