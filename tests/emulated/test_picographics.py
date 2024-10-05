#!/usr/bin/env python3
# i75
# Copyright (C) 2023-2024 Andrew Wilkinson
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


class TestPicoGraphics(unittest.TestCase):
    def test_clear(self) -> None:
        graphics = picographics.PicoGraphics(
            picographics.DISPLAY_INTERSTATE75_64X64
        )

        red = graphics.create_pen(255, 0, 0)

        self.assertIsNone(graphics._buffer[0][0])

        graphics.set_pen(red)

        graphics.clear()

        self.assertEqual(graphics._buffer[0][0], (255, 0, 0))
