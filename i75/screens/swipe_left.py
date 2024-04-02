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
    from typing import Callable
except ImportError:
    pass

from ..colour import Colour
from .screen import Screen
from .screen_wipe import ScreenWipe


class SwipeLeft(ScreenWipe):
    def __init__(self,
                 width: int,
                 height: int,
                 duration: int,
                 first: Screen,
                 second: Screen) -> None:
        super().__init__(width, height, duration, first, second)

        self.pixel_per_ms = self.width / float(self.duration)

    def get_pixel(self, x: int, y: int) -> Colour:
        divide = self.__get_divide(self.total_time)

        if x >= divide:
            return self.second.get_pixel(x, y)
        return self.first.get_pixel(x, y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        old_divide = self.__get_divide(self.total_time)
        self.total_time = min(self.total_time + frame_time, self.duration)
        new_divide = self.__get_divide(self.total_time)

        if old_divide != new_divide:
            for x in range(new_divide, old_divide):
                for y in range(0, self.height):
                    mark_dirty(x, y)

        self.first.update(frame_time,
                          lambda x, y:
                          mark_dirty(x, y) if x >= new_divide else None)
        self.second.update(frame_time,
                           lambda x, y:
                           mark_dirty(x, y) if x < new_divide else None)

    def __get_divide(self, time: int) -> int:
        return max(self.width - round(time * self.pixel_per_ms), 0)
