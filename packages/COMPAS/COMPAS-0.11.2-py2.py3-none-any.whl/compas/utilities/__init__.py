"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas.utilities


async
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    await_callback


colors
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    i_to_rgb
    i_to_red
    i_to_green
    i_to_blue
    i_to_white
    i_to_black
    rgb_to_hex
    color_to_colordict
    color_to_rgb


datetime
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    timestamp
    now


itertools
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    take
    tabulate
    tail
    consume
    nth
    all_equal
    quantify
    padnone
    ncycles
    dotproduct
    flatten
    repeatfunc
    pairwise
    window
    roundrobin
    powerset
    unique_justseen
    iter_except
    first_true
    random_permutation
    random_combination
    random_combination_with_replacement


maps
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    geometric_key
    reverse_geometric_key
    geometric_key2
    normalize_values


profiling
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    print_profile


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def valuedict(keys, value, default):
    value = value or default
    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}
    return valuedict


from .animation import *
from .async_ import *
from .coercing import *
from .colors import *
from .datetime_ import *
from .decorators import *
from .descriptors import *
from .encoders import *
from .functions import *
from .itertools_ import *
from .maps import *
from .profiling import *
from .remote import *
from .statistics import *
from .xfunc import *


__all__ = [name for name in dir() if not name.startswith('_')]
