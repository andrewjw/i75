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
import micropython
try:
    from typing import Any, List, Tuple
except ImportError:
    pass

from .screens.writable_screen import WritableScreen


@micropython.native
def line(screen: WritableScreen,
         x1: int,
         y1: int,
         x2: int,
         y2: int,
         *colour: Any) -> None:
    if x1 == x2:
        for y in range(y1 if y1 < y2 else y2, (y2 if y1 < y2 else y1)+1):
            screen.set_pixel(x1, y, *colour)
        return
    if y1 == y2:
        for x in range(x1 if x1 < x2 else x2, (x2 if x1 < x2 else x1)+1):
            screen.set_pixel(x, y1, *colour)
        return

    # This is Bresenham's Algorithm
    x, y = x1, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    pixel = screen.set_pixel
    if (dy / float(dx)) > 1:
        dx, dy = dy, dx
        x, y = y, x
        x1, y1, x2, y2 = y1, x1, y2, x2
        def pixel(x, y, *colour): return screen.set_pixel(y, x, *colour)

    p = 2*dy - dx

    pixel(x, y, *colour)

    for _ in range(2, dx + 2):
        if p > 0:
            y = y + 1 if y < y2 else y - 1
            p = p + 2 * (dy - dx)
        else:
            p = p + 2 * dy

        x = x + 1 if x < x2 else x - 1

        pixel(x, y, *colour)


@micropython.native
def circle(screen: WritableScreen,
           cx: int,
           cy: int,
           radius: int,
           *colour: Any) -> None:
    d = 3 - 2 * radius
    y = radius
    i = 0
    while i <= y:
        line(screen, cx + i, cy + y, cx + i, cy - y, *colour)
        line(screen, cx - i, cy + y, cx - i, cy - y, *colour)
        line(screen, cx + y, cy + i, cx + y, cy - i, *colour)
        line(screen, cx - y, cy - i, cx - y, cy + i, *colour)

        if d < 0:
            d = d + 4 * i + 6
        else:
            d = d + 4 * (i - y) + 10
            y = y - 1
        i = i + 1


def filled_polygon(screen: WritableScreen,
                   points: List[List[Tuple[float, float]]],
                   *colour: Any) -> None:
    miny, maxy = math.floor(points[0][0][1]), math.ceil(points[0][0][1])
    for contour in points:
        for point in contour:
            if point[1] < miny:
                miny = math.floor(point[1])
            if point[1] > maxy:
                maxy = math.ceil(point[1])

    for y in range(miny, maxy):
        intersections: List[int] = []
        for contour in points:
            for i in range(len(contour)):
                p1 = (int(round(contour[i][0])), int(round(contour[i][1])))
                p2c = contour[(i + 1) % len(contour)]
                p2 = (int(round(p2c[0])), int(round(p2c[1])))
                if p1[1] == p2[1]:
                    continue
                if (p1[1] <= y and p2[1] > y) or (p2[1] <= y and p1[1] > y):
                    x = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                    intersections.append(int(round(x)))

        intersections = sorted(intersections)
        if len(intersections) == 1:
            screen.set_pixel(intersections[0], y, *colour)
        else:
            for i in range(0, len(intersections), 2):
                x1 = intersections[i]
                x2 = intersections[i + 1]
                for x in range(x1, x2):
                    screen.set_pixel(x, y, *colour)
