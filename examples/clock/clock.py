#!/usr/bin/env micropython
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

import math
import time

from interstate75wrapper import DateTime, Interstate75Wrapper, \
                                Pen, display_type

HOUR_LENGTH = 25
MINUTE_LENGTH = 30
SECOND_LENGTH = 30


def render_clock_face(i75: Interstate75Wrapper) -> None:
    for tick in range(12):
        tick_len = 3 if tick in (0, 3, 6, 9) else 2
        x1 = math.floor((31 - tick_len) *
                        math.cos(2 * math.pi * tick / 12.0) + 31.5)
        y1 = math.floor((31 - tick_len) *
                        math.sin(2 * math.pi * tick / 12.0) + 31.5)
        x2 = math.floor(31 * math.cos(2 * math.pi * tick / 12.0) + 31.5)
        y2 = math.floor(31 * math.sin(2 * math.pi * tick / 12.0) + 31.5)

        i75.display.line(x1, y1, x2, y2)


def render_hand(i75: Interstate75Wrapper, length: int, percent: float) -> None:
    i75.display.line(32,
                     32,
                     math.floor(length * math.sin(2 * math.pi * percent) + 32),
                     math.floor(length *
                                -math.cos(2 * math.pi * percent) + 32))


def render_clock(i75: Interstate75Wrapper,
                 white: Pen,
                 red: Pen,
                 now: DateTime,
                 subsecond: int,
                 display_ticks: bool = True) -> None:
    if display_ticks:
        i75.display.set_pen(white)
        render_clock_face(i75)

    i75.display.set_pen(red)

    part_second = subsecond / 1000.0
    render_hand(i75, SECOND_LENGTH, (now.second + part_second) / 60.0)

    i75.display.set_pen(white)

    minute_percent = (now.minute * 60
                      + now.second
                      + part_second) / (60.0 * 60)
    hour_percent = (((now.hour + 1) % 12) * (60 * 60)
                    + now.minute * 60
                    + now.second + part_second) / (60.0 * 60 * 12)
    render_hand(i75, MINUTE_LENGTH, minute_percent)
    render_hand(i75, HOUR_LENGTH, hour_percent)

    return now


def main() -> None:
    i75 = Interstate75Wrapper(
        display_type=display_type.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if Interstate75Wrapper.is_mock() else 90)

    i75.enable_wifi()
    i75.set_time()
    base_ticks = i75.ticks_ms()

    white = i75.display.create_pen(255, 255, 255)
    red = i75.display.create_pen(255, 0, 0)
    black = i75.display.create_pen(0, 0, 0)

    old_time = i75.now()
    old_subsecond = 0

    while True:
        now = i75.now()
        subsecond = i75.ticks_diff(i75.ticks_ms(), base_ticks) % 1000

        if now != old_time and subsecond > old_subsecond and subsecond < 9975:
            base_ticks -= 25
        elif now == old_time and subsecond < old_subsecond:
            base_ticks += 25
            subsecond = 999

        render_clock(i75,
                     black,
                     black,
                     old_time,
                     old_subsecond,
                     False)
        render_clock(i75,
                     white,
                     red,
                     now,
                     subsecond)
        old_time = now
        old_subsecond = subsecond

        i75.update()

        i75.sleep_ms(100)


if __name__ == "__main__":
    main()
