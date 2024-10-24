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
    from typing import Tuple, Optional
except ImportError:
    pass

from .graphics import Graphics


class Image:
    data: bytearray

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def render(self, buffer: Graphics, offset_x: int, offset_y: int) -> None:
        raise NotImplementedError()

    def set_colour(self, red: int, green: int, blue: int) -> None:
        raise NotImplementedError()

    @staticmethod
    def load(fp) -> "Image":
        magic = fp.read(5)
        if magic != b"I75v1":
            raise ValueError(
                "Image has the wrong initial bytes. Wrong format?")
        width = int.from_bytes(fp.read(1), "big")
        height = int.from_bytes(fp.read(1), "big")
        colours = int.from_bytes(fp.read(1), "big")

        if colours == 1:
            return SingleColourImage(width, height, fp)
        if colours == 3:
            return ThreeColourImage(width, height, fp)
        raise ValueError("Image has an unsupported number of colours.")

    @staticmethod
    def load_into_buffer(fp, data: bytearray) -> "Image":
        magic = fp.read(5)
        if magic != b"I75v1":
            raise ValueError(
                "Image has the wrong initial bytes. Wrong format?")
        width = int.from_bytes(fp.read(1), "big")
        height = int.from_bytes(fp.read(1), "big")
        colours = int.from_bytes(fp.read(1), "big")

        if colours == 1:
            assert len(data) >= width * math.ceil(width / 8.0)
            return SingleColourImage(width, height, fp, data)
        if colours == 3:
            assert len(data) >= width * height * 3
            return ThreeColourImage(width, height, fp, data)
        raise ValueError("Image has an unsupported number of colours.")


class SingleColourImage(Image):
    def __init__(self,
                 width: int,
                 height: int,
                 fp,
                 data: Optional[bytearray] = None) -> None:
        super().__init__(width, height)
        if data is None:
            self.data: bytearray = fp.read(height * math.ceil(width / 8.0))
        else:
            self.data = data
            for i in range(0, height * math.ceil(width / 8.0)):
                self.data[i] = ord(fp.read(1))
        self.colour: Tuple[int, int, int] = (255, 255, 255)

    def set_colour(self, red: int, green: int, blue: int) -> None:
        self.colour = (red, green, blue)

    def render(self, buffer: Graphics, offset_x: int, offset_y: int) -> None:
        buffer.set_pen(buffer.create_pen(*self.colour))
        for y in range(self.height):
            for x in range(self.width):
                if self._is_pixel(x, y):
                    buffer.pixel(offset_x + x, offset_y + y)

    def _is_pixel(self, x: int, y: int) -> bool:
        row_width = math.ceil(self.width / 8.0)
        byte = self.data[y * row_width + math.floor(x / 8)]
        return (byte >> (7 - x % 8)) & 1 == 1


class ThreeColourImage(Image):
    def __init__(self,
                 width: int,
                 height: int,
                 fp,
                 data: Optional[bytearray] = None) -> None:
        super().__init__(width, height)
        if data is None:
            self.data: bytearray = fp.read(3 * width * height)
        else:
            self.data = data
            for i in range(0, 3 * width * height):
                self.data[i] = ord(fp.read(1))

    def render(self, buffer: Graphics, offset_x: int, offset_y: int) -> None:
        for y in range(self.height):
            for x in range(self.width):
                buffer.set_pen(buffer.create_pen(
                    self.data[3 * (y * self.width + x)],
                    self.data[3 * (y * self.width + x) + 1],
                    self.data[3 * (y * self.width + x) + 2],
                ))
                buffer.pixel(offset_x + x, offset_y + y)
