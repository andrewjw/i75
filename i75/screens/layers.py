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
    from typing import Callable, List
except ImportError:
    pass

from ..colour import Colour
from .screen import Screen


class Layers(Screen):
    def __init__(self,
                 bgcolour: Colour,
                 layers: List[Screen]) -> None:
        self.bgcolour = bgcolour
        self.layers = layers

    def get_pixel(self, x: int, y: int) -> Colour:
        for layer in self.layers[::-1]:
            pixel = layer.get_pixel(x, y)
            if pixel.a == 255:  # TODO: Handle partial transparency
                return pixel
        return self.bgcolour

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        for layer in self.layers:
            layer.update(frame_time, mark_dirty)
