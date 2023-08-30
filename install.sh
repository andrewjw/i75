#!/bin/bash

ampy -p /dev/tty.usbmodem14201 mkdir i75
ampy -p /dev/tty.usbmodem14201 put i75/__init__.py i75/__init__.py
ampy -p /dev/tty.usbmodem14201 put i75/basei75.py i75/basei75.py
ampy -p /dev/tty.usbmodem14201 put i75/datetime.py i75/datetime.py
ampy -p /dev/tty.usbmodem14201 put i75/display_type.py i75/display_type.py
ampy -p /dev/tty.usbmodem14201 put i75/nativei75.py i75/nativei75.py
ampy -p /dev/tty.usbmodem14201 put i75/pen.py i75/pen.py
