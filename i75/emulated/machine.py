#!/usr/bin/env python3
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

import gc
import traceback
import time
import sys
import uuid

import mp_time

time.sleep_ms = mp_time.sleep_ms  # type: ignore[attr-defined]


def print_exception(e: Exception, file=sys.stdout) -> None:
    traceback.print_exception(e, file=file)


sys.print_exception = print_exception  # type: ignore[attr-defined]


def mem_free() -> int:
    return 120000


gc.mem_free = mem_free  # type: ignore[attr-defined]


def unique_id() -> bytes:
    return hex(uuid.getnode()).encode("ascii")


def reset() -> None:
    sys.exit()


def soft_reset() -> None:
    sys.exit()
