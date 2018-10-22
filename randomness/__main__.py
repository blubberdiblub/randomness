#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterable as _Iterable

from .provider import PROVIDERS, _Provider


def _test(providers: _Iterable[_Provider]) -> None:
    import sys

    for provider in providers:
        print(f"\n{provider.name}:\n", file=sys.stderr, flush=True)

        random = provider.cls()

        for expression in [
            'random.getrandbits(4096).bit_length()',
            'random.random()',
            'random.randint(-15, -1)',
            'random.randrange(16)',
            'random.randint(16, 32)',
        ]:
            print(f"{expression} = {eval(expression)!r}",
                  file=sys.stderr, flush=True)


_test(PROVIDERS)
