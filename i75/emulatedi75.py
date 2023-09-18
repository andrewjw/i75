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

from datetime import datetime as PyDateTime
import math
import time
from typing import Callable, Optional

import picographics

from .basei75 import BaseI75
from .datetime import DateTime


class EmulatedI75(BaseI75):
    """
    This class aims to emulates all the features of the Interstate75, using
    PyGame to render the display. See :ref baseinterstate75: for a description
    of the available methods.
    """
    def __init__(self,
                 display_type: picographics.DisplayType,
                 stb_invert=False,
                 rotate: int = 0) -> None:
        super().__init__(display_type,
                         rotate=rotate,
                         wifi_ssid="native",
                         wifi_password="native")

    @staticmethod
    def is_emulated() -> bool:
        return True

    def set_time(self) -> bool:
        return self.wlan is not None and self.wlan.isconnected()

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
