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

from i75 import Colour, I75, ScreenManager
from i75.screens import ColourBlock, ScreenWipe, SwipeDown, \
                        SwipeLeft, SwipeRight, SwipeUp

DURATION = 2000


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    blue = Colour.fromrgb(0, 0, 255)
    red = Colour.fromrgb(255, 0, 0)
    yellow = Colour.fromrgb(255, 255, 0)
    green = Colour.fromrgb(0, 255, 0)

    manager = ScreenManager(64, 64, i75.display)

    blue_block = ColourBlock(0, 0, 64, 64, blue)
    red_block = ColourBlock(0, 0, 64, 64, red)
    yellow_block = ColourBlock(0, 0, 64, 64, yellow)
    green_block = ColourBlock(0, 0, 64, 64, green)

    swipe: ScreenWipe = SwipeRight(64, 64, DURATION, blue_block, red_block)

    manager.set_screen(swipe)

    base_ticks = i75.ticks_ms()
    while True:
        now = i75.ticks_ms()
        frame_time = i75.ticks_diff(now, base_ticks)
        base_ticks = now

        manager.update(frame_time)

        if swipe.is_complete():
            i75.sleep_ms(500)
            base_ticks = i75.ticks_ms()
            if isinstance(swipe, SwipeRight):
                swipe = SwipeUp(64, 64, DURATION, red_block, yellow_block)
            elif isinstance(swipe, SwipeUp):
                swipe = SwipeLeft(64, 64, DURATION, yellow_block, green_block)
            elif isinstance(swipe, SwipeLeft):
                swipe = SwipeDown(64, 64, DURATION, green_block, blue_block)
            else:
                swipe = SwipeRight(64, 64, DURATION, blue_block, red_block)
            manager.set_screen(swipe, False)


if __name__ == "__main__":
    main()
