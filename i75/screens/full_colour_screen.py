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

from ..colour import Colour
from .screen import Screen
from .writable_screen import WritableScreen


class FullColourScreen(WritableScreen):
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 width: int,
                 height: int,
                 child: Screen) -> None:
        super().__init__(child)
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._width = width
        self._height = height
        self._data = bytearray(width*height*3)
        self._dirty: List[Tuple[int, int]] = []

    def get_pixel(self, x: int, y: int) -> Colour:
        assert self._child is not None
        if x < self._offset_x \
           or y < self._offset_y \
           or x >= (self._offset_x + self._width) \
           or y >= (self._offset_y + self._height):
            return self._child.get_pixel(x, y)

        return Colour.fromrgb(self._data[self.__get_index(x, y) + 0],
                              self._data[self.__get_index(x, y) + 1],
                              self._data[self.__get_index(x, y) + 2])

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def hidden_mark_dirty(x: int, y: int) -> None:
            if x < self._offset_x \
               or y < self._offset_y \
               or x >= (self._offset_x + self._width) \
               or y >= (self._offset_y + self._height):
                mark_dirty(x, y)
        super().update(frame_time, hidden_mark_dirty)

        for (dx, dy) in self._dirty:
            mark_dirty(dx, dy)
        self._dirty.clear()

    def set_pixel(self, x: int, y: int, *colour: Colour) -> None:
        assert len(colour) == 1 and isinstance(colour[0], Colour)
        if x < 0 or x > self._width or y < 0 or y > self._height:
            return
        self._data[self.__get_index(x, y) + 0] = colour[0].r
        self._data[self.__get_index(x, y) + 1] = colour[0].g
        self._data[self.__get_index(x, y) + 2] = colour[0].b
        self._dirty.append((x, y))

    def __get_index(self, x: int, y: int) -> int:
        return (self._width * (y - self._offset_y) + (x - self._offset_x)) * 3
