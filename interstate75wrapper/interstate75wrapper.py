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

try:
    import interstate75  # type: ignore
    MOCK = False
except ImportError:
    MOCK = True

from .console_graphics import ConsoleGraphics
from .display_type import DisplayType


class Interstate75Wrapper:
    def __init__(self, display_type: DisplayType) -> None:
        self.display_type = display_type
        if MOCK:
            self.graphics = ConsoleGraphics(self.display_type.width,
                                            self.display_type.height)
        else:
            self.i75 = interstate75.Interstate75(
                display=self.display_type.i75type)
            self.graphics = self.i75.display
