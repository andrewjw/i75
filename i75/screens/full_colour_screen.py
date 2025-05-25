#!/usr/bin/env micropython
# i75
# Copyright (C) 2025 Andrew Wilkinson
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
    from typing import Any, Callable, List, Sequence, Tuple
except ImportError:  # pragma: no cover
    pass
import micropython

from ..colour import Colour, TRANSPARENT
from .single_bit_buffer import SingleBitBuffer
from .writable_screen import WritableScreen
from ..profile import profile


class FullColourScreen(WritableScreen):
    def __init__(self,
                 width: int,
                 height: int) -> None:
        self._width = width
        self._height = height
        self._data = bytearray(width*height*3)
        self._dataview = memoryview(self._data)
        self._dirty = SingleBitBuffer(width, height)

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return TRANSPARENT

        idx = (self._width * y + x) * 3
        return Colour.frombytearray(self._dataview[idx + 0:idx + 3])

    @profile
    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def hidden_mark_dirty(x: int, y: int) -> None:
            if x < 0 or y < 0 or x >= self._width or y >= self._height:
                mark_dirty(x, y)
        super().update(frame_time, hidden_mark_dirty)

        for (dx, dy) in self._dirty.set_pixels():
            mark_dirty(dx, dy)
        self._dirty.reset()

    @micropython.native
    def set_pixel(self, x: int, y: int, *colour: Colour) -> None:
        idx = (self._width * y + x) * 3
        self._data[idx + 0] = colour[0]._rgb[0]
        self._data[idx + 1] = colour[0]._rgb[1]
        self._data[idx + 2] = colour[0]._rgb[2]
        self._dirty.set_pixel(x, y)
