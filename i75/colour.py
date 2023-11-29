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

from .basei75 import BaseI75


class Colour:
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def r(self) -> int:
        return (self._value >> 24) & 255

    @property
    def g(self) -> int:
        return (self._value >> 16) & 255

    @property
    def b(self) -> int:
        return (self._value >> 8) & 255

    @property
    def a(self) -> int:
        return self._value & 255

    def set_colour(self, i75: BaseI75):
        i75.display.set_pen(i75.display.create_pen(self.r, self.g, self.b))

    @staticmethod
    def fromint32(value) -> "Colour":
        return Colour(value)
