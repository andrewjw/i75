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
try:
    from typing import Tuple
except ImportError:
    pass
import sys

import picographics

from i75 import Colour, DateTime, I75, line
from i75.screens.layers import Layers
from i75.screens.single_bit_screen import SingleBitScreen
from i75.screens.single_colour import SingleColour
from i75.screen_manager import ScreenManager
from i75.tz import EuropeLondon

HOUR_LENGTH = 25
MINUTE_LENGTH = 30
SECOND_LENGTH = 30


def get_center_point(angle) -> Tuple[int, int]:
    if angle < math.pi / 2:
        return (32, 31)
    if angle < math.pi:
        return (32, 32)
    if angle < 2 * math.pi / 3:
        return (31, 32)
    return (31, 31)


# This currently has issues due to the i75 working in single precision
# floats, and Python3 using doubles.
def render_clock_face(screen: SingleBitScreen) -> None:
    for tick in range(12):
        tick_len = 3 if tick in (0, 3, 6, 9) else 3
        angle = 2 * math.pi * tick / 12.0
        cx, cy = get_center_point(angle)
        x1 = math.floor((31 - tick_len) * math.cos(angle) + cx)
        y1 = math.floor((31 - tick_len) * math.sin(angle) + cy)
        x2 = math.floor(31 * math.cos(angle) + cx)
        y2 = math.floor(31 * math.sin(angle) + cy)

        line(screen, x1, y1, x2, y2, 2, True)

    line(screen, 32, 3, 32, 0, True)
    line(screen, 31, 60, 31, 63, True)
    line(screen, 0, 31, 3, 31, True)
    line(screen, 60, 32, 63, 32, True)


SECOND_HAND = (0, 0, 0, 0)
MINUTE_HAND = (0, 0, 0, 0)
HOUR_HAND = (0, 0, 0, 0)


def calculate_hand(length: int, percent: float) -> Tuple[int, int, int, int]:
    angle = 2 * math.pi * percent
    cx, cy = get_center_point(angle)
    x = math.floor(length * math.sin(angle) + cx)
    y = math.floor(length * -math.cos(angle) + cy)
    return (cx, cy, x, y)


def render_hand(screen: SingleBitScreen,
                hand: Tuple[int, int, int, int],
                set_pixel: bool) -> None:
    line(screen,
         hand[0],
         hand[1],
         hand[2],
         hand[3],
         set_pixel)


def render_clock(hour_screen: SingleBitScreen,
                 minute_screen: SingleBitScreen,
                 second_screen: SingleBitScreen,
                 now: DateTime,
                 subsecond: int) -> None:
    global HOUR_HAND, MINUTE_HAND, SECOND_HAND

    part_second = subsecond / 1000.0
    second_hand = calculate_hand(SECOND_LENGTH,
                                 (now.second + part_second) / 60.0)
    if SECOND_HAND != second_hand:
        render_hand(second_screen, SECOND_HAND, False)
        render_hand(second_screen, second_hand, True)
        SECOND_HAND = second_hand

    minute_percent = (now.minute * 60
                      + now.second
                      + part_second) / (60.0 * 60)
    minute_hand = calculate_hand(MINUTE_LENGTH, minute_percent)
    if MINUTE_HAND != minute_hand:
        render_hand(minute_screen, MINUTE_HAND, False)
        render_hand(minute_screen, minute_hand, True)
        MINUTE_HAND = minute_hand

    hour_percent = ((now.hour % 12) * (60 * 60)
                    + now.minute * 60
                    + now.second + part_second) / (60.0 * 60 * 12)
    hour_hand = calculate_hand(HOUR_LENGTH, hour_percent)
    if HOUR_HAND != hour_hand:
        render_hand(hour_screen, HOUR_HAND, False)
        render_hand(hour_screen, hour_hand, True)
        HOUR_HAND = hour_hand


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    i75.enable_wifi()
    i75.set_time()
    next_ntp = i75.now().hour + 23
    base_ticks = i75.ticks_ms()

    white = Colour.fromrgb(255, 255, 255)
    red = Colour.fromrgb(255, 0, 0)
    black = Colour.fromrgb(0, 0, 0)

    clockface = SingleBitScreen(64, 64, white)
    hour_hand = SingleBitScreen(64, 64, white)
    minute_hand = SingleBitScreen(64, 64, white)
    second_hand = SingleBitScreen(64, 64, red)

    manager = ScreenManager(64, 64, i75.display)
    manager.set_screen(Layers(black,
                              [clockface,
                               hour_hand,
                               minute_hand,
                               second_hand]))

    render_clock_face(clockface)

    old_time = i75.now()
    old_subsecond = 0

    while True:
        now = EuropeLondon.to_localtime(i75.now())
        subsecond = i75.ticks_diff(i75.ticks_ms(), base_ticks) % 1000

        if now.hour == next_ntp:
            i75.set_time()
            now = i75.now()
            next_ntp = now.hour + 23

        if now != old_time and subsecond > old_subsecond and subsecond < 9975:
            base_ticks -= 25
        elif now == old_time and subsecond < old_subsecond:
            base_ticks += 25
            subsecond = 999

        render_clock(hour_hand,
                     minute_hand,
                     second_hand,
                     now,
                     subsecond)
        old_time = now
        old_subsecond = subsecond

        manager.update(100)

        i75.sleep_ms(100)


if __name__ == "__main__":
    main()
