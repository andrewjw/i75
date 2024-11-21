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

from i75 import I75, render_text, wrap_text, text_boundingbox

FONT = "cg_pixel_3x5_5"


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    white = i75.display.create_pen(255, 255, 255)
    i75.display.set_pen(white)

    y = 0
    for scale in range(1, 4):
        _, height = text_boundingbox(FONT, f"Scale x{scale}", scale=scale)
        render_text(i75.display, FONT, 0, y, f"Scale x{scale}", scale=scale)
        y += height

    i75.display.update()

    i75.sleep_ms(10000)


if __name__ == "__main__":
    main()
