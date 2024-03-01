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

import _thread
import picographics
import time

from i75 import I75

LOCK = _thread.allocate_lock()


def second_thread() -> None:
    i = 0
    while True:
        with LOCK:
            print(f"Second thread: {i}")
        i += 1

        time.sleep_ms(500)


def main() -> None:
    i75 = I75(
        display_type=picographics.DISPLAY_INTERSTATE75_64X64)

    _thread.start_new_thread(second_thread, ())

    i = 0
    while True:
        with LOCK:
            print(f"First thread: {i}")
        i += 1

        time.sleep_ms(300)


if __name__ == "__main__":
    main()
