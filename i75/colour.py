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

import micropython

CACHE_SIZE = 256


class Colour:
    """Manage colours from a 32-bit integer"""
    def __init__(self, value: int) -> None:
        self._value = value
        self._rgb = bytearray([self.r, self.g, self.b])
        self.is_transparent = value & 255 != 255

    def mix(self, other: "Colour") -> "Colour":
        """Mix this colour with another colour."""
        assert self.a == 255, "Base colour must be opaque"
        if other.a == 255:
            return other
        oratio = other.a / 255.0
        sratio = 1.0 - oratio
        r = round(self.r * sratio + other.r * oratio)
        g = round(self.g * sratio + other.g * oratio)
        b = round(self.b * sratio + other.b * oratio)
        return Colour.fromrgb(r, g, b)

    @property
    @micropython.native
    def r(self) -> int:
        """The red component - 0 to 255."""
        return (self._value >> 24) & 255

    @property
    @micropython.native
    def g(self) -> int:
        """The green component - 0 to 255."""
        return (self._value >> 16) & 255

    @property
    @micropython.native
    def b(self) -> int:
        """The blue component - 0 to 255."""
        return (self._value >> 8) & 255

    @property
    @micropython.native
    def a(self) -> int:
        """The alpha component - 0 to 255."""
        return self._value & 255

    @micropython.native
    def rgb(self) -> bytearray:
        """Return the RGB components as a bytes object."""
        return bytearray([self.r, self.g, self.b])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Colour):
            return False
        return self._value == other._value

    def __neq__(self, other: object) -> bool:
        if not isinstance(other, Colour):
            return False
        return self._value != other._value

    def __str__(self) -> str:
        return f"<Colour {self.r} {self.g} {self.b} {self.a}>"

    @staticmethod
    @micropython.native
    def fromint32(value: int) -> "Colour":
        """Create a Colour object from a 32-bit integer."""
        return Colour(value)

    @staticmethod
    @micropython.native
    def fromrgb(r: int, g: int, b: int) -> "Colour":
        """Create a Colour object from three RGB values."""
        return Colour(r << 24 | g << 16 | b << 8 | 255)

    @staticmethod
    @micropython.native
    def fromrgba(r: int, g: int, b: int, a: int) -> "Colour":
        """Create a Colour object from four RGBA values."""
        if a == 0:
            return TRANSPARENT
        return Colour(r << 24 | g << 16 | b << 8 | a)

    @staticmethod
    @micropython.native
    def frombytearray(bytes: bytearray) -> "Colour":
        """Create a Colour object from three RGB values."""
        return Colour(bytes[0] << 24
                      | bytes[1] << 16
                      | bytes[2] << 8
                      | (255 if len(bytes) == 3 else bytes[3]))


TRANSPARENT = Colour.fromint32(0)
