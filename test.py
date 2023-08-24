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
import sys

import tests

def suite():
    """Test suite"""

    return unittest.defaultTestLoader.loadTestsFromModule(tests)

if __name__ == "__main__":
    RESULT = unittest.TextTestRunner(verbosity=2).run(suite())

    sys.exit(0 if RESULT.wasSuccessful() else 1)
