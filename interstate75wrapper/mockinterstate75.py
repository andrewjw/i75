#!/usr/bin/env micropython
# interstate75-wrapper
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

from datetime import datetime as PyDateTime
import math
import time
from typing import Callable, Optional

import pygame
from .pygame_graphics import PyGameGraphics

from .baseinterstate75 import BaseInterstate75
from .datetime import DateTime
from .display_type import DisplayType


class MockInterstate75(BaseInterstate75):
    def __init__(self,
                 display_type: DisplayType,
                 stb_invert=False,
                 rotate: int = 0) -> None:
        super().__init__(display_type)

        self.display = PyGameGraphics(self.display_type.width,
                                      self.display_type.height,
                                      rotate=rotate)
        self.width, self.height = self.display.get_bounds()

        self._wifi_enabled = False

    @staticmethod
    def is_mock() -> bool:
        return True

    def update(self):
        pygame.display.flip()

    def enable_wifi(self,
                    callback: Optional[Callable[[int], None]] = None) -> bool:
        self._wifi_enabled = True
        return True

    def disable_wifi(self) -> None:
        self._wifi_enabled = False

    def set_time(self) -> bool:
        return self._wifi_enabled

    def ticks_ms(self) -> int:
        return math.floor(time.time_ns() / 1000000)

    def ticks_diff(self, t1: int, t2: int) -> int:
        return t1 - t2

    def sleep_ms(self, delay: int) -> None:
        time.sleep(delay / 1000.0)

    def now(self) -> DateTime:
        now = PyDateTime.utcnow()
        return DateTime(now.year,
                        now.month,
                        now.day,
                        now.weekday(),
                        now.hour,
                        now.minute,
                        now.second,
                        now.microsecond)
