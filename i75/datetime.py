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
    from typing import Tuple
except ImportError:
    pass

try:
    ticks_diff = time.ticks_diff
    ticks_ms = time.ticks_ms
except AttributeError:
    def ticks_ms():
        return time.time_ns() / 1000000

    def ticks_diff(t1, t2):
        # TODO: Probably need to handle wrap around here.
        return t1 - t2


def _is_leap_year(year: int) -> bool:
    if year % 100 == 0:
        return year % 400 == 0
    return year % 4 == 0


def _days_in_month(year: int, month: int) -> int:
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        return 29 if _is_leap_year(year) else 28
    return 31


class Date:
    """Represents a specific date."""
    def __init__(self, year: int, month: int, day: int):
        assert year >= 1970, "Dates before 1970 are not supported."
        assert month >= 1 and month <= 12, f"Month {month} out of range."
        assert day >= 1 and day <= _days_in_month(year, month), \
            f"Day {day} out of range for {year} {month}."
        self.__days_since_1970 = (year - 1970) * 365
        for i in range(1970, year):
            if _is_leap_year(i):
                self.__days_since_1970 += 1
        for m in range(1, month):
            self.__days_since_1970 += _days_in_month(year, m)
        self.__days_since_1970 += day

    def __year_month_day(self) -> Tuple[int, int, int]:
        y, m, d = 1970, 1, self.__days_since_1970
        while d > (366 if _is_leap_year(y) else 365):
            d -= (366 if _is_leap_year(y) else 365)
            y += 1
        while d > _days_in_month(y, m):
            d -= _days_in_month(y, m)
            m += 1
        return y, m, d

    def weekday(self) -> int:
        """Returns the day of the week. 0 is Monday, 6 is Sunday."""
        return ((self.__days_since_1970 % 7) + 2) % 7

    def __iadd__(self, days: int) -> "Date":
        self.__days_since_1970 += days
        return self

    def __isub__(self, days: int) -> "Date":
        self.__days_since_1970 -= days
        return self

    @property
    def year(self) -> int:
        return self.__year_month_day()[0]

    @property
    def month(self) -> int:
        return self.__year_month_day()[1]

    @property
    def day(self) -> int:
        return self.__year_month_day()[2]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return False
        return self.__days_since_1970 == other.__days_since_1970


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
        self.__date = Date(year, month, day)
        self.hour = hour
        self.minute = minute
        self.second = second

    def weekday(self) -> int:
        """Returns the day of the week. 0 is Monday, 6 is Sunday."""
        return self.__date.weekday()

    @property
    def year(self) -> int:
        return self.__date.year

    @property
    def month(self) -> int:
        return self.__date.month

    @property
    def day(self) -> int:
        return self.__date.day

    def __add__(self, other: "TimeDelta") -> "DateTime":
        dt = DateTime(self.year,
                      self.month,
                      self.day,
                      hour=self.hour,
                      minute=self.minute,
                      second=self.second)
        dt.second += other.seconds
        while dt.second > 60:
            dt.minute += 1
            dt.second -= 60
        while dt.minute > 60:
            dt.hour += 1
            dt.minute -= 60
        dt.hour += other.hours
        while dt.hour > 24:
            dt.__date += 1
            dt.hour -= 24
        dt.__date += other.days
        return dt

    def __iadd__(self, other: "TimeDelta") -> "DateTime":
        self.second += other.seconds
        while self.second > 60:
            self.minute += 1
            self.second -= 60
        while self.minute > 60:
            self.hour += 1
            self.minute -= 60
        self.hour += other.hours
        while self.hour > 24:
            self.__date += 1
            self.hour -= 24
        self.__date += other.days
        return self

    def __sub__(self, other: "TimeDelta") -> "DateTime":
        dt = DateTime(self.year,
                      self.month,
                      self.day,
                      hour=self.hour,
                      minute=self.minute,
                      second=self.second)
        dt.second -= other.seconds
        while dt.second < 0:
            dt.minute -= 1
            dt.second += 60
        while dt.minute < 0:
            dt.hour -= 1
            dt.minute += 60
        dt.hour -= other.hours
        while dt.hour < 0:
            dt.__date -= 1
            dt.hour += 24
        dt.__date -= other.days
        return dt

    def __isub__(self, other: "TimeDelta") -> "DateTime":
        self.second -= other.seconds
        while self.second < 0:
            self.minute -= 1
            self.second += 60
        while self.minute < 0:
            self.hour -= 1
            self.minute += 60
        self.hour -= other.hours
        while self.hour < 24:
            self.__date -= 1
            self.hour += 24
        self.__date -= other.days
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return False
        return self.__date == other.__date \
            and self.hour == other.hour \
            and self.minute == other.minute \
            and self.second == other.second

    def __str__(self):
        return f"{self.year}-{self.month:02n}-{self.day:02n} " \
             + f"{self.hour:02n}:{self.minute:02n}:{self.second:02n}"

    def __repr__(self):
        return f"{self.year}-{self.month:02n}-{self.day:02n} " \
             + f"{self.hour:02n}:{self.minute:02n}:{self.second:02n}"


class TimeDelta:
    """Represents a difference between two times."""
    def __init__(self,
                 days: int = 0,
                 hours: int = 0,
                 seconds: int = 0) -> None:
        self.days = days
        self.hours = hours
        self.seconds = seconds
