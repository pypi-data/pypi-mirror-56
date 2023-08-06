# -*- coding: utf-8 -*-
"""
Main module of the icet package.
"""

from __future__ import print_function, division

from .core.cluster_space import ClusterSpace, get_singlet_info, view_singlets
from .core.cluster_expansion import ClusterExpansion
from .core.orbit_list import OrbitList
from .core.structure import Structure
from .core.structure_container import StructureContainer
from .fitting import (Optimizer,
                      EnsembleOptimizer,
                      CrossValidationEstimator)

__project__ = 'icet'
__description__ = 'A Pythonic approach to cluster expansions'
__authors__ = ['Mattias Ångqvist',
               'William A. Muñoz',
               'J. Magnus Rahm',
               'Erik Fransson',
               'Céline Durniak',
               'Piotr Rozyczko',
               'Thomas Holm Rod',
               'Paul Erhart']
__copyright__ = '2019'
__license__ = 'Mozilla Public License 2.0 (MPL 2.0)'
__version__ = '1.1-r1'
__maintainer__ = 'The icet developers team'
__email__ = 'icet@materialsmodeling.org'
__status__ = 'Stable'
__url__ = 'http://icet.materialsmodeling.org/'

__all__ = ['ClusterSpace',
           'ClusterExpansion',
           'Structure',
           'OrbitList',
           'StructureContainer',
           'Optimizer',
           'EnsembleOptimizer',
           'CrossValidationEstimator',
           'get_singlet_info',
           'view_singlets']
