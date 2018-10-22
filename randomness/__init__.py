#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from ._version import version as __version__

except ImportError:
    __version__ = 'unknown'

from .provider import Flag, PROVIDERS


__all__ = [
    'Flag',
    'PROVIDERS',
]
