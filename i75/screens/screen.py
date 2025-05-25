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

try:
    from typing import Callable, Optional
except ImportError:
    pass

from ..colour import Colour


class Screen:
    def __init__(self, child: Optional["Screen"] = None) -> None:
        self._child: Optional["Screen"] = child

    def get_pixel(self, x: int, y: int) -> Colour:
        raise NotImplementedError()

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        if self._child is not None:
            self._child.update(frame_time, mark_dirty)
