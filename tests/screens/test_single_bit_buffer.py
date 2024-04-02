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

from i75.screens import SingleBitBuffer


class TestSingleBitBuffer(unittest.TestCase):
    def test_set_zero_zero(self):
        buf = SingleBitBuffer(10, 10)
        self.assertFalse(buf.is_pixel_set(0, 0))
        buf.set_pixel(0, 0)
        self.assertTrue(buf.is_pixel_set(0, 0))
        buf.clear_pixel(0, 0)
        self.assertFalse(buf.is_pixel_set(0, 0))

    def test_set_part_row_byte(self):
        buf = SingleBitBuffer(10, 10)
        self.assertFalse(buf.is_pixel_set(9, 2))
        buf.set_pixel(9, 2)
        self.assertTrue(buf.is_pixel_set(9, 2))
        buf.clear_pixel(9, 2)
        self.assertFalse(buf.is_pixel_set(9, 2))

    def test_reset(self):
        buf = SingleBitBuffer(10, 10)
        self.assertFalse(buf.is_pixel_set(0, 0))
        self.assertFalse(buf.is_pixel_set(9, 2))
        buf.set_pixel(0, 0)
        buf.set_pixel(9, 2)
        self.assertTrue(buf.is_pixel_set(0, 0))
        self.assertTrue(buf.is_pixel_set(9, 2))
        buf.reset()
        self.assertFalse(buf.is_pixel_set(0, 0))
        self.assertFalse(buf.is_pixel_set(9, 2))

    def test_reset_noop(self):
        buf = SingleBitBuffer(10, 10)
        self.assertFalse(buf.is_pixel_set(0, 0))
        buf.reset()
        self.assertFalse(buf.is_pixel_set(0, 0))
