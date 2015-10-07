#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**Prerequisites**

- numpy >= 1.6.1
- scipy >= 0.9
- sklearn >= 0.14.1
- pandas >= 0.14.1
"""

from .core import psm
from .dataset import load_re78

__version__ = "0.0.3"
__short_description__ = ("Treatment group, control group matching algorithm "
                         "high level python implementation.")
