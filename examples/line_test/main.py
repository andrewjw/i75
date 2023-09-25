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

import picographics

from i75 import I75


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    white = i75.display.create_pen(255, 255, 255)
    red = i75.display.create_pen(255, 0, 0)
    green = i75.display.create_pen(0, 255, 0)
    blue = i75.display.create_pen(0, 0, 255)
    purple = i75.display.create_pen(255, 0, 255)

    i75.display.set_pen(red)
    i75.display.line(63, 0, 0, 0)
    i75.display.line(0, 63, 63, 63)

    i75.display.set_pen(green)
    i75.display.line(1, 1, 1, 62)

    i75.display.set_pen(blue)
    i75.display.line(62, 62, 62, 1)

    i75.display.set_pen(purple)
    i75.display.line(25, 45, 45, 25)
    i75.display.line(25, 25, 45, 45)

    i75.display.set_pen(white)
    i75.display.line(25, 10, 35, 15)
    i75.display.line(20, 10, 30, 25)
    i75.display.line(15, 10, 25, 35)
    i75.display.line(10, 10, 20, 45)

    i75.display.line(36, 10, 36, 12)
    i75.display.line(35, 10, 35, 11)
    i75.display.line(37, 10, 37, 13)
    i75.display.line(38, 10, 38, 14)
    i75.display.line(39, 10, 39, 15)

    i75.display.update()

    while True:
        i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
