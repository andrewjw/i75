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

# Based off https://github.com/pimoroni/pimoroni-pico/blob/
# main/micropython/modules_py/interstate75.py

import time
try:
    from typing import Any, Callable, Optional
except ImportError:
    pass

import ntptime   # type: ignore
from presto import Presto
import machine

from .basei75 import BaseI75
from .datetime import DateTime
from .prestographics import PrestoGraphics


class PrestoI75(BaseI75):
    """
    This class is used when running on real Presto hardware.
    See :ref baseinterstate75: for a description of the
    available methods.
    """
    def __init__(self) -> None:
        self.presto = Presto(full_res=False)

        self.display = PrestoGraphics(self.presto)

    @staticmethod
    def is_emulated() -> bool:
        return False

    def enable_wifi(self,
                    callback: Optional[Callable[[int], None]] = None
                    ) -> bool:
        self.presto.connect()

    def set_time(self) -> bool:
        try:
            ntptime.settime()
        except OSError:
            return False
        else:
            self.rtc = machine.RTC()
            return True

    def ticks_ms(self) -> int:
        return time.ticks_ms()

    def ticks_diff(self, t1: int, t2: int) -> int:
        return time.ticks_diff(t1, t2)

    def sleep_ms(self, delay: int) -> None:
        time.sleep_ms(delay)

    def now(self) -> DateTime:
        assert self.rtc is not None
        return DateTime(*self.rtc.datetime())
