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
    # noinspection PyStatementEffect
    _os.getrandom

except AttributeError:
    pass

else:
    class URandom(_random.Random):

        _GETRANDOM_FLAGS = 0

        def __init__(self, x=None) -> None:
            super().__init__(x)
            self._entropy = 0
            self._entropy_bits = 0

        def random(self) -> float:
            return self.getrandbits(_random.BPF) * _random.RECIP_BPF

        def getrandbits(self, k: int) -> int:
            assert k > 0

            missing_bytes = (k - self._entropy_bits + 7) // 8
            while missing_bytes > 0:
                random_bytes = _os.getrandom(missing_bytes,
                                             flags=self._GETRANDOM_FLAGS)
                random_bytes_count = len(random_bytes)
                self._entropy |= (int.from_bytes(random_bytes, 'little') <<
                                  self._entropy_bits)
                self._entropy_bits += random_bytes_count * 8
                missing_bytes -= random_bytes_count

            result = self._entropy & ((1 << k) - 1)
            self._entropy >>= k
            self._entropy_bits -= k
            return result

        # noinspection PyMethodOverriding
        def _randbelow(self, n: int) -> int:
            assert n > 0

            if n == 1:
                return 0

            k = (n - 1).bit_length()
            r = self.getrandbits(k)
            while r >= n:
                r = self.getrandbits(k)

            return r

        def seed(self, *args, **kwargs) -> None:
            pass

        def getstate(self) -> _Any:
            raise NotImplementedError

        def setstate(self, state: _Any) -> None:
            raise NotImplementedError

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

    try:
        # noinspection PyStatementEffect
        _os.GRND_RANDOM

    except AttributeError:
        pass

    else:
        # noinspection PyAbstractClass
        class Random(URandom):

            _GETRANDOM_FLAGS = _os.GRND_RANDOM

        PROVIDERS += [
            _Provider(
                    precedence=99,
                    name='random',
                    cls=Random,
                    flags=(
                            Flag.NONDETERMINISTIC |
                            Flag.CRYPTOGRAPHICALLY_SECURE |
                            Flag.CRYPTOGRAPHICALLY_STRONG
                    ),
            ),
        ]


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
