#!/bin/bash

rm -rf i75/screens/__pycache__

ampy ${@:1} mkdir i75 --exists-okay
ampy ${@:1} mkdir i75/tz --exists-okay
ampy ${@:1} mkdir i75/screens --exists-okay
ampy ${@:1} mkdir i75/fontdata --exists-okay
ampy ${@:1} put i75/__init__.py i75/__init__.py
ampy ${@:1} put i75/basei75.py i75/basei75.py
ampy ${@:1} put i75/colour.py i75/colour.py
ampy ${@:1} put i75/datetime.py i75/datetime.py
ampy ${@:1} put i75/graphics.py i75/graphics.py
ampy ${@:1} put i75/image.py i75/image.py
ampy ${@:1} put i75/nativei75.py i75/nativei75.py
ampy ${@:1} put i75/screen_manager.py i75/screen_manager.py
ampy ${@:1} put i75/text.py i75/text.py
ampy ${@:1} put i75/tz/__init__.py i75/tz/__init__.py
ampy ${@:1} put i75/tz/europe_london.py i75/tz/europe_london.py
ampy ${@:1} put i75/screens i75/screens
ampy ${@:1} put i75/fontdata/cg_pixel_3x5_5.py i75/fontdata/cg_pixel_3x5_5.py
