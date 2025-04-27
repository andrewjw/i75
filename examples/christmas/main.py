#!/usr/bin/env micropython
# i75
# Copyright (C) 2024 Andrew Wilkinson
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

try:
    from typing import Callable, List, Tuple, cast
except ImportError:  # pragma: no cover
    def cast(t, x):  # type: ignore
        return x

import random

import picographics

from i75 import Date, Colour, Face, Font, I75, Image, SingleColourImage, \
                ScreenManager, render_text, text_boundingbox
from i75.screens.layers import Layers
from i75.screens.offset import Offset
from i75.screens.screen import Screen
from i75.screens.sprite_instance import SpriteInstance
from i75.screens.scale import Scale
from i75.screens.single_bit_screen import SingleBitScreen
from i75.screens.single_colour import SingleColour

FONT = "tiny5.af"

NUMBER_SCALE = 4


class Snowflake(SpriteInstance):
    def __init__(self,
                 colour: Colour,
                 image: SingleColourImage) -> None:
        super().__init__(random.randint(10, 55),
                         random.randint(0, 60),
                         colour,
                         image)

        self._dir = 1 if random.randint(0, 1) == 1 else -1
        self._bounce = random.randint(3, 10)
        self._delay = 0
        self._speed = random.randint(50, 300)

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        self._delay += frame_time
        if self._delay > self._speed:
            self._delay -= self._speed
            self._bounce -= 1
            if self._bounce < 0:
                self._dir = -self._dir
                self._bounce = 10

            self.move_to(self._offset_x + self._dir, self._offset_y + 1)

            if self._offset_y > 64:
                self.move_to(random.randint(10, 55), -self.height)

        super().update(frame_time, mark_dirty)


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64,
        rotate=0 if I75.is_emulated() else 90)

    i75.enable_wifi()
    i75.set_time()

    face = Face.load_face(FONT)
    font = Font(face, 7)

    black = Colour.fromrgb(0, 0, 0)
    red = Colour.fromrgb(255, 50, 50)
    white = Colour.fromrgb(255, 255, 255)

    manager = ScreenManager(64, 64, i75.display)

    today = i75.now().date()
    christmas = Date(today.year, 12, 25)

    days_to_go = (christmas - today).days

    width, height = text_boundingbox(font, str(days_to_go))
    scale = 4 if len(str(days_to_go)) <= 2 else 3
    number_offset_x = 32 - int(scale * (width / 2))
    days = SingleBitScreen(width, height, red)
    render_text(days, font, 0, 0, str(days_to_go))

    width, height = text_boundingbox(font, "sleeps to go")
    sleeps_offset_x = 32 - int(width / 2)
    sleeps = SingleBitScreen(width, height, red)
    render_text(sleeps, font, 0, 0, "sleeps to go")

    snowflake_image = cast(SingleColourImage,
                           Image.load(open("snowflake.i75", "rb")))

    snowflakes = []
    for _ in range(10):
        snowflakes.append(Snowflake(white,
                                    snowflake_image))

    sprites: List[Screen] = []
    sprites.append(Offset(sleeps_offset_x, 40, sleeps))
    sprites.append(Offset(number_offset_x, 10, Scale(scale, days)))
    sprites.extend(snowflakes)
    screen = Layers(black, sprites)

    manager.set_screen(screen)

    base_ticks = i75.ticks_ms()
    while True:
        now = i75.ticks_ms()
        frame_time = i75.ticks_diff(now, base_ticks)
        base_ticks = now

        manager.update(frame_time)


if __name__ == "__main__":
    main()
