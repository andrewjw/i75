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

from i75 import Colour, Face, Font, I75, ScreenManager
from i75.text import text_boundingbox, render_text, \
                     render_text_multiline, wrap_text
from i75.screens.layers import Layers
from i75.screens.offset import Offset
from i75.screens.single_colour import SingleColour
from i75.screens.horizontal_scrolling_screen import HorizontalScrollingScreen
from i75.screens.single_bit_screen import SingleBitScreen
from i75.screens.vertical_scrolling_screen import VerticalScrollingScreen

DURATION = 2000

HTEXT = \
    "This is some scrolling text. Look how long this line is! Woah! So long!"

VTEXT = """This is too long.
Seriously, too many lines.
What's down here?
Really, this far down?
1.
2.
3.
4.
5.
A list? How dull!"""

FONT = "tiny5.af"


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    face = Face.load_face(FONT)
    font = Font(face, 7)

    white = Colour.fromrgb(255, 255, 255)
    black = Colour.fromrgb(0, 0, 0)

    manager = ScreenManager(64, 64, i75.display)

    bg = SingleColour(black)

    bbox_width, bbox_height = text_boundingbox(font, HTEXT)
    hscreen = SingleBitScreen(bbox_width, bbox_height, white)
    render_text(hscreen, font, 0, 0, HTEXT)
    hscroller = HorizontalScrollingScreen(64,
                                          bbox_height,
                                          hscreen,
                                          bbox_width,
                                          scroll_duration=10000)

    vtext = wrap_text(font, VTEXT, 64)
    bbox_width, bbox_height = text_boundingbox(font, vtext)
    vscreen = SingleBitScreen(bbox_width, bbox_height, white)
    render_text_multiline(vscreen, font, 0, 0, vtext)
    vscroller = VerticalScrollingScreen(bbox_width,
                                        12,
                                        vscreen,
                                        bbox_height,
                                        scroll_duration=10000)
    vscroller_offset = Offset(0, 20, vscroller)

    manager.set_screen(Layers(black, [hscroller, vscroller_offset]))

    base_ticks = i75.ticks_ms()
    while True:
        now = i75.ticks_ms()
        frame_time = i75.ticks_diff(now, base_ticks)
        base_ticks = now

        manager.update(frame_time)

        if hscroller.is_complete():
            hscroller.reset()
        if vscroller.is_complete():
            vscroller.reset()


if __name__ == "__main__":
    main()
