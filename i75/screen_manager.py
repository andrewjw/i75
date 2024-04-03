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
    from typing import Optional
except ImportError:
    pass

from .graphics import Graphics
from .screens.screen import Screen
from .screens.single_bit_buffer import SingleBitBuffer


class ScreenManager:
    def __init__(self, width: int, height: int, display: Graphics) -> None:
        self.width = width
        self.height = height
        self._dirty_buffer = SingleBitBuffer(width, height)
        self._display = display
        self._screen: Optional[Screen] = None

    def set_screen(self, screen: Screen, mark_dirty: bool = True) -> None:
        self._screen = screen

        if not mark_dirty:
            return
        for x in range(self.width):
            for y in range(self.height):
                self._dirty_buffer.set_pixel(x, y)

    def update(self, frame_time: int) -> None:
        if self._screen is None:
            return

        self._screen.update(frame_time, self._dirty_buffer.set_pixel)

        for x in range(self.width):
            for y in range(self.height):
                if self._dirty_buffer.is_pixel_set(x, y):
                    c = self._screen.get_pixel(x, y)
                    self._display.set_colour(c)
                    self._display.pixel(x, y)

        self._display.flip()

        self._dirty_buffer.reset()
