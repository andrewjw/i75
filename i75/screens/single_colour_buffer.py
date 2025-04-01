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

import math

from ..colour import Colour

class SingleColourBuffer:
    """
    Holds a buffer capable of telling if a single pixel is set of not.

    Can be any size, although widths not exactly divisible by 8 have
    some memory wastage, as each row is stored as a byte array.
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._row_width = math.ceil(self.width / 8.0)
        self._data: bytearray = bytearray(self._row_width * self.height)

    def set_pixel(self, x: int, y: int) -> None:
        """Set the given pixel."""
        byte = self._row_width * y + math.floor(x / 8.0)
        self._data[byte] = self._data[byte] | (1 << (x % 8))

    def clear_pixel(self, x: int, y: int) -> None:
        """Clear the given pixel."""
        byte = self._row_width * y + math.floor(x / 8.0)
        self._data[byte] = self._data[byte] & ~(1 << (x % 8))

    def is_pixel_set(self, x: int, y: int) -> bool:
        """Returns true if the given pixel is set."""
        byte = self._row_width * y + math.floor(x / 8.0)
        return (self._data[byte] & (1 << (x % 8))) != 0
