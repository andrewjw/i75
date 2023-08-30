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

try:  # pragma: no cover
    import picographics as pg  # type: ignore
    DISPLAY_INTERSTATE75_64X64 = pg.DISPLAY_INTERSTATE75_64X64
except ImportError:
    from typing import Any, Optional
    DISPLAY_INTERSTATE75_64X64 = None


class DisplayType:
    def __init__(self,
                 width: int,
                 height: int,
                 i75type: Optional[Any] = None) -> None:
        self.width = width
        self.height = height
        self.i75type = i75type


DISPLAY_INTERSTATE75_64X64 = DisplayType(64,
                                         64,
                                         DISPLAY_INTERSTATE75_64X64)
