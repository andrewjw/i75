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
    from typing import Callable, Dict, List, Tuple
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour, TRANSPARENT
from .screen import Screen
from .writable_screen import WritableScreen


class IndexedColourScreen(WritableScreen):
    def __init__(self,
                 width: int,
                 height: int,
                 colourmap: Dict[int, Colour]) -> None:
        self._width = width
        self._height = height
        self._colourmap = colourmap
        self._data = bytearray(width*height)
        self._dirty: List[Tuple[int, int]] = []

    def get_pixel(self, x: int, y: int) -> Colour:
        assert self._child is not None
        if x < 0 \
           or y < 0 \
           or x >= self._width \
           or y >= self._height:
            return TRANSPARENT

        c = self._data[self.__get_index(x, y)]
        if c == 0:
            return TRANSPARENT
        else:
            return self._colourmap[c]

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def hidden_mark_dirty(x: int, y: int) -> None:
            c = self._data[self.__get_index(x, y)]
            if c == 0:
                mark_dirty(x, y)
        super().update(frame_time, hidden_mark_dirty)

        for (dx, dy) in self._dirty:
            mark_dirty(dx, dy)
        self._dirty.clear()

    def set_pixel(self, x: int, y: int, colour: int) -> None:
        if x < 0 or x > self._width or y < 0 or y > self._height:
            return
        self._data[self.__get_index(x, y)] = colour
        self._dirty.append((x, y))

    def __get_index(self, x: int, y: int) -> int:
        return self.width * (y - self._offset_y) + (x - self._offset_x)
