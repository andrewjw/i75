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
    from typing import Callable, List, Tuple
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour
from .screen import Screen
from .single_bit_buffer import SingleBitBuffer
from .writable_screen import WritableScreen


class SingleBitScreen(WritableScreen):
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 width: int,
                 height: int,
                 colour: Colour,
                 child: Screen) -> None:
        super().__init__(child)
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._width = width
        self._height = height
        self._colour = colour
        self._data = SingleBitBuffer(width, height)
        self._dirty: List[Tuple[int, int]] = []

    def get_pixel(self, x: int, y: int) -> Colour:
        assert self._child is not None
        if x < self._offset_x \
           or y < self._offset_y \
           or x >= (self._offset_x + self._width) \
           or y >= (self._offset_y + self._height):
            return self._child.get_pixel(x, y)

        return self._colour if \
            self._data.is_pixel_set(x - self._offset_x, y - self._offset_y) \
            else self._child.get_pixel(x, y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        def hidden_mark_dirty(x: int, y: int) -> None:
            if not self._data.is_pixel_set(x - self._offset_x,
                                           y - self._offset_y):
                mark_dirty(x, y)
        super().update(frame_time, hidden_mark_dirty)

        for (dx, dy) in self._dirty:
            mark_dirty(dx, dy)
        self._dirty.clear()

    def pixel(self, x: int, y: int) -> None:
        if x < 0 or x > self._width or y < 0 or y > self._height:
            return
        self._data.set_pixel(x, y)
        self._dirty.append((x, y))
