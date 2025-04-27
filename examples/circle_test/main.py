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

from i75 import Colour, I75, ScreenManager, graphic_primitives
from i75.screens.full_colour_screen import FullColourScreen


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    red = Colour.fromrgb(255, 0, 0)
    green = Colour.fromrgb(0, 255, 0)
    blue = Colour.fromrgb(0, 0, 255)

    screen = FullColourScreen(64, 64)
    manager = ScreenManager(64, 64, i75.display)
    manager.set_screen(screen)

    graphic_primitives.circle(screen, 10, 10, 5, red)

    graphic_primitives.circle(screen, 25, 25, 10, green)

    graphic_primitives.circle(screen, 50, 50, 13, blue)

    manager.update(0)

    while True:
        i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
