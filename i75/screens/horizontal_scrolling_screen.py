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
    from typing import Callable, List, Tuple
except ImportError:  # pragma: no cover
    pass

from ..colour import Colour
from .screen import Screen


class HorizontalScrollingScreen(Screen):
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 viewport_width: int,
                 viewport_height: int,
                 screen: Screen,
                 screen_width: int,
                 child: Screen,
                 initial_pause: int = 2500,
                 scroll_duration: int = 5000,
                 final_pause: int = 2500) -> None:
        super().__init__(child)
        self._offset_x = offset_x
        self._offset_y = offset_y
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self._scroll_x = 0
        self.total_time = 0
        self.initial_pause = initial_pause
        self.scroll_duration = scroll_duration
        self.final_pause = final_pause
        self.screen = screen
        self.screen_width = screen_width
        self.__reset = False

    def get_pixel(self, x: int, y: int) -> Colour:
        if x < self._offset_x or x >= self._offset_x + self.viewport_width \
           or y < self._offset_y or y >= self._offset_y + self.viewport_height:
            assert self._child is not None
            return self._child.get_pixel(x, y)

        return self.screen.get_pixel(x - self._offset_x + self._scroll_x,
                                     y - self._offset_y)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        if self._child is not None:
            self._child.update(frame_time, mark_dirty)

        old_scroll = self._scroll_x
        if not self.__reset:
            self.total_time = min(self.total_time + frame_time,
                                  self.total_duration)
            if self.total_time > self.initial_pause \
               and self.total_time <= \
                    (self.initial_pause + self.scroll_duration):
                self._scroll_x = \
                    round((self.screen_width - self.viewport_width)
                          * float(self.total_time - self.initial_pause)
                          / self.scroll_duration)
            if old_scroll == self._scroll_x:
                return
        else:
            self.__reset = False
            self.total_time = 0
            self._scroll_x = 0

        for x in range(self.viewport_width):
            for y in range(self.viewport_height):
                c1 = self.screen.get_pixel(x + old_scroll, y)
                c2 = self.screen.get_pixel(x + self._scroll_x, y)
                if c1 != c2:
                    mark_dirty(x + self._offset_x, y + self._offset_y)

    def is_complete(self):
        return self.total_time >= self.total_duration

    def reset(self):
        self.__reset = True

    @property
    def total_duration(self):
        return self.initial_pause + self.scroll_duration + self.final_pause
