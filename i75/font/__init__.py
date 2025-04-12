# Adapted from https://github.com/lowfatcode/alright-fonts/tree/main
# MIT License
#
# Copyright (c) 2022 lowfatcode
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
from typing import Dict, List, Optional, Tuple, Union
import struct
import sys


class Point():
    def __init__(self,
                 x: Optional[int
                             | float
                             | Tuple[int, int]
                             | Tuple[float, float]] = None,
                 y: Optional[int | float] = None) -> None:
        if x is not None:
            if isinstance(x, tuple):
                self.x = x[0]
                self.y = x[1]
            elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
                self.x = x
                self.y = y
            else:
                raise TypeError(
                    f"Invalid type for x ({type(x)} or y ({type(y)})")
        else:
            self.x = 0
            self.y = 0

    def scale(self, scale_x, scale_y=None) -> "Point":
        if not scale_y:
            scale_y = scale_x
        return Point(self.x * scale_x, self.y * scale_y)

    def round(self) -> "Point":
        return Point(round(self.x), round(self.y))

    def distance(self, other) -> float:
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return math.sqrt(dx * dx + dy * dy)

    def delta(self, p) -> "Point":
        if p:
            return Point(self.x - p.x, self.y - p.y)
        return Point(self.x, self.y)

    def __repr__(self) -> str:
        return "Point({}, {})".format(self.x, self.y)


class Glyph():
    def __init__(self) -> None:
        self.codepoint: int
        self.advance: float
        self.bbox_x: float
        self.bbox_y: float
        self.bbox_w: float
        self.bbox_h: float
        self.contours: List[List[Point]] = []

    def __repr__(self) -> str:
        return f"{self.codepoint} ({self.bbox_x},{self.bbox_y}: " \
               + f"{self.bbox_w}x{self.bbox_h}) [{self.advance}]"


class Face():
    def __init__(self) -> None:
        self.glyphs: Dict[int, Glyph] = {}

    def get_glyph(self, codepoint: int) -> Optional[Glyph]:
        if codepoint not in self.glyphs:
            return None

        return self.glyphs[codepoint]

    def get_height(self) -> float:
        height = 0.0
        for glyph in self.glyphs.values():
            if glyph.bbox_h is not None and glyph.bbox_h > height:
                height = glyph.bbox_h

        return height

    @property
    def space_width(self) -> int:
        space_glyph = self.get_glyph(ord(" "))
        if space_glyph is None:
            return int(list(self.glyphs.values())[0].advance)
        return int(space_glyph.advance)

    @staticmethod
    def load_face(file_or_name_or_bytes: str | bytes) -> "Face":
        face = Face()

        data: Union[bytes, bytearray]
        if isinstance(file_or_name_or_bytes, (bytes, bytearray)):
            data = file_or_name_or_bytes
        elif isinstance(file_or_name_or_bytes, str):
            f = open(file_or_name_or_bytes, "rb")
            data = f.read()
            f.close()
        else:
            data = file_or_name_or_bytes.read()

        # check the header is correct
        if data[:4] != b"af!?":
            print("> invalid Alright Fonts file provided. "
                  + "no matching magic marker in header!")
            sys.exit()

        glyph_count = int.from_bytes(data[4:6], byteorder="big")
        flags = int.from_bytes(data[6:8], byteorder="big")

        glyph_entry_length = 9

        # contours start at end of glyph dictionary
        contour_offset = 8 + (glyph_count * glyph_entry_length)

        for i in range(0, glyph_count):
            glyph = Glyph()
            glyph_entry_offset = 8 + (i * glyph_entry_length)
            glyph.codepoint, glyph.bbox_x, glyph.bbox_y, glyph.bbox_w, \
                glyph.bbox_h, glyph.advance, contour_data_length = \
                struct.unpack(
                    ">HbbBBBH",
                    data[glyph_entry_offset:
                         glyph_entry_offset + glyph_entry_length]
                )

            glyph.contours = extract_contours(
                data[contour_offset:contour_offset + contour_data_length])
            contour_offset += contour_data_length

            face.glyphs[glyph.codepoint] = glyph

        return face


class Font:
    def __init__(self, face: Face, height: int) -> None:
        self.face = face
        self.height = height
        self.scale = height / self.face.get_height()
        self.glyphs: Dict[int, Optional[Glyph]] = {}

    def get_height(self) -> float:
        return self.height

    def get_glyph(self, codepoint: int) -> Optional[Glyph]:
        if codepoint not in self.glyphs:
            original_glyph = self.face.get_glyph(codepoint)
            if original_glyph is None:
                self.glyphs[codepoint] = None
            else:
                glyph = Glyph()
                glyph.codepoint = original_glyph.codepoint
                glyph.advance = original_glyph.advance * self.scale
                glyph.bbox_x = original_glyph.bbox_x * self.scale
                glyph.bbox_y = original_glyph.bbox_y * self.scale
                glyph.bbox_w = original_glyph.bbox_w * self.scale
                glyph.bbox_h = original_glyph.bbox_h * self.scale
                glyph.contours = []
                for contour in original_glyph.contours:
                    new_contour: List[Point] = []
                    for point in contour:
                        new_contour.append(point.scale(self.scale))
                    glyph.contours.append(new_contour)
                self.glyphs[codepoint] = glyph

        return self.glyphs[codepoint]

    @property
    def space_width(self) -> int:
        return int(self.face.space_width * self.scale)


def extract_contours(data) -> List[List[Point]]:
    contours: List[List[Point]] = []

    offset = 0
    while True:
        point_count: int = struct.unpack(">H", data[offset + 0:offset + 2])[0]
        offset += 2
        if point_count == 0:  # at end we have a "zero" contour
            break

        contour: List[Point] = []

        # load points of contour
        for j in range(0, point_count):
            point = Point()
            point.x, point.y = struct.unpack(
                ">bb",
                data[offset + 0:offset + 2])
            offset += 2
            contour.append(point)

        contours.append(contour)

    return contours
