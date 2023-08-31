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

from pimoroni import RGBLED, Button  # type: ignore
from picographics import PicoGraphics  # type: ignore
from pimoroni_i2c import PimoroniI2C  # type: ignore
import hub75   # type: ignore

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
from .display_type import DisplayType


# Index Constants
SWITCH_A = 0
SWITCH_B = 1
SWITCH_BOOT = 1


class NativeI75(BaseI75):
    """
    This class is used when running on real Interstate75 hardware.
    See :ref baseinterstate75: for a description of the
    available methods.
    """
    I2C_SDA_PIN = 20
    I2C_SCL_PIN = 21
    SWITCH_PINS = (14, 23)
    SWITCH_PINS_W = (14, 15)
    LED_R_PIN = 16
    LED_G_PIN = 17
    LED_B_PIN = 18

    NUM_SWITCHES = 2

    def __init__(self,
                 display_type: DisplayType,
                 stb_invert=False,
                 rotate: int = 0) -> None:
        super().__init__(display_type,
                         wifi_ssid=WIFI_SSID,
                         wifi_password=WIFI_PASSWORD)
        self.interstate75w = "Pico W" in sys.implementation._machine

        self.display = PicoGraphics(display=display_type.i75type,
                                    rotate=rotate)
        self.width, self.height = self.display.get_bounds()

        panel_type = hub75.PANEL_GENERIC
        color_order = hub75.COLOR_ORDER_RGB
        self.hub75 = hub75.Hub75(self.width,
                                 self.height,
                                 panel_type=panel_type,
                                 stb_invert=stb_invert,
                                 color_order=color_order)
        self.hub75.start()
        if self.interstate75w:
            self._switch_pins = self.SWITCH_PINS_W
        else:
            self._switch_pins = self.SWITCH_PINS

        # Set up the user switches
        self.__switches = []
        for i in range(self.NUM_SWITCHES):
            self.__switches.append(Button(self._switch_pins[i]))

        self.__rgb = RGBLED(NativeI75.LED_R_PIN,
                            NativeI75.LED_G_PIN,
                            NativeI75.LED_B_PIN,
                            invert=True)

        # Set up the i2c for Qw/st and Breakout Garden
        self.i2c = PimoroniI2C(self.I2C_SDA_PIN, self.I2C_SCL_PIN, 100000)

        self.rtc: Optional[machine.RTC] = None

        self.wifi_available = WIFI_AVAILABLE
        if self.wifi_available:
            self.wifi_ssid = WIFI_SSID
            self.wifi_password = WIFI_PASSWORD

    @staticmethod
    def is_emulated() -> bool:
        return False

    def update(self, buffer=None):
        if buffer is None:
            buffer = self.display
        self.hub75.update(buffer)

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
