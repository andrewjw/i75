#!/usr/bin/env python3
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
try:
    from typing import Tuple
except ImportError:
    pass

from .font import Font
from .graphic_primitives import filled_polygon
from .screens.writable_screen import WritableScreen


def render_text(buffer: WritableScreen,
                font: Font,
                x: int,
                y: int,
                text: str) -> None:
    """
    Render the given text, at location (x,y) using font onto the scren buffer.
    """
    if "\n" in text:
        render_text_multiline(buffer, font, x, y, text)
        return

    for c in text:
        if c == " ":
            x += font.space_width
            continue
        glyph = font.get_glyph(ord(c))
        if glyph is None:
            glyph = font.get_glyph(ord("#"))

        assert glyph is not None
        filled_polygon(buffer,
                       [[(x + p.x, y + p.y + font.height)
                         for p in contour]
                        for contour in glyph.contours])

        x += int(round(glyph.advance))


def render_text_multiline(buffer: WritableScreen,
                          font: Font,
                          x: int,
                          y: int,
                          textdata: str) -> None:
    for line in textdata.split("\n"):
        render_text(buffer, font, x, y, line)

        y += int(round(font.get_height())) + 1


def text_boundingbox(font: Font, text: str) -> Tuple[int, int]:
    """
    Return the width and height of the given text using the given font.
    """
    width, height = 0, 0
    for line in text.split("\n"):
        line_width = 0
        for c in line:
            if c == " ":
                line_width += font.space_width
                continue
            glyph = font.get_glyph(ord(c))
            if glyph is not None:
                cwidth = glyph.advance
            else:
                cwidth, _ = font.get_glyph(ord("#")).advance + 1  # type:ignore
            line_width += int(round(cwidth))
        if line_width > width:
            width = line_width
        height += int(round(font.get_height())) + 1

    return width, height


def wrap_text(font: Font, text: str, max_width: int) -> str:
    lines = [text]
    while True:
        split_line = False
        for i in range(len(lines)):
            width = text_boundingbox(font, lines[i])[0]
            if width > max_width and " " in lines[i]:
                split_line = True
                last_word = lines[i].split(" ")[-1]
                lines[i] = " ".join(lines[i].split(" ")[:-1])
                if len(lines) == i + 1:
                    lines.append(last_word)
                else:
                    lines[i + 1] = last_word + " " + lines[i + 1]

        if not split_line:
            break

    return "\n".join(lines)
