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

import collections
try:
    from typing import Any, Callable, List, Sequence, Tuple
except ImportError:  # pragma: no cover
    pass
import micropython

from ..colour import Colour, TRANSPARENT
from .single_bit_buffer import SingleBitBuffer
from .writable_screen import WritableScreen
from ..profile import profile


CACHE = {}


class FullColourScreen(WritableScreen):
    def __init__(self,
                 width: int,
                 height: int,
                 data: bytearray,
                 dataview: memoryview,
                 _cache: bool = False) -> None:
        self.released = False
        assert _cache, "FullColourScreen must be created by calling get."
        self._width = width
        self._height = height
        self._data = data
        self._dataview = dataview
        self._dirty = SingleBitBuffer.get(width, height)

    def __del__(self):
        if not self.released:
            print("Error! Unreleased FullColourScreen",
                  self._width,
                  self._height)

    def release(self):
        if (self._width, self._height) not in CACHE:
            CACHE[(self._width, self._height)] = collections.deque([], 2)
        CACHE[(self._width, self._height)].append((self._data, self._dataview))
        self._dirty.release()
        self.released = True

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return TRANSPARENT

        idx = (self._width * y + x) * 3
        return Colour.fromrgb(self._dataview[idx + 0],
                              self._dataview[idx + 1],
                              self._dataview[idx + 2])

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
    def fill(self, colour: Colour, mark_dirty: bool = True) -> None:
        r, g, b = colour._rgb
        for idx in range(0, self._width * self._height * 3, 3):
            self._dataview[idx + 0] = r
            self._dataview[idx + 1] = g
            self._dataview[idx + 2] = b
        if mark_dirty:
            self._dirty.set_all()

    @micropython.native
    def set_pixel(self, x: int, y: int, *colour: Colour) -> None:
        self.set_raw_pixel(x,
                           y,
                           colour[0]._rgb[0],
                           colour[0]._rgb[1],
                           colour[0]._rgb[2])

    @micropython.native
    def set_raw_pixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        idx = (self._width * y + x) * 3
        if idx < 0 or idx >= len(self._data):
            return
        self._dataview[idx + 0] = r
        self._dataview[idx + 1] = g
        self._dataview[idx + 2] = b
        self._dirty.set_pixel(x, y)

    @staticmethod
    def get(width, height):
        if (width, height) not in CACHE or len(CACHE[(width, height)]) == 0:
            data = bytearray(width*height*3)
            return FullColourScreen(width,
                                    height,
                                    data,
                                    memoryview(data),
                                    True)
        else:
            data, view = CACHE[(width, height)].pop()
            return FullColourScreen(width, height, data, view, True)
