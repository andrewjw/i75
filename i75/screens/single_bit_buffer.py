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

import collections
import math

import micropython

from ..profile import profile

CACHE = {}


class SingleBitBuffer:
    """
    Holds a buffer capable of telling if a single pixel is set of not.

    Can be any size, although widths not exactly divisible by 8 have
    some memory wastage, as each row is stored as a byte array.
    """
    def __init__(self, width: int, height: int, _cache: bool = False) -> None:
        self.released = False
        assert _cache, "SingleBitBuffer must be created by calling get."
        self.width = width
        self.height = height
        self._row_width = math.ceil(self.width / 8.0)
        self._is_dirty = False
        self.__data: bytearray = bytearray(self._row_width * self.height)
        self._data_view = memoryview(self.__data)

    def __del__(self):
        if not self.released:
            print("Error! Unreleased SingleBitBuffer", self.width, self.height)

    def release(self):
        if (self.width, self.height) not in CACHE:
            CACHE[(self.width, self.height)] = collections.deque([], 10)
        CACHE[(self.width, self.height)].append(self)
        self.released = True

    @micropython.native
    def set_pixel(self, x: int, y: int) -> None:
        """Set the given pixel."""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        self._is_dirty = True
        byte = self._row_width * y + (x >> 3)
        self._data_view[byte] = self._data_view[byte] | (1 << (x % 8))

    @micropython.native
    def clear_pixel(self, x: int, y: int) -> None:
        """Clear the given pixel."""
        byte = self._row_width * y + (x >> 3)
        self._data_view[byte] = self._data_view[byte] & ~(1 << (x % 8))

    @micropython.native
    def is_pixel_set(self, x: int, y: int) -> bool:
        """Returns true if the given pixel is set."""
        byte = self._row_width * y + (x >> 3)
        return (self._data_view[byte] & (1 << (x % 8))) != 0

    @micropython.native
    def is_pixel_group_set(self, x: int, y: int) -> bool:
        """Returns true if any pixel is a group of 8 is set."""
        byte = self._row_width * y + (x >> 3)
        return self._data_view[byte] != 0

    @micropython.native
    def set_pixels(self):
        for i in range(len(self._data_view)):
            if self._data_view[i] != 0:
                for b in range(8):
                    if (self._data_view[i] & (1 << b)) != 0:
                        yield (i % self._row_width) * 8 + b, \
                              i // self._row_width

    @micropython.native
    def set_pixels_call(self, func):
        for i in range(len(self._data_view)):
            if self._data_view[i] != 0:
                for b in range(8):
                    if (self._data_view[i] & (1 << b)) != 0:
                        func((i % self._row_width) * 8 + b,
                             i // self._row_width)

    @micropython.native
    def set_all(self):
        """
        Marks all bits as set
        """
        for b in range(len(self._data_view)):
            self._data_view[b] = 255
        self._is_dirty = True

    @micropython.native
    def reset(self):
        """
        Marks all bits as unset

        A noop if no bits were set since the last reset.
        """
        if not self._is_dirty:
            return
        for b in range(len(self._data_view)):
            self._data_view[b] = 0
        self._is_dirty = False

    @staticmethod
    def get(width: int, height: int):
        if (width, height) not in CACHE or len(CACHE[(width, height)]) == 0:
            return SingleBitBuffer(width, height, True)
        else:
            return CACHE[(width, height)].pop()
