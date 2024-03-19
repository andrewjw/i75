# i75

[![Pipeline](https://github.com/andrewjw/i75/actions/workflows/build.yaml/badge.svg)](https://github.com/andrewjw/i75/actions/workflows/build.yaml)
[![PyPI version](https://badge.fury.io/py/i75.svg)](https://pypi.org/project/i75/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/i75)](https://pypi.org/project/i75/)
[![Coverage Status](https://coveralls.io/repos/github/andrewjw/i75/badge.svg?branch=main)](https://coveralls.io/github/andrewjw/i75?branch=main)
[![Documentation Status](https://readthedocs.org/projects/i75/badge/?version=latest)](https://i75.readthedocs.io/en/latest/?badge=latest)

A wrapper around Pimoroni's [interstate75](https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules_py/interstate75.md) library which allows for running locally and easier testing.

This library provides a module, `i75`, which contains additional useful functionality over what is provided by MicroPython
and the Pimoroni libraries. For full details, please [read the documentation](https://i75.readthedocs.io/en/latest).

This library also provides a script, `i75`, which is used when running programs on a normal PC for testing purposes.
This is done by a set of modules which replicate the functionality of the native Interstate75(W) hardware, in particular
using [PyGame](https://www.pygame.org/) to represent a [Hub75 LED matrix](https://thepihut.com/products/rgb-full-colour-led-matrix-panel-2-5mm-pitch-64x64-pixels).

This emulation is far from perfect but hopefully allows a quicker development cycle than deploying to the physical
hardware. In particular, problems may include:

* Full Python3.x is used, so syntactic and semantic differences with MicroPython won't be picked up.
* Your PC is many times more powerful than the RP2040 chip, so CPU limits won't be picked up.
* Our emulation of built-in functionality may be incomplete or incorrect.
* Sensors or additional hardware are not emulated.

Any help improving these limitations is most welcome. Please see [CONTRIBUTING.md](https://github.com/andrewjw/i75/blob/main/CONTRIBUTING.md) for more details.

## Installation

To install this library either check it out from GitHub or install it from [PyPI](https://pypi.org/project/i75/).

    git checkout https://github.com/andrewjw/i75.git
    cd i75
    sudo python3 setup.py install

or

    pip3 install i75

## Running On A PC

To run your script simply follow `i75` with the path to your script. There are examples provided in the `examples`
directory, which can be run as follows.

    i75 examples/clock/clock.py

## Running On Interstate75

To install the library on your Interstate75 run `install.sh`. This will create an `i75` directory on the Raspberry Pi
Zero, and copy across the required files.

Install your script in the normal way, e.g.

    ampy examples/clock/clock.py main.py

For `ampy` to work you need to tell it the correct device to use to communicate with Raspberry Pi Pico. To do that either
run `install.sh -p /dev/tty.usbmodemN` or set the `AMPY_PORT` environment details. For more details about `ampy`,
check out [their documentation](https://github.com/scientifichackers/ampy).

