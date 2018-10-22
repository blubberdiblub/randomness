#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as _random

from functools import partial as _partial


class JKiss(_random.Random):

    VERSION = 1

    # noinspection PyMissingConstructor
    def __init__(self, a=None, version: int = 2) -> None:

        self._x, self._y, self._z, self._c = None, None, None, None
        self.gauss_next = None

        self.seed(a=a, version=version)

    def seed(self, a=None, version: int = 2):

        super().seed(a=a, version=version)

        self._x = super().getrandbits(32)
        self._y = super().getrandbits(32)
        while self._y == 0:
            self._y = super().getrandbits(32)
        self._z = super().getrandbits(32)
        self._c = (super().getrandbits(32) % 698769068) + 1

        self.gauss_next = None

    def getstate(self):

        return (self.VERSION,
                self._x, self._y, self._z, self._c,
                self.gauss_next)

    def setstate(self, state):

        version, *state = state

        if version != 1:
            raise ValueError(f"state with version {version}"
                             f" passed to {self.__class__.__name__}.setstate()"
                             f" of version {self.VERSION}")

        self._x, self._y, self._z, self._c, self.gauss_next = state

    def get32bits(self):

        self._x = (314527869 * self._x + 1234567) & 0xffffffff
        self._y ^= (self._y << 5) & 0xffffffff
        self._y ^= self._y >> 7
        self._y ^= (self._y << 22) & 0xffffffff
        t = 4294584393 * self._z + self._c
        self._c = t >> 32
        self._z = t & 0xffffffff

        return (self._x + self._y + self._z) & 0xffffffff

    def getrandbits(self, k: int):

        assert k > 0

        result = 0
        while k > 32:
            k -= 32
            result = (result << 32) | self.get32bits()

        return (result << k) | (self.get32bits() & ((1 << k) - 1))

    # noinspection PyMethodOverriding
    def _randbelow(self, n: int):

        assert n > 0

        num_bits = (n - 1).bit_length()
        func = ((lambda mask=(1 << num_bits) - 1: self.get32bits() & mask)
                if num_bits < 32
                else self.get32bits if num_bits == 32
                else _partial(self.getrandbits, num_bits))

        v = func()
        while v >= n:
            v = func()

        return v

    def random(self):

        return self.get32bits() / 0x100000000
