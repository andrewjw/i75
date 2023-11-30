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

import time

try:
    ticks_diff = time.ticks_diff
    ticks_ms = time.ticks_ms
except AttributeError:
    def ticks_ms():
        return time.time_ns() / 1000000

    def ticks_diff(t1, t2):
        # TODO: Probably need to handle wrap around here.
        return t1 - t2


class DateTime:
    """Represents a specific date and a time."""
    BASE: int = 0

    def __init__(self,
                 year: int,
                 month: int,
                 day: int,
                 weekday: int = 0,
                 hour: int = 0,
                 minute: int = 0,
                 second: int = 0,
                 microsecond: int = 0) -> None:
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return False
        return self.year == other.year \
            and self.month == other.month \
            and self.day == other.day \
            and self.hour == other.hour \
            and self.minute == other.minute \
            and self.second == other.second

    def __str__(self):
        return f"{self.year}-{self.month:02n}-{self.day:02n} " \
             + f"{self.hour:02n}:{self.minute:02n}:{self.second:02n}"
