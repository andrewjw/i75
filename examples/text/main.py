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

from i75 import Colour, I75, Face, Font, ScreenManager, \
                render_text, wrap_text, text_boundingbox
from i75.screens.single_colour import SingleColour
from i75.screens.single_bit_screen import SingleBitScreen

PANGRAM = "The Quick Brown Fox Jumps Over The Lazy Dog.".upper()

FONT = "tiny5.af"


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    face = Face.load_face(FONT)
    font = Font(face, 7)

    white = Colour.fromrgb(255, 255, 255)

    manager = ScreenManager(64, 64, i75.display)

    screen = SingleBitScreen(64, 64, white)
    manager.set_screen(screen)

    _, height = text_boundingbox(font, PANGRAM)
    render_text(screen, font, 0, 0, PANGRAM)

    pangram_wrapped = wrap_text(font, PANGRAM, 64)
    _, height2 = text_boundingbox(font, pangram_wrapped)
    render_text(screen, font, 0, height + 1, pangram_wrapped)

    render_text(screen, font, 0, height + height2 + 2, "£")

    manager.update(0)

    i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
