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

from i75.datetime import Date, DateTime, TimeDelta


class TestDateTime(unittest.TestCase):
    def test_date_leap_year(self):
        d = Date(2024, 2, 29)
        self.assertEqual(2024, d.year)
        self.assertEqual(2, d.month)
        self.assertEqual(29, d.day)
        self.assertEqual(3, d.weekday())
