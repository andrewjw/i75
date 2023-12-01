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

from i75 import DateTime
from i75.tz import EuropeLondon


class TestEuropeLondon(unittest.TestCase):
    def test_to_local_before_clock_change(self):
        dt = DateTime(2023, 1, 1)

        self.assertEqual(dt, EuropeLondon.to_localtime(dt))

    def test_to_local_after_clock_change_back(self):
        dt = DateTime(2023, 11, 1)

        self.assertEqual(dt, EuropeLondon.to_localtime(dt))

    def test_to_local_after_clock_change(self):
        dt = DateTime(2023, 4, 1)

        self.assertEqual(DateTime(2023, 4, 1, hour=1),
                         EuropeLondon.to_localtime(dt))

    def test_to_local_march_before(self):
        dt = DateTime(2023, 3, 1)

        self.assertEqual(dt, EuropeLondon.to_localtime(dt))

    def test_to_local_march_after(self):
        dt = DateTime(2023, 3, 29)

        self.assertEqual(DateTime(2023, 3, 29, hour=1),
                         EuropeLondon.to_localtime(dt))

    def test_to_local_march_on_day(self):
        dt = DateTime(2023, 3, 26, hour=2)

        self.assertEqual(DateTime(2023, 3, 26, hour=3),
                         EuropeLondon.to_localtime(dt))

    def test_to_local_october_before(self):
        dt = DateTime(2023, 10, 1)

        self.assertEqual(DateTime(2023, 10, 1, hour=1),
                         EuropeLondon.to_localtime(dt))

    def test_to_local_october_after(self):
        dt = DateTime(2023, 10, 30)

        self.assertEqual(dt, EuropeLondon.to_localtime(dt))

    def test_to_local_october_on_day(self):
        dt = DateTime(2023, 10, 29, hour=3)

        self.assertEqual(dt, EuropeLondon.to_localtime(dt))

    def test_to_utc_before_clock_change(self):
        dt = DateTime(2023, 1, 1)

        self.assertEqual(dt, EuropeLondon.to_utc(dt))

    def test_to_utc_after_clock_change_back(self):
        dt = DateTime(2023, 11, 1)

        self.assertEqual(dt, EuropeLondon.to_utc(dt))

    def test_to_utc_after_clock_change(self):
        dt = DateTime(2023, 4, 1, hour=1)

        self.assertEqual(DateTime(2023, 4, 1), EuropeLondon.to_utc(dt))

    def test_to_utc_march_before(self):
        dt = DateTime(2023, 3, 1)

        self.assertEqual(dt, EuropeLondon.to_utc(dt))

    def test_to_utc_march_after(self):
        dt = DateTime(2023, 3, 29, hour=1)

        self.assertEqual(DateTime(2023, 3, 29), EuropeLondon.to_utc(dt))

    def test_to_utc_march_on_day(self):
        dt = DateTime(2023, 3, 26, hour=3)

        self.assertEqual(DateTime(2023, 3, 26, hour=2),
                         EuropeLondon.to_utc(dt))

    def test_to_utc_october_before(self):
        dt = DateTime(2023, 10, 1, hour=1)

        self.assertEqual(DateTime(2023, 10, 1), EuropeLondon.to_utc(dt))

    def test_to_utc_october_after(self):
        dt = DateTime(2023, 10, 30)

        self.assertEqual(dt, EuropeLondon.to_utc(dt))

    def test_to_utc_october_on_day(self):
        dt = DateTime(2023, 10, 29, hour=3)

        self.assertEqual(dt, EuropeLondon.to_utc(dt))
