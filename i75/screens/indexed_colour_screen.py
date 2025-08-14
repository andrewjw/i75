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
    from typing import Callable, Dict, List, Tuple
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour, TRANSPARENT
from .single_bit_buffer import SingleBitBuffer
from .writable_screen import WritableScreen

CACHE = {}


class IndexedColourScreen(WritableScreen):
    def __init__(self,
                 width: int,
                 height: int,
                 colourmap: Dict[int, Colour],
                 data: bytearray,
                 dataview: memoryview,
                 _cache: bool = False) -> None:
        self.released = False
        assert _cache, "IndexedColourScreen must be created by calling get."
        self._width = width
        self._height = height
        self._colourmap = colourmap
        self._data = data
        self._dataview = dataview
        self._dirty: SingleBitBuffer = SingleBitBuffer.get(width, height)

    def __del__(self):
        if not self.released:
            print("Error! Unreleased IndexedColourScreen",
                  self._width,
                  self._height)

    def release(self):
        if (self._width, self._height) not in CACHE:
            CACHE[(self._width, self._height)] = collections.deque([], 5)
        CACHE[(self._width, self._height)].append((self._data, self._dataview))
        self._dirty.release()
        self.released = True

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < 0 \
           or y < 0 \
           or x >= self._width \
           or y >= self._height:
            return TRANSPARENT

        c = self._dataview[self.__get_index(x, y)]
        if c == 0:
            return TRANSPARENT
        else:
            return self._colourmap.get(c, TRANSPARENT)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def hidden_mark_dirty(x: int, y: int) -> None:
            c = self._dataview[self.__get_index(x, y)]
            if c == 0:
                mark_dirty(x, y)
        super().update(frame_time, hidden_mark_dirty)

        for (dx, dy) in self._dirty.set_pixels():
            mark_dirty(dx, dy)
        self._dirty.reset()

    def fill(self, colour: int, mark_dirty: bool = True) -> None:
        for idx in range(self._width * self._height):
            self._dataview[idx] = colour
        if mark_dirty:
            self._dirty.set_all()

    def set_pixel(self, x: int, y: int, colour: int) -> None:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return
        self._dataview[self.__get_index(x, y)] = colour
        self._dirty.set_pixel(x, y)

    def __get_index(self, x: int, y: int) -> int:
        return self._width * y + x

    @staticmethod
    def get(width, height, colourmap):
        if (width, height) not in CACHE or len(CACHE[(width, height)]) == 0:
            data = bytearray(width*height)
            return IndexedColourScreen(width,
                                       height,
                                       colourmap,
                                       data,
                                       memoryview(data),
                                       True)
        else:
            data, view = CACHE[(width, height)].pop()
            return IndexedColourScreen(width,
                                       height,
                                       colourmap,
                                       data,
                                       view,
                                       True)
