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

import os.path
from typing import Dict, List, Tuple, Union
import string

from PIL import Image, ImageDraw, ImageFont

character_set = set(string.digits + string.ascii_letters.upper() + string.punctuation + "‐–£$€…"
                    + "\u2018\u2019\u201c\u201d") # quote marks

character_map: Dict[str, Union[str, List[str]]] = {
    "‐": "-",
    "–": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": "\"",
    "\u201d": "\"",
    "£": [" xx",
          "x   ",
          "xxx",
          "x   ",
          "xxx"],
    "$": [" xx",
          "xx",
          "xxx",
          " xx",
          "xx "],
    "€": [" xx",
          "x  ",
          "xxx",
          "x  ",
          " xx"],
    "…": ["    ",
          "    ",
          "    ",
          "    ",
          "xxx "]
}

def get_max_size(font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    width, height = 0, 0
    for c in character_set:
        cwidth, cheight = get_size(font, c)
        width = max(width, cwidth)
        height = max(height, cheight)
    return width, height

def get_size(font: ImageFont.FreeTypeFont, c: str) -> Tuple[int, int]:
    if c in character_map:
        c = character_map[c]

        if isinstance(c, list):
            return len(c[0]), len(c)

    im = Image.new(mode="1", size=(100, 100))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), c, font=font, fill=1, stroke_width=0)

    max_x, max_y = 0, 0
    for y in range(100):
        for x in range(100):
            if im.getpixel((x, y)) == 1:
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    print(c, max_x, max_y)
    return max_x + 1, max_y + 2

    # why doesn't the following work?
    #ascent, descent = font.getmetrics()
    #left, top, right, bottom = font.getmask(c, stroke_width=0).getbbox()
    #return right, bottom + max(0, ascent + descent)


def get_char_data(font: ImageFont.FreeTypeFont, height: int, c: str) -> bytes:
    width, _ = get_size(font, c)

    if c in character_map:
        c = character_map[c]

        if isinstance(c, list):
            data = bytes()
            for y in range(height):
                b = 0
                for x in range(width):
                    b = b | (1 if y < len(c) and x < len(c[y]) and c[y][x] == "x" else 0) << x
                data += b.to_bytes(1, "little")
            return width, data

    im = Image.new(mode="1", size=(width, height))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), c, font=font, fill=1, stroke_width=0)

    data = bytes()
    for y in range(height):
        b = 0
        for x in range(width):
            b = b | im.getpixel((x, y)) << x
        data += b.to_bytes(1, "little")

    return width, data


def generate_font_data(fontfile: str, size: int) -> None:
    fontname = os.path.basename(fontfile).split(".")[0].replace("-", "_").replace(" ", "_")
    font = ImageFont.truetype(font=fontfile, size=size)

    max_width, max_height = get_max_size(font)

    font_data = {}
    for c in character_set:
        font_data[c] = repr(get_char_data(font, max_height, c))

    try:
        os.mkdir("i75/fontdata")
    except FileExistsError:
        pass
    with open(f"i75/fontdata/{fontname}_{size}.py", "w") as fp:
        fp.write(f"# This font data was generated from\n# {fontfile} with size {size}.\n")

        fp.write(f"HEIGHT = {max_height}\n")
        fp.write(f"SPACE_WIDTH = {max_width}\n")
        fp.write("DATA = {\n")
        for c in font_data.keys():
            fp.write(f"    {repr(c)}: {font_data[c]},\n")
        fp.write("}\n")

def main() -> None:
    generate_font_data("data/cg-pixel-3x5/cg-pixel-3x5.ttf", 5)


if __name__ == "__main__":
    main()
