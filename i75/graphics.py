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

class Graphics:
    def create_pen(self, r: int, g: int, b: int) -> picographics.Pen:
        raise NotImplementedError()

    def set_pen(self, pen: picographics.Pen) -> None:
        raise NotImplementedError()

    def line(self, x1: int, y1: int, x2: int, y2: int) -> None:
        raise NotImplementedError()

    def circle(self, cx: int, cy: int, radius: int) -> None:
        raise NotImplementedError()

    def fill(self, tl_x: int, tl_y: int, br_x: int, br_y: int) -> None:
        raise NotImplementedError()

    def clear(self) -> None:
        raise NotImplementedError()

    def pixel(self, x: int, y: int) -> None:
        raise NotImplementedError()

    def update(self) -> None:
        raise NotImplementedError()

    def get_bounds(self) -> Tuple[int, int]:
        raise NotImplementedError()
