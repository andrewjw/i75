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
    from typing import Callable, List, Sequence
except ImportError:
    pass

from ..colour import Colour, TRANSPARENT
from .screen import Screen


class Layers(Screen):
    def __init__(self,
                 bgcolour: Colour,
                 layers: Sequence[Screen]) -> None:
        self.bgcolour = bgcolour
        self.layers = list(layers)

    def release(self):
        for layer in self.layers:
            layer.release()

    def get_pixel(self, x: int, y: int) -> Colour:
        i = len(self.layers) - 1
        colours: List[Colour] = []
        while i >= 0:
            c = self.layers[i].get_pixel(x, y)
            if c.a == 255:
                colours.insert(0, c)
                break
            elif c.a == 0:
                pass
            else:
                colours.insert(0, c)

            i -= 1

        if i == -1:
            colours.insert(0, self.bgcolour)

        c = colours[0]
        for px in colours[1:]:
            c = c.mix(px)
        return c

    def update(self,
               frame_time: int,
               mark_dirty: Callable[[int, int], None]) -> None:
        for layer in self.layers:
            layer.update(frame_time, mark_dirty)

    def add_layer(self, screen: Screen) -> None:
        self.layers.append(screen)
