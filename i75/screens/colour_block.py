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
    from typing import Optional
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour
from .screen import Screen


class ColourBlock(Screen):
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 width: int,
                 height: int,
                 colour: Colour,
                 child: Optional[Screen] = None) -> None:
        super().__init__(child)
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height
        self.colour = colour

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < self.offset_x \
           or y < self.offset_y \
           or x >= (self.offset_x + self.width) \
           or y >= (self.offset_y + self.height):
            assert self._child is not None
            return self._child.get_pixel(x, y)

        return self.colour
