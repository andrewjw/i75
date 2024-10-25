#!/usr/bin/env micropython
# i75
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

__version__ = "1.11.1"

import picographics
if hasattr(picographics, "DisplayType"):
    from .emulatedi75 import EmulatedI75
    I75 = EmulatedI75  # type: ignore
else:
    from .nativei75 import NativeI75
    I75 = NativeI75  # type: ignore
del picographics

from .colour import Colour  # noqa
from .datetime import DateTime  # noqa
from .image import Image  # noqa
from .text import render_text, text_boundingbox, wrap_text  # noqa
