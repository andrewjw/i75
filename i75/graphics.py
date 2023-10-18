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
    from typing import Optional, Tuple
except ImportError:
    pass
import math

import picographics
import hub75


class Graphics:
    def __init__(self,
                 display_type: picographics.DisplayType,
                 rotate: Optional[int] = 0,
                 panel_type: hub75.PanelType = hub75.PANEL_GENERIC,
                 stb_invert: bool = False,
                 color_order: hub75.ColorOrder
                 = hub75.COLOR_ORDER_RGB) -> None:
        self._driver = picographics.PicoGraphics(display_type)
        self.rotate = rotate

        width, height = self._driver.get_bounds()
        self.hub75 = hub75.Hub75(width,
                                 height,
                                 panel_type=panel_type,
                                 stb_invert=stb_invert,
                                 color_order=color_order)
        self.hub75.start()

    def create_pen(self, r: int, g: int, b: int) -> picographics.Pen:
        return self._driver.create_pen(r, g, b)

    def set_pen(self, pen: picographics.Pen) -> None:
        self._driver.set_pen(pen)

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        # While picographics has a line function, it doesn't include
        # the second point when drawing.

        if x1 == x2:
            for y in range(y1 if y1 < y2 else y2, (y2 if y1 < y2 else y1)+1):
                self.pixel(x1, y)
            return
        if y1 == y2:
            for x in range(x1 if x1 < x2 else x2, (x2 if x1 < x2 else x1)+1):
                self.pixel(x, y1)
            return

        # This is Bresenham's Algorithm
        x, y = x1, y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        pixel = self.pixel
        if (dy / float(dx)) > 1:
            dx, dy = dy, dx
            x, y = y, x
            x1, y1, x2, y2 = y1, x1, y2, x2
            pixel = self.__pixel_reverse

        p = 2*dy - dx

        pixel(x, y)

        for _ in range(2, dx + 2):
            if p > 0:
                y = y + 1 if y < y2 else y - 1
                p = p + 2 * (dy - dx)
            else:
                p = p + 2 * dy

            x = x + 1 if x < x2 else x - 1

            pixel(x, y)

    def circle(self, cx: int, cy: int, radius: int) -> None:
        d = 3 - 2 * radius
        y = radius
        i = 0
        while i <= y:
            self.line(cx + i, cy + y, cx + i, cy - y)
            self.line(cx - i, cy + y, cx - i, cy - y)
            self.line(cx + y, cy + i, cx + y, cy - i)
            self.line(cx - y, cy - i, cx - y, cy + i)

            if d < 0:
                d = d + 4 * i + 6
            else:
                d = d + 4 * (i - y) + 10
                y = y - 1
            i = i + 1

    def pixel(self, x: int, y: int) -> None:
        if x >= 0 and x < 64 and y >= 0 and y < 64:
            self._driver.pixel(x, y)

    def __pixel_reverse(self, x: int, y: int) -> None:
        if x >= 0 and x < 64 and y >= 0 and y < 64:
            self._driver.pixel(y, x)

    def update(self) -> None:
        self.hub75.update(self._driver)

    def get_bounds(self) -> Tuple[int, int]:
        return self._driver.get_bounds()
