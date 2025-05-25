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

import math
import time

if not hasattr(time, "ticks_ms"):
    def ticks_ms():
        return math.floor(time.time_ns() / 1000000)
    def ticks_diff(t1, t2):
        return t1 - t2
else:
    ticks_ms = time.ticks_ms
    ticks_diff = time.ticks_diff


def profile(func):
    def wrapper(*args, **kwargs):
        start = ticks_ms()
        result = func(*args, **kwargs)
        end = ticks_ms()

        print(f"Function {func.__name__} took {ticks_diff(end, start)} ms")
        #if id(func) not in _PROFILE_CACHE:
        #    _PROFILE_CACHE[id(func)] = []

        #_PROFILE_CACHE[id(func)].append(time.ticks_diff(end, start))
        return result
    return wrapper
