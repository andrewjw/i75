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

from ..colour import Colour, TRANSPARENT
from .screen import Screen


class ColourBlock(Screen):
    def __init__(self,
                 width: int,
                 height: int,
                 colour: Colour) -> None:
        self.width = width
        self.height = height
        self.colour = colour

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return TRANSPARENT

        return self.colour
