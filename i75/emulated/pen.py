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

from typing import Tuple


class Pen:
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
        self._value = r << 24 | g << 16 | b << 8 | a

    @property
    def r(self) -> int:
        return (self._value >> 24) & 255

    @property
    def g(self) -> int:
        return (self._value >> 16) & 255

    @property
    def b(self) -> int:
        return (self._value >> 8) & 255

    @property
    def a(self) -> int:
        return self._value & 255

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)


class RGB332Pen(Pen):
    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__((1 << 3) * round(float(r) / (1 << 3)),
                         (1 << 3) * round(float(g) / (1 << 3)),
                         (1 << 2) * round(float(b) / (1 << 2)))


class RGB888Pen(Pen):
    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__(r, g, b)
