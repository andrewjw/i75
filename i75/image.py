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
    from typing import Callable, Tuple, Optional
except ImportError:
    pass

from .colour import Colour
from .graphics import Graphics
from .screens.screen import Screen
from .screens.full_colour_screen import FullColourScreen
from .screens.single_bit_screen import SingleBitScreen


class Image(Screen):
    data: bytearray

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def render(self, buffer: Graphics, offset_x: int, offset_y: int) -> None:
        raise NotImplementedError()

    def set_colour(self, colour: Colour) -> None:
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
    def _read_metadata(fp) -> Tuple[int, int, int]:
        magic = fp.read(5)
        if magic != b"I75v1":
            raise ValueError(
                "Image has the wrong initial bytes. Wrong format?")
        width = int.from_bytes(fp.read(1))
        height = int.from_bytes(fp.read(1))
        colours = int.from_bytes(fp.read(1))

        return width, height, colours


class SingleColourImage(Image):
    def __init__(self,
                 width: int,
                 height: int,
                 fp) -> None:
        super().__init__(width, height)
        self._screen = SingleBitScreen(width, height)
        SingleColourImage.load_into_screen(width, height, fp, self._screen)

    def release(self):
        self._screen.release()

    def set_colour(self, colour: Colour) -> None:
        self._screen.set_colour(colour)

    def get_pixel(self, x: int, y: int) -> Colour:
        return self._screen.get_pixel(x, y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        self._screen.update(frame_time, mark_dirty)

    def set_pixel(self, x: int, y: int, *colour: bool) -> None:
        self._screen.set_pixel(x, y, *colour)

    def is_pixel_set(self, x: int, y: int) -> bool:
        return self._screen.is_pixel_set(x, y)

    @staticmethod
    def load(fp) -> "SingleColourImage":
        width, height, colours = Image._read_metadata(fp)
        if colours != 1:
            raise ValueError("Image has an unsupported number of colours.")
        fp.seek(0)  # Reset file pointer to the start
        return SingleColourImage(width, height, fp)

    @staticmethod
    def load_into_screen(width: int,
                         height: int,
                         fp,
                         screen: SingleBitScreen) -> None:
        width, height, colours = Image._read_metadata(fp)
        if colours != 1:
            raise ValueError("Image has an unsupported number of colours.")
        current: int = 0
        for y in range(height):
            count: int = 0
            for x in range(width):
                if count % 8 == 0:
                    current = ord(fp.read(1))
                screen.set_pixel(x, y, (current >> (7 - count % 8)) & 1 == 1)
                count += 1


class ThreeColourImage(Image):
    def __init__(self,
                 width: int,
                 height: int,
                 fp,
                 skip_metadata: bool = False) -> None:
        super().__init__(width, height)
        self._screen = FullColourScreen.get(width, height)
        ThreeColourImage.load_into_screen(width,
                                          height,
                                          fp,
                                          self._screen,
                                          skip_metadata)

    def release(self):
        self._screen.release()

    def get_pixel(self, x: int, y: int) -> Colour:
        return self._screen.get_pixel(x, y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        self._screen.update(frame_time, mark_dirty)

    def set_pixel(self, x: int, y: int, *colour: Colour) -> None:
        self._screen.set_pixel(x, y, *colour)

    @staticmethod
    def load(fp) -> "ThreeColourImage":
        width, height, colours = Image._read_metadata(fp)
        if colours != 3:
            raise ValueError("Image has an unsupported number of colours.")
        return ThreeColourImage(width, height, fp, True)

    @staticmethod
    def load_into_screen(width: int,
                         height: int,
                         fp,
                         screen: FullColourScreen,
                         skip_metadata: bool = False) -> None:
        if not skip_metadata:
            width, height, colours = Image._read_metadata(fp)
            if colours != 3:
                raise ValueError("Image has an unsupported number of colours.")

        for y in range(height):
            for x in range(width):
                screen.set_raw_pixel(x,
                                     y,
                                     ord(fp.read(1)),
                                     ord(fp.read(1)),
                                     ord(fp.read(1)))
