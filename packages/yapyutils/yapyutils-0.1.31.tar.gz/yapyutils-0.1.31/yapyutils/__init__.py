# -*- coding: utf-8 -*-
"""*yapyutils* provides various low-level *Python* utilities for installation and bootstrap stages,
thus the implementation is kept independent from higher stack-layers when ever possible.
Ultimately features are provided redundant in favor of independence.

The subpackage layout prioritizes modularity and granularity, eventually at the cost of
minor performance reduction.

The absolute and overall priority is the avoidance of circular dependencies.
"""

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2019 Arno-Can Uestuensoez" \
                " @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.1'
__uuid__ = "60cac28d-efe6-4a8d-802f-fa4fc94fa741"

__docformat__ = "restructuredtext en"


_debug = 0
_verbose = 0


class YapyUtilsError(Exception):
    """Subsystem *YapyUtils*.
    """
    pass


