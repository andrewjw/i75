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
    from typing import Any, Dict
except ImportError:
    pass

from .graphics import Graphics


def text(buffer: Graphics, font: str, x: int, y: int, text: str):
    """
    Render the given text, at location (x,y) using font onto the scren buffer.
    """
    globals: Dict[str, Any] = {}
    locals: Dict[str, Any] = {}
    exec(f"import i75.fontdata.{font}", globals, locals)
    font_data = getattr(locals["i75"].fontdata, font)

    for c in text:
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
