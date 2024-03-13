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
from typing import List, Optional, Tuple

from pen import Pen, RGB888Pen


class DisplayType:
    def __init__(self, width: int, height: int,) -> None:
        self.width = width
        self.height = height


DISPLAY_INTERSTATE75_64X64 = DisplayType(64, 64)


class PicoGraphics:
    def __init__(self, display_type: DisplayType):
        self.display_type = display_type
        self.pen = self.create_pen(0, 0, 0)

        self._buffer: List[List[Optional[Tuple[int, int, int]]]] = []
        for _ in range(self.display_type.height):
            self._buffer.append([None] * self.display_type.width)

    def create_pen(self, r: int, g: int, b: int) -> Pen:
        return RGB888Pen(r, g, b)

    def set_pen(self, pen: Pen) -> None:
        self.pen = pen

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        # This doesn't properly replicate picographs.
        # It seems to sort the two points, and then doesn't
        # include the second point when drawing the line.
        llen = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dx = (x2 - x1) / llen
        dy = (y2 - y1) / llen

        x: float = x1
        y: float = y1
        last_coord = (x1, y1)
        self.pixel(x1, y1)
        for _ in range(math.floor(llen) - 1):
            x, y = x + dx, y + dy
            px, py = math.floor(x), math.floor(y)
            if last_coord != (px, py):
                last_coord = (px, py)
                self.pixel(px, py)

    def pixel(self, x: int, y: int) -> None:
        self._buffer[y][x] = self.pen.as_tuple()

    def get_bounds(self) -> Tuple[int, int]:
        return (self.display_type.width, self.display_type.height)
