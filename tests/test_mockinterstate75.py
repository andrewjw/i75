#!/usr/bin/env python3
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

import unittest
import unittest.mock

from interstate75wrapper.display_type import DISPLAY_INTERSTATE75_64X64
from interstate75wrapper.mockinterstate75 import MockInterstate75


class TestMockInterstate75(unittest.TestCase):
    @unittest.mock.patch("interstate75wrapper.mockinterstate75.pygame")
    @unittest.mock.patch("interstate75wrapper.pygame_graphics.pygame")
    def test_wifi(self, _, _2):
        mock = MockInterstate75(DISPLAY_INTERSTATE75_64X64)

        self.assertFalse(mock._wifi_enabled)

        mock.enable_wifi()

        self.assertTrue(mock._wifi_enabled)

        mock.disable_wifi()

        self.assertFalse(mock._wifi_enabled)
