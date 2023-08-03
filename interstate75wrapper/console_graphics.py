#!/usr/bin/env micropython
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

import curses
import math
import io
import sys


class ConsoleGraphics:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.stdout = sys.stdout
        sys.stdout = io.StringIO()
        self.stderr = sys.stderr
        sys.stderr = io.StringIO()

        self.stdscr = curses.initscr()
        curses.start_color()
        self.stdscr.clear()

        assert curses.has_colors(), "Terminal doesn't have color support"
        assert curses.can_change_color(), "Terminal can't change colors"
        assert curses.COLORS >= 256, \
            f"Not enough colours available - {curses.COLORS}"

        # RGB332

        self.colors = {}
        c = 0
        r_bits, g_bits, b_bits = 1 << 3, 1 << 3, 1 << 2
        for r in range(0, 1 << 3):
            for g in range(0, 1 << 3):
                for b in range(0, 1 << 2):
                    self.colors[(r, g, b)] = c
                    curses.init_color(c,
                                      round(r * (1000 / (r_bits - 1))),
                                      round(g * (1000 / (g_bits - 1))),
                                      round(b * (1000 / (b_bits - 1))))
                    if c > 0:
                        curses.init_pair(c, 0, c)
                    self.stdscr.addstr(math.floor(c / width),
                                       c % width,
                                       " ",
                                       curses.color_pair(c))
                    self.stdscr.refresh()
                    c += 1

    def __del__(self) -> None:
        curses.endwin()

        stdout = sys.stdout
        sys.stdout = self.stdout
        stdout.seek(0)
        sys.stdout.write(stdout.read())

        stderr = sys.stderr
        sys.stderr = self.stderr
        stderr.seek(0)
        sys.stderr.write(stderr.read())
