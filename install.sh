#!/bin/bash

ampy -p /dev/tty.usbmodem14201 mkdir interstate75wrapper
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/__init__.py interstate75wrapper/__init__.py
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/baseinterstate75.py interstate75wrapper/baseinterstate75.py
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/datetime.py interstate75wrapper/datetime.py
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/display_type.py interstate75wrapper/display_type.py
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/nativeinterstate75.py interstate75wrapper/nativeinterstate75.py
ampy -p /dev/tty.usbmodem14201 put interstate75wrapper/pen.py interstate75wrapper/pen.py
