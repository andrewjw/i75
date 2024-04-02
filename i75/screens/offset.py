#!/usr/bin/env micropython
# i75
# Copyright (C) 2024 Andrew Wilkinson
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
    from typing import Callable
except ImportError:
    pass

from ..colour import Colour
from .screen import Screen


class Offset(Screen):
    def __init__(self,
                 dx: int,
                 dy: int,
                 base: Screen) -> None:
        self.dx = dx
        self.dy = dy
        self.base = base

    def get_pixel(self, x: int, y: int) -> Colour:
        return self.base.get_pixel(x - self.dx, y - self.dy)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def shift_dirty(x: int, y: int) -> None:
            mark_dirty(x + self.dx,
                       y + self.dy)
        self.base.update(frame_time, shift_dirty)
