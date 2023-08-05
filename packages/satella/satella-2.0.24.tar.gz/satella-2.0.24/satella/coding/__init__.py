# coding=UTF-8
"""
Just useful objects to make your coding nicer every day
"""
from __future__ import print_function, absolute_import, division

from .algos import merge_dicts
from .concurrent import Monitor, RMonitor, CallableGroup, LockedDataset
from .recast_exceptions import rethrow_as, silence_excs
from .structures import TimeBasedHeap, Heap, typednamedtuple, OmniHashableMixin
from .structures import TimeBasedHeap, Heap, typednamedtuple, OmniHashableMixin, Singleton
from .typecheck import typed, Callable, Sequence, \
    TypeVar, Mapping, Iterable, Any, Optional, CallSignature, \
    Number, coerce, Set, Dict, List, Tuple, checked_coerce, for_argument, \
    precondition, PreconditionError
from .decorators import treat_result_with
from .fun_static import static_var

__all__ = [
    'typednamedtuple', 'OmniHashableMixin'
                       'TimeBasedHeap', 'Heap', 'CallableGroup',
    'Monitor', 'RMonitor', 'CallableGroup', 'LockedDataset', 'merge_dicts',
    'typed', 'NewType', 'Callable', 'Sequence', 'coerce'
                                                'TypeVar', 'Mapping', 'Iterable', 'Union', 'Any',
    'Optional',
    'CallSignature', 'Number',
    'Set', 'Dict', 'List', 'Tuple', 'checked_coerce', 'for_argument',
    'precondition', 'PreconditionError',
    'rethrow_as', 'silence_excs',
    'Singleton',
    'treat_result_with',
    'static_var'
]
