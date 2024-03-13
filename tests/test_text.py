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

from i75.text import render_text, text_boundingbox

FONT = "cg_pixel_3x5_5"


class TestText(unittest.TestCase):
    def test_bounding_box_width_matches_render(self) -> None:
        text = "This Is A Test String."
        width, _ = text_boundingbox(FONT, text)

        mock_buffer = unittest.mock.Mock()
        render_text(mock_buffer, FONT, 0, 0, text)

        max_x = max([x for ((x, _), _) in mock_buffer.pixel.call_args_list])

        self.assertEqual(width, max_x + 2)
