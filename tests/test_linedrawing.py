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

from typing import Tuple
import unittest
import unittest.mock

import picographics

from i75.graphics import Graphics


@unittest.mock.patch("hub75.pygame")
@unittest.mock.patch("i75.graphics.picographics")
class TestLineDrawing(unittest.TestCase):
    def create(self, mockgraphics: unittest.mock.Mock) \
            -> Tuple[unittest.mock.Mock, Graphics]:
        mock = unittest.mock.Mock()

        mock.get_bounds.return_value = (64, 64)
        mockgraphics.PicoGraphics.return_value = mock

        graphics = Graphics(picographics.DISPLAY_INTERSTATE75_64X64)

        return (mock, graphics)

    def test_diag_down(self, mockgraphics: unittest.mock.Mock, _) -> None:
        mock, graphics = self.create(mockgraphics)

        graphics.line(5, 5, 0, 0)

        mock.pixel.assert_called()
        for call, expected in zip(mock.pixel.mock_calls,
                                  [(5, 5), (4, 4), (3, 3),
                                   (2, 2), (1, 1), (0, 0)]):
            self.assertEqual(call[1], expected)

    def test_diag_up(self, mockgraphics: unittest.mock.Mock, _) -> None:
        mock, graphics = self.create(mockgraphics)

        graphics.line(0, 5, 5, 0)

        mock.pixel.assert_called()
        for call, expected in zip(mock.pixel.mock_calls,
                                  [(0, 5), (1, 4), (2, 3),
                                   (3, 2), (4, 1), (5, 0)]):
            self.assertEqual(call[1], expected)

    def test_steep_up(self, mockgraphics: unittest.mock.Mock, _) -> None:
        mock, graphics = self.create(mockgraphics)

        graphics.line(0, 5, 2, 0)

        mock.pixel.assert_called()
        for call, expected in zip(mock.pixel.mock_calls,
                                  [(0, 5), (0, 4), (1, 3),
                                   (1, 2), (2, 1), (2, 0)]):
            self.assertEqual(call[1], expected)

    def test_horizontal(self, mockgraphics: unittest.mock.Mock, _) -> None:
        mock, graphics = self.create(mockgraphics)

        graphics.line(0, 0, 0, 5)

        mock.pixel.assert_called()
        for call, expected in zip(mock.pixel.mock_calls,
                                  [(0, 0), (0, 1), (0, 2),
                                   (0, 3), (0, 4), (0, 5)]):
            self.assertEqual(call[1], expected)

    def test_vertical(self, mockgraphics: unittest.mock.Mock, _) -> None:
        mock, graphics = self.create(mockgraphics)

        graphics.line(0, 0, 5, 0)

        mock.pixel.assert_called()
        for call, expected in zip(mock.pixel.mock_calls,
                                  [(0, 0), (1, 0), (2, 0),
                                   (3, 0), (4, 0), (5, 0)]):
            self.assertEqual(call[1], expected)
