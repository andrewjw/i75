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
    WIFI_AVAILABLE = True
except ImportError:
    print("Create secrets.py with your WiFi credentials to get time from NTP")
    WIFI_AVAILABLE = False

from .baseinterstate75 import BaseInterstate75
from .datetime import DateTime
from .display_type import DisplayType


# Index Constants
SWITCH_A = 0
SWITCH_B = 1
SWITCH_BOOT = 1


class NativeInterstate75(BaseInterstate75):
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
        self.display_type = display_type
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

        self.__rgb = RGBLED(NativeInterstate75.LED_R_PIN,
                            NativeInterstate75.LED_G_PIN,
                            NativeInterstate75.LED_B_PIN,
                            invert=True)

        # Set up the i2c for Qw/st and Breakout Garden
        self.i2c = PimoroniI2C(self.I2C_SDA_PIN, self.I2C_SCL_PIN, 100000)

        self.rtc: Optional[machine.RTC] = None

    @staticmethod
    def is_mock() -> bool:
        return False

    def update(self, buffer=None):
        if buffer is None:
            buffer = self.display
        self.hub75.update(buffer)

    def enable_wifi(self,
                    callback: Optional[Callable[[int], None]] = None) -> bool:
        if not WIFI_AVAILABLE:
            return False

        # Start connection
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        # Turn WiFi power saving off for some slow APs
        self.wlan.config(pm=0xa11140)
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connect success or failure
        max_wait = 100
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            if callback is not None:
                callback(self.wlan.status())
            time.sleep_ms(200)

        return self.wlan.isconnected()

    def disable_wifi(self) -> None:
        if not WIFI_AVAILABLE or not hasattr(self, "wlan"):
            return
        self.wlan.disconnect()
        self.wlan.active(False)

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
