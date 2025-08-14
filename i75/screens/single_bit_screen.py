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
    from typing import Any, Callable, Optional, List, Tuple
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour, TRANSPARENT
from .single_bit_buffer import SingleBitBuffer
from .writable_screen import WritableScreen


class SingleBitScreen(WritableScreen):
    def __init__(self,
                 width: int,
                 height: int,
                 colour: Optional[Colour] = None) -> None:
        self._width = width
        self._height = height
        self._colour = colour if colour is not None \
            else Colour.fromrgb(255, 255, 255)
        self._data = SingleBitBuffer.get(width, height)
        self._dirty = SingleBitBuffer.get(width, height)

    def release(self):
        self._data.release()
        self._dirty.release()

    def set_colour(self, colour: Colour) -> None:
        if colour == self._colour:
            return
        self._colour = colour
        for x, y in self._data.set_pixels():
            self._dirty.set_pixel(x, y)

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return TRANSPARENT

        return self._colour if \
            self._data.is_pixel_set(x, y) \
            else TRANSPARENT

    def fill(self, colour: bool, mark_dirty: bool = True) -> None:
        if colour:
            self._data.set_all()
        else:
            self._data.reset()
        if mark_dirty:
            self._dirty.set_all()

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        for (dx, dy) in self._dirty.set_pixels():
            mark_dirty(dx, dy)
        self._dirty.reset()

    def set_pixel(self, x: int, y: int, *colour: bool) -> None:
        if x < 0 or x > self._width or y < 0 or y > self._height:
            return
        if len(colour) == 0:
            colour = (True, )
        if self._data.is_pixel_set(x, y) == colour[0]:
            return
        if colour[0]:
            self._data.set_pixel(x, y)
        else:
            self._data.clear_pixel(x, y)
        self._dirty.set_pixel(x, y)

    def is_pixel_set(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return False
        return self._data.is_pixel_set(x, y)
