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
        self._driver.line(x1, y1, x2, y2)

    def pixel(self, x: int, y: int) -> None:
        self._driver.pixel(x, y)

    def update(self) -> None:
        self.hub75.update(self._driver)

    def get_bounds(self) -> Tuple[int, int]:
        return self._driver.get_bounds()
