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

import unittest
import unittest.mock

import picographics

from i75.emulatedi75 import EmulatedI75


class TestEmulatedI75(unittest.TestCase):
    @unittest.mock.patch("hub75.pygame")
    def test_wifi(self, _):
        i75 = EmulatedI75(picographics.DISPLAY_INTERSTATE75_64X64)

        self.assertFalse(i75.wlan is not None and i75.wlan.isconnected())

        i75.enable_wifi()

        self.assertTrue(i75.wlan is not None and i75.wlan.isconnected())

        i75.disable_wifi()

        self.assertFalse(i75.wlan is not None and i75.wlan.isconnected())
