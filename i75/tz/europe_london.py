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

from ..datetime import DateTime, TimeDelta


class EuropeLondon:
    @staticmethod
    def to_localtime(dt: DateTime) -> DateTime:
        if dt.month < 3 or dt.month > 10:
            return dt
        if dt.month > 3 and dt.month < 10:
            return dt + TimeDelta(hours=1)
        if dt.month == 3:
            last_day = DateTime(dt.year, 3, 31)
            while last_day.weekday() != 6:
                last_day -= TimeDelta(days=1)
            if dt.day < last_day.day:
                return dt
            if dt.day > last_day.day:
                return dt + TimeDelta(hours=1)
            return dt + TimeDelta(hours=1) if dt.hour > 1 else dt
        else:
            last_day = DateTime(dt.year, 10, 31)
            while last_day.weekday() != 6:
                last_day -= TimeDelta(days=1)
            if dt.day < last_day.day:
                return dt + TimeDelta(hours=1)
            if dt.day > last_day.day:
                return dt
            return dt if dt.hour > 1 else dt + TimeDelta(hours=1)

    @staticmethod
    def to_utc(dt: DateTime) -> DateTime:
        if dt.month < 3 or dt.month > 10:
            return dt
        if dt.month > 3 and dt.month < 10:
            return dt - TimeDelta(hours=1)
        if dt.month == 3:
            last_day = DateTime(dt.year, 3, 31)
            while last_day.weekday() != 6:
                last_day -= TimeDelta(days=1)
            if dt.day < last_day.day:
                return dt
            if dt.day > last_day.day:
                return dt - TimeDelta(hours=1)
            return dt - TimeDelta(hours=1) if dt.hour > 1 else dt
        else:
            last_day = DateTime(dt.year, 10, 31)
            while last_day.weekday() != 6:
                last_day -= TimeDelta(days=1)
            if dt.day < last_day.day:
                return dt - TimeDelta(hours=1)
            if dt.day > last_day.day:
                return dt
            return dt if dt.hour > 1 else dt - TimeDelta(hours=1)
