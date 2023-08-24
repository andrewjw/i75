#!/usr/bin/env micropython
# interstate75-wrapper
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
from typing import Tuple

import pygame

from .pen import Pen, RGB888Pen

LED_SIZE = 10


class PyGameGraphics:
    def __init__(self, width: int, height: int, rotate: int = 0):
        pygame.init()
        self.width = width
        self.height = height
        self.rotate = rotate
        self.screen = \
            pygame.display.set_mode((width * LED_SIZE, height * LED_SIZE))
        self.pen: Pen = RGB888Pen(0, 0, 0)

    def create_pen(self, r: int, g: int, b: int) -> Pen:
        return RGB888Pen(r, g, b)

    def set_pen(self, pen: Pen) -> None:
        self.pen = pen

    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        llen = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dx = (x2 - x1) / llen
        dy = (y2 - y1) / llen

        x: float = x1
        y: float = y1
        last_coord = (x1, y1)
        self.pixel(x1, y1)
        for _ in range(math.floor(llen)):
            x, y = x + dx, y + dy
            px, py = math.floor(x), math.floor(y)
            if last_coord != (px, py):
                last_coord = (px, py)
                self.pixel(px, py)

    def pixel(self, x: int, y: int) -> None:
        centre = self._rotate_point(math.floor(x * LED_SIZE + LED_SIZE/2),
                                    math.floor(y * LED_SIZE + LED_SIZE/2))
        pygame.draw.circle(self.screen,
                           self.pen.as_tuple(),
                           centre,
                           LED_SIZE/2)

    def _rotate_point(self, x: int, y: int) -> Tuple[int, int]:
        if self.rotate == 0:
            return (x, y)
        elif self.rotate == 90:
            return (y, self.width - x)
        elif self.rotate == 180:
            return (self.width - x, self.height - y)
        else:
            return (self.height - y, x)
