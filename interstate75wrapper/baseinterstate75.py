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
    from typing import Callable, Optional
except ImportError:
    pass

from .datetime import DateTime
from .display_type import DisplayType


class BaseInterstate75:
    def __init__(self,
                 display_type: DisplayType,
                 stb_invert=False,
                 rotate: int = 0) -> None:
        self.display_type = display_type

    def update(self) -> None:
        raise NotImplementedError()

    def enable_wifi(self,
                    callback: Optional[Callable[[int], None]] = None) -> bool:
        raise NotImplementedError()

    def disable_wifi(self) -> None:
        raise NotImplementedError()

    def set_time(self) -> bool:
        raise NotImplementedError()

    def now(self) -> DateTime:
        raise NotImplementedError()

    def sleep_ms(self, delay: int) -> None:
        raise NotImplementedError()

    def ticks_ms(self) -> int:
        raise NotImplementedError()

    def ticks_diff(self, t1: int, t2: int) -> int:
        raise NotImplementedError()

    @staticmethod
    def is_mock() -> bool:
        raise NotImplementedError()
