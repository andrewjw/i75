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

from io import BytesIO

import unittest
import unittest.mock

from i75.image import SingleColourImage


class TestImage(unittest.TestCase):
    def test_single_color_image_is_pixel(self):
        image_data = BytesIO((1 << 6).to_bytes(1, byteorder="big")
                             + (1 << 7).to_bytes(1, byteorder="big"))
        sci = SingleColourImage(2, 2, image_data)

        self.assertFalse(sci._is_pixel(0, 0))
        self.assertTrue(sci._is_pixel(1, 0))
        self.assertTrue(sci._is_pixel(0, 1))
        self.assertFalse(sci._is_pixel(1, 1))
