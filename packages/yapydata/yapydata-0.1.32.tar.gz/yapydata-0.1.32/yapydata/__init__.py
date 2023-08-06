# -*- coding: utf-8 -*-
"""*YapyData* - Yet Another Python Data - provides various low-level *Python* utilities for the management and processing
of structured data types. The definition, persistence, and the processing is hereby supported
for multiple data definition languages. The current support comprises:

* *JSON*
* *XML*
* *YAML*

In addition the syntaxes defined by the widespread legacy configuration file formats:

* *INI* - multiple variants: *INI*, *INIX*, *CFG*, *CONF*
* *.properties* - the *Java* configuration syntax in *INI* style

The package *YapyData* is member of the *DataFusion* family by providing the basic 
syntaxes and features required for the low-level components of modern software stacks.
This is applicable including for installation utilities, thus is kept independent
from higher stack-layers when ever possible.
Ultimately, when required features are even provided redundant in favor of independence.

The higher application level semantic features such as full validation and standard compliant
processing options such as e.g. RFC-6901 [RFC6901]_ and RFC6902 [RFC6902]_.

The subpackage layout prioritizes modularity and granularity, eventually at the cost of
minor performance reduction.
For specific use-cases of large data alternates with better performance are included,
while the generic cases offer flexibility.   

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


class YapyDataError(Exception):
    """Subsystem *YapyData*.
    """
    pass

class YapyDataTypeError(YapyDataError):
    """Type mismatch, e.g. incompatible, check syntax,
    and refer to *strict* parameters.
    """
    pass

