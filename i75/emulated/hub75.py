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

import math
from typing import List, Optional, Tuple

import pygame

import picographics

LED_SIZE = 10


class ColorOrder:
    pass


class Hub75:
    def __init__(self,
                 width: int,
                 height: int,
                 panel_type: "PanelType",
                 stb_invert: bool,
                 color_order: ColorOrder):
        pygame.init()
        self.screen = \
            pygame.display.set_mode((width * LED_SIZE,
                                     height * LED_SIZE))

        self._width, self._height = width, height
        self._buffer: List[List[Optional[Tuple[int, int, int]]]] = []
        for _ in range(height):
            self._buffer.append([None] * width)

    def start(self) -> None:
        pass

    def update(self, buffer: picographics.PicoGraphics) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt()

        for y in range(self._height):
            for x in range(self._width):
                if buffer._buffer[y][x] != self._buffer[y][x]:
                    centre = (math.floor(x * LED_SIZE + LED_SIZE/2),
                              math.floor(y * LED_SIZE + LED_SIZE/2))
                    colour = buffer._buffer[y][x]
                    if colour is None:
                        colour = (0, 0, 0)
                    pygame.draw.circle(self.screen,
                                       colour,
                                       centre,
                                       LED_SIZE/2)

        pygame.display.flip()


class PanelType:
    pass


PANEL_GENERIC = PanelType()

COLOR_ORDER_RGB = ColorOrder()
