#!/bin/bash

ampy ${@:1} mkdir i75 --exists-okay
ampy ${@:1} put i75/__init__.py i75/__init__.py
ampy ${@:1} put i75/basei75.py i75/basei75.py
ampy ${@:1} put i75/datetime.py i75/datetime.py
ampy ${@:1} put i75/graphics.py i75/graphics.py
ampy ${@:1} put i75/nativei75.py i75/nativei75.py
