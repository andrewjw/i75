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

from .screen import Screen


class ScreenWipe(Screen):
    def __init__(self,
                 width: int,
                 height: int,
                 duration: int,
                 first: Screen,
                 second: Screen) -> None:
        self.width = width
        self.height = height
        self.total_time = 0
        self.duration = duration
        self.first = first
        self.second = second

    def is_complete(self):
        return self.total_time >= self.duration
