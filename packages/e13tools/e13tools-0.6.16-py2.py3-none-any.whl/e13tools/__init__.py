# -*- coding: utf-8 -*-

"""
e13Tools
========
Provides a collection of utility functions.
Recommended usage::

    import e13tools as e13

Available modules
-----------------
:mod:`~core`
    Provides a collection of functions that are core to **e13Tools** and are
    imported automatically.

:mod:`~math`
    Provides a collection of functions useful in various mathematical
    calculations and data array manipulations.

:mod:`~pyplot`
    Provides a collection of functions useful in various plotting routines.

:mod:`~sampling`
    Provides a collection of functions and techniques useful in sampling
    problems.

:mod:`~utils`
    Provides several useful utility functions.

"""


# %% IMPORTS AND DECLARATIONS
# Future imports
from __future__ import absolute_import, division, print_function

# Package imports
from warnings import warn as _warn

# e13Tools imports
from .__version__ import __version__
from . import core, math, pyplot, sampling, utils
from .core import *
from .math import *
from .pyplot import *
from .sampling import *
from .utils import *

# All declaration
__all__ = ['math', 'pyplot', 'sampling', 'utils']
__all__.extend(core.__all__)
__all__.extend(math.__all__)
__all__.extend(pyplot.__all__)
__all__.extend(sampling.__all__)
__all__.extend(utils.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
