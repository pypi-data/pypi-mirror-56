# -*- coding: utf-8 -*-
"""
GENO is a solver for non-linear optimization problems.
It can solve constrained and unconstrained problems.
"""
from packaging import version

__version__ = '0.0.2.17'

def check_version(new_version):
    """ Check if GENO solver should be upgraded.
    """
    if version.parse(__version__) < version.parse(new_version):
        print("New version of GENO solver is available. You should consider upgrading via 'pip install --upgrade genosolver'.")
