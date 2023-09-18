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
    from typing import Callable, Optional
except ImportError:  # pragma: no cover
    pass

import hub75
import picographics
from pimoroni import RGBLED, Button
from pimoroni_i2c import PimoroniI2C
import network
import ntptime
import machine
import time
import sys


from .datetime import DateTime
from .graphics import Graphics


# Index Constants
SWITCH_A = 0
SWITCH_B = 1
SWITCH_BOOT = 1


class BaseI75:
    I2C_SDA_PIN = 20
    I2C_SCL_PIN = 21
    SWITCH_PINS = (14, 23)
    SWITCH_PINS_W = (14, 15)
    LED_R_PIN = 16
    LED_G_PIN = 17
    LED_B_PIN = 18

    NUM_SWITCHES = 2

    """This is the base class for the Interstate75 library. All
       functions are overridden by either an emulated version, which
       replicates the functionality, or a native version if we're
       running on real Interstate75 hardware."""
    def __init__(self,
                 display_type: picographics.DisplayType,
                 stb_invert=False,
                 rotate: int = 0,
                 wifi_ssid: Optional[str] = None,
                 wifi_password: Optional[str] = None) -> None:
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.wlan: Optional[network.WLAN] = None

        self.interstate75w = not hasattr(sys.implementation, "_machine") \
            or "Pico W" in sys.implementation._machine

        self.display = Graphics(display_type,
                                rotate,
                                hub75.PANEL_GENERIC,
                                stb_invert,
                                hub75.COLOR_ORDER_RGB)

        if self.interstate75w:
            self._switch_pins = self.SWITCH_PINS_W
        else:
            self._switch_pins = self.SWITCH_PINS

        # Set up the user switches
        self.__switches = []
        for i in range(self.NUM_SWITCHES):
            self.__switches.append(Button(self._switch_pins[i]))

        self.__rgb = RGBLED(BaseI75.LED_R_PIN,
                            BaseI75.LED_G_PIN,
                            BaseI75.LED_B_PIN,
                            invert=True)

        # Set up the i2c for Qw/st and Breakout Garden
        self.i2c = PimoroniI2C(self.I2C_SDA_PIN, self.I2C_SCL_PIN, 100000)

        self.rtc: Optional[machine.RTC] = None

    def enable_wifi(self,
                    callback: Optional[Callable[[int], None]] = None
                    ) -> bool:
        """Enables wifi.

           To run on real Interstate75 hardware you must have a secrets files
           (see :doc:`secrets`)

           :param callback: A function which is called every 200ms with the
               current connection status.
        """
        if self.wifi_ssid is None or self.wifi_password is None:
            return False

        # Start connection
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        # Turn WiFi power saving off for some slow APs
        self.wlan.config(pm=0xa11140)
        self.wlan.connect(self.wifi_ssid, self.wifi_password)

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
        """
        Disables the wifi.

        Noop is wifi is not available, or hasn't been enabled.
        """
        if self.wifi_ssid is None or self.wifi_password is None\
                or self.wlan is None:
            return
        self.wlan.disconnect()
        self.wlan.active(False)

    def set_time(self) -> bool:  # pragma: no cover
        raise NotImplementedError()

    def now(self) -> DateTime:  # pragma: no cover
        raise NotImplementedError()

    def sleep_ms(self, delay: int) -> None:  # pragma: no cover
        raise NotImplementedError()

    def ticks_ms(self) -> int:  # pragma: no cover
        raise NotImplementedError()

    def ticks_diff(self, t1: int, t2: int) -> int:  # pragma: no cover
        raise NotImplementedError()

    @staticmethod
    def is_emulated() -> bool:  # pragma: no cover
        """
        Returns true if we are not running on real Interstate75 hardware.
        """
        raise NotImplementedError()
