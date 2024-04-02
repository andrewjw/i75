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

try:
    from typing import Callable, List, Tuple, Optional
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour
from ..image import SingleColourImage
from .screen import Screen


class SpriteInstance(Screen):
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 colour: Colour,
                 image: SingleColourImage,
                 child: Screen) -> None:
        super().__init__(child)
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._colour = colour
        self._image = image
        self._move_to: Optional[Tuple[int, int]] = None

        self._first_dirty = None

    def get_pixel(self, x: int, y: int) -> Colour:
        assert self._child is not None
        if self._first_dirty is not None and self._first_dirty == (x, y):
            print("d", x, y, self._offset_x, self._offset_y, self._child.get_pixel(x, y))
            print(x < self._offset_x \
           or y < self._offset_y \
           or x >= (self._offset_x + self._image.width) \
           or y >= (self._offset_y + self._image.height))
        if x < self._offset_x \
           or y < self._offset_y \
           or x >= (self._offset_x + self._image.width) \
           or y >= (self._offset_y + self._image.height):
            return self._child.get_pixel(x, y)

        return self._colour if self._image._is_pixel(x - self._offset_x, y - self._offset_y) else self._child.get_pixel(x, y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        if self._move_to is not None:
            first = True
            for dx in range(min(self._offset_x, self._move_to[0]),
                            max(self._offset_x, self._move_to[0]) + self._image.width):
                for dy in range(min(self._offset_y, self._move_to[1]),
                                max(self._offset_y, self._move_to[1]) + self._image.height):
                    if dx >= 0 and dx < 64 and dy >= 0 and dy < 64:
                        x1, y1 = dx - self._offset_x, dy - self._offset_y
                        x2, y2 = dx - self._move_to[0], dy - self._move_to[1]
                        valid1 = x1 >= 0 and y1 >= 0 and x1 < self._image.width and y1 < self._image.height
                        valid2 = x2 >= 0 and y2 >= 0 and x2 < self._image.width and y2 < self._image.height
                        if valid1 and valid2:
                            c1 = self._image._is_pixel(x1, y1)
                            c2 = self._image._is_pixel(x2, y2)
                            if c1 != c2:
                                mark_dirty(dx, dy)
                        elif valid1:
                            # if old position was set, mark as dirty to clear it
                            if self._image._is_pixel(x1, y1):
                                if first:
                                    first = False
                                    self._first_dirty = (dx, dy)
                                    print(dx, dy, x1, y1, x2, y2)
                            mark_dirty(dx, dy)
                        elif valid2:
                            # if new position is set, mark as dirty to draw it
                            if self._image._is_pixel(x2, y2):
                                mark_dirty(dx, dy)

            self._offset_x, self._offset_y = self._move_to
            self._move_to = None

        if self._child is not None:
            self._child.update(frame_time, mark_dirty)

    def move_to(self, x: int, y: int) -> None:
        self._move_to = (x, y)

    @property
    def width(self) -> int:
        return self._image.width

    @property
    def height(self) -> int:
        return self._image.height
