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
    from typing import Any, Callable, Dict, Tuple, cast
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


def __scale_pixel(scale: int,
                  pixel: Callable[[int, int], None]) \
        -> Callable[[int, int, int, int], None]:
    def r(x: int, y: int, cx: int, cy: int) -> None:
        for sx in range(scale):
            for sy in range(scale):
                pixel(x + cx * scale + sx, y + cy * scale + sy)
    return r


def render_text(buffer: Graphics,
                font: str,
                x: int,
                y: int,
                text: str,
                scale: int = 1) -> None:
    """
    Render the given text, at location (x,y) using font onto the scren buffer.
    """
    if "\n" in text:
        render_text_multiline(buffer, font, x, y, text)
        return

    font_data = __get_font(font)

    if scale == 1:
        pixel: Callable[[int, int, int, int], None] = \
            lambda x, y, cx, cy: buffer.pixel(x + cx, y + cy)
    else:
        pixel = __scale_pixel(scale, buffer.pixel)

    for c in text.upper():
        if c == " ":
            x += font_data.SPACE_WIDTH * scale
            continue
        if c in font_data.DATA:
            width, data = font_data.DATA[c]
        else:
            width, data = font_data.DATA["#"]

        for cy in range(font_data.HEIGHT):
            row = data[cy]
            if row == b'\0':
                continue
            for cx in range(width):
                if row & 1 == 1:
                    pixel(x, y, cx, cy)
                row = row >> 1
        x += (width + 1) * scale


def render_text_multiline(buffer: Graphics,
                          font: str,
                          x: int,
                          y: int,
                          textdata: str,
                          scale: int = 1) -> None:
    font_data = __get_font(font)

    for line in textdata.split("\n"):
        render_text(buffer, font, x, y, line, scale)

        y += font_data.HEIGHT


def text_boundingbox(font: str, text: str, scale: int = 1) -> Tuple[int, int]:
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

    return width * scale, height * scale


def wrap_text(font: str, text: str, max_width: int, scale: int = 1) -> str:
    lines = [text]
    while True:
        split_line = False
        for i in range(len(lines)):
            width = text_boundingbox(font, lines[i], scale)[0]
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
