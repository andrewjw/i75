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

from pen import RGB332Pen, RGB888Pen


class TestPen(unittest.TestCase):
    def test_rgb888_as_tuple(self):
        self.assertEquals(RGB888Pen(100, 100, 100).as_tuple(), (100, 100, 100))

    def test_rgb332_as_tuple(self):
        self.assertEquals(RGB332Pen(100, 100, 100).as_tuple(), (96, 96, 100))
