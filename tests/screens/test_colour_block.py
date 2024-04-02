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

from i75 import Colour
from i75.screens import ColourBlock


class TestColourBlock(unittest.TestCase):
    def test_get_colour(self):
        colour = Colour.fromrgb(255, 0, 0)
        cb = ColourBlock(10, 10, 20, 20, colour)
        self.assertEqual(cb.get_pixel(10, 10), colour)

    def test_outside(self):
        colour1 = Colour.fromrgb(255, 0, 0)
        colour2 = Colour.fromrgb(255, 0, 0)
        cb2 = ColourBlock(0, 0, 30, 30, colour2)
        cb1 = ColourBlock(10, 10, 20, 20, colour1, cb2)
        self.assertEqual(cb1.get_pixel(10, 10), colour1)
        self.assertEqual(cb1.get_pixel(5, 5), colour1)
        self.assertEqual(cb1.get_pixel(25, 25), colour2)
