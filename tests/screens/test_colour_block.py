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
from i75.screens.colour_block import ColourBlock


class TestColourBlock(unittest.TestCase):
    def test_get_colour(self):
        colour = Colour.fromrgb(255, 0, 0)
        cb = ColourBlock(20, 20, colour)
        self.assertEqual(cb.get_pixel(10, 10), colour)

    def test_outside(self):
        colour = Colour.fromrgb(255, 0, 0)
        cb1 = ColourBlock(20, 20, colour)
        self.assertEqual(cb1.get_pixel(-5, -5).a, 0)
        self.assertEqual(cb1.get_pixel(5, 5), colour)
        self.assertEqual(cb1.get_pixel(25, 25).a, 0)
