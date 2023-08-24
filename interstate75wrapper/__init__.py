#!/usr/bin/env micropython
# interstate75-wrapper
# Copyright (C) 2023 Andrew Wilkinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.2.0"

from .datetime import DateTime
from .display_type import DisplayType
from .pen import Pen

try:
    import picographics  # type: ignore
except ImportError:
    from .mockinterstate75 import MockInterstate75
    Interstate75Wrapper = MockInterstate75  # type: ignore
else:
    from .nativeinterstate75 import NativeInterstate75
    Interstate75Wrapper = NativeInterstate75  # type: ignore
