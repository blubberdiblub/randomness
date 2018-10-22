#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any as _Any

import os as _os
import random as _random


try:
    # noinspection PyStatementEffect
    _os.getrandom

except AttributeError:
    pass

else:
    class URandom(_random.Random):

        _os_getrandom = _os.getrandom
        _OS_GETRANDOM_FLAGS = 0

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
                random_bytes = self._os_getrandom(
                        missing_bytes,
                        flags=self._OS_GETRANDOM_FLAGS,
                )
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


    try:
        # noinspection PyStatementEffect
        _os.GRND_RANDOM

    except AttributeError:
        pass

    else:
        # noinspection PyAbstractClass
        class DevRandom(URandom):

            _OS_GETRANDOM_FLAGS = _os.GRND_RANDOM
