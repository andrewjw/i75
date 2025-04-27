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

from i75 import Colour, I75, line
from i75.screens.single_colour import SingleColour
from i75.screens.full_colour_screen import FullColourScreen
from i75.screen_manager import ScreenManager


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    manager = ScreenManager(64, 64, i75.display)

    white = Colour.fromrgb(255, 255, 255)
    red = Colour.fromrgb(255, 0, 0)
    green = Colour.fromrgb(0, 255, 0)
    blue = Colour.fromrgb(0, 0, 255)
    purple = Colour.fromrgb(255, 0, 255)

    screen = FullColourScreen(64, 64)
    manager.set_screen(screen)

    line(screen, 63, 0, 0, 0, red)
    line(screen, 0, 63, 63, 63, red)

    line(screen, 1, 1, 1, 62, green)

    line(screen, 62, 62, 62, 1, blue)

    line(screen, 25, 45, 45, 25, purple)
    line(screen, 25, 25, 45, 45, purple)

    line(screen, 25, 10, 35, 15, white)
    line(screen, 20, 10, 30, 25, white)
    line(screen, 15, 10, 25, 35, white)
    line(screen, 10, 10, 20, 45, white)

    line(screen, 36, 10, 36, 12, white)
    line(screen, 35, 10, 35, 11, white)
    line(screen, 37, 10, 37, 13, white)
    line(screen, 38, 10, 38, 14, white)
    line(screen, 39, 10, 39, 15, white)

    manager.update(0)

    while True:
        i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
