#!/bin/bash

ampy ${@:2} mkdir i75
ampy ${@:2} put i75/__init__.py i75/__init__.py
ampy ${@:2} put i75/basei75.py i75/basei75.py
ampy ${@:2} put i75/datetime.py i75/datetime.py
ampy ${@:2} put i75/display_type.py i75/display_type.py
ampy ${@:2} put i75/nativei75.py i75/nativei75.py
ampy ${@:2} put i75/pen.py i75/pen.py
