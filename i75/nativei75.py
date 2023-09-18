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
import sys

from pimoroni import RGBLED, Button
from pimoroni_i2c import PimoroniI2C  # type: ignore
import hub75   # type: ignore

import picographics
import network   # type: ignore
import ntptime   # type: ignore
import machine

try:
    from secrets import WIFI_SSID, WIFI_PASSWORD   # type: ignore
    WIFI_AVAILABLE: bool = True
except ImportError:
    print("Create secrets.py with your WiFi credentials to get time from NTP")
    WIFI_AVAILABLE = False
    WIFI_SSID = None
    WIFI_PASSWORD = None

from .basei75 import BaseI75
from .datetime import DateTime


class NativeI75(BaseI75):
    """
    This class is used when running on real Interstate75 hardware.
    See :ref baseinterstate75: for a description of the
    available methods.
    """
    def __init__(self,
                 display_type: picographics.DisplayType,
                 stb_invert=False,
                 rotate: int = 0) -> None:
        super().__init__(display_type,
                         rotate=rotate,
                         wifi_ssid=WIFI_SSID,
                         wifi_password=WIFI_PASSWORD)

    @staticmethod
    def is_emulated() -> bool:
        return False

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
