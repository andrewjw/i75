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

import picographics

from i75 import Colour, I75, ScreenManager, filled_polygon
from i75.screens.single_colour import SingleColour
from i75.screens.single_bit_screen import SingleBitScreen


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    black = Colour.fromrgb(0, 0, 0)
    white = Colour.fromrgb(255, 255, 255)

    manager = ScreenManager(64, 64, i75.display)

    bg = SingleColour(black)
    screen = SingleBitScreen(0, 0, 64, 64, white, bg)
    manager.set_screen(screen)

    filled_polygon(screen, [[(2, 2), (6, 2), (6, 6), (2, 6)]])

    filled_polygon(screen, [[(6, 12), (10, 16), (6, 20), (2, 16)]])

    filled_polygon(screen, [[(2, 24), (16, 24), (16, 34), (2, 34)],
                            [(6, 28), (12, 28), (12, 30), (6, 30)]])

    manager.update(0)

    i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
