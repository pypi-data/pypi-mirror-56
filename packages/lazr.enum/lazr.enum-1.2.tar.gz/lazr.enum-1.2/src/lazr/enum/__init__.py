# Copyright 2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.enum
#
# lazr.enum is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.enum is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.enum.  If not, see <http://www.gnu.org/licenses/>.
"""Enumerations."""

import pkg_resources
__version__ = pkg_resources.resource_string(
    "lazr.enum", "version.txt").strip()

# While we generally frown on "*" imports, this, combined with the fact we
# only test code from this module, means that we can verify what has been
# exported.
from lazr.enum._enum import *
from lazr.enum._enum import __all__ as _all
from lazr.enum._json import *
from lazr.enum._json import __all__ as _jall
from lazr.enum.interfaces import *
from lazr.enum.interfaces import __all__ as _iall
__all__ = []
__all__.extend(_all)
__all__.extend(_iall)
__all__.extend(_jall)
