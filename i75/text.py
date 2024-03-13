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

try:
    from typing import Any, Dict, Tuple, cast
except ImportError:
    def cast(x, y):  # type:ignore
        return y

from .graphics import Graphics


class FontData:
    HEIGHT: int
    SPACE_WIDTH: int
    DATA: Dict[str, Tuple[int, bytes]]


def __get_font(font: str) -> FontData:
    globals: Dict[str, Any] = {}
    locals: Dict[str, Any] = {}
    exec(f"import i75.fontdata.{font}", globals, locals)
    return cast(FontData, getattr(locals["i75"].fontdata, font))


def render_text(buffer: Graphics,
                font: str,
                x: int,
                y: int,
                text: str) -> None:
    """
    Render the given text, at location (x,y) using font onto the scren buffer.
    """
    if "\n" in text:
        render_text_multiline(buffer, font, x, y, text)
        return

    font_data = __get_font(font)

    for c in text.upper():
        if c == " ":
            x += font_data.SPACE_WIDTH
            continue
        if c in font_data.DATA:
            width, data = font_data.DATA[c]
        else:
            width, data = font_data.DATA["#"]

        for cy in range(y, y+font_data.HEIGHT):
            row = data[cy-y]
            if row == b'\0':
                continue
            for cx in range(x, x+width):
                if row & 1 == 1:
                    buffer.pixel(cx, cy)
                row = row >> 1
        x += width + 1


def render_text_multiline(buffer: Graphics,
                          font: str,
                          x: int,
                          y: int,
                          textdata: str) -> None:
    font_data = __get_font(font)

    for line in textdata.split("\n"):
        render_text(buffer, font, x, y, line)

        y += font_data.HEIGHT


def text_boundingbox(font: str, text: str) -> Tuple[int, int]:
    """
    Return the width and height of the given text using the given font.
    """
    font_data = __get_font(font)

    width, height = 0, 0
    for line in text.split("\n"):
        line_width = 0
        for c in line.upper():
            if c == " ":
                line_width += font_data.SPACE_WIDTH
                continue
            if c in font_data.DATA:
                cwidth, _ = font_data.DATA[c]
            else:
                cwidth, _ = font_data.DATA["#"]
            line_width += cwidth + 1
        if line_width > width:
            width = line_width
        height += font_data.HEIGHT

    return width, height


def wrap_text(font: str, text: str, max_width: int) -> str:
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
