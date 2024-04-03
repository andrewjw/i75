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

class Colour:
    """Manage colours from a 32-bit integer"""
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def r(self) -> int:
        """The red component - 0 to 255."""
        return (self._value >> 24) & 255

    @property
    def g(self) -> int:
        """The green component - 0 to 255."""
        return (self._value >> 16) & 255

    @property
    def b(self) -> int:
        """The blue component - 0 to 255."""
        return (self._value >> 8) & 255

    @property
    def a(self) -> int:
        """The alpha component - 0 to 255."""
        return self._value & 255

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Colour):
            return False
        return self._value == other._value

    def __neq__(self, other: object) -> bool:
        if not isinstance(other, Colour):
            return False
        return self._value != other._value

    @staticmethod
    def fromint32(value: int) -> "Colour":
        """Create a Colour object from a 32-bit integer."""
        return Colour(value)

    @staticmethod
    def fromrgb(r: int, g: int, b: int) -> "Colour":
        """Create a Colour object from three RGB values."""
        return Colour(r << 24 | g << 16 | b << 8 | 255)

    @staticmethod
    def fromrgba(r: int, g: int, b: int, a: int) -> "Colour":
        """Create a Colour object from four RGBA values."""
        return Colour(r << 24 | g << 16 | b << 8 | a)
