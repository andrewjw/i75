#!/usr/bin/env python3
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

class NetworkType:
    pass


STA_IF = NetworkType()

STAT_IDLE = 0
STAT_CONNECTING = 1
STAT_WRONG_PASSWORD = -1
STAT_NO_AP_FOUND = -2
STAT_CONNECT_FAIL = -3
STAT_GOT_IP = 3


class WLAN:
    """
    This is an emulation of the built-in WLAN class. As we can't actually
    control the wifi, it just pretends to configure it when called.
    """
    def __init__(self, network_type: NetworkType) -> None:
        assert network_type is STA_IF, \
            "STA_IF is the only supported network type currently."

        self._wifi_active = False
        self._wifi_connected = False

    def active(self, active: bool) -> None:
        self._wifi_active = active

    def config(self, pm: int) -> None:
        pass

    def connect(self, ssid: str, password: str) -> None:
        assert self._wifi_active
        self._wifi_connected = True

    def disconnect(self) -> None:
        self._wifi_connected = False

    def status(self) -> int:
        if self._wifi_active and self._wifi_connected:
            return STAT_GOT_IP
        if self._wifi_active:
            return STAT_IDLE
        return STAT_CONNECT_FAIL

    def isconnected(self) -> bool:
        return self._wifi_connected
