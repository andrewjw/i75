=========
About i75
=========

`i75` is a wrapper around Pimoroni's [interstate75](https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules_py/interstate75.md) library which allows for running locally and easier testing.

This library provides a module, `i75`, which contains additional useful functionality over what is provided by MicroPython
and the Pimoroni libraries. For full details, please [read the documentation](https://i75.readthedocs.io/en/latest).

This library also provides a script, `i75`, which is used when running programs on a normal PC for testing purposes.
This done by a set of modules which replicate the functionality of the native Interstate75(W) hardware, in particular
using [PyGame](https://www.pygame.org/) to represent a [Hub75 LED matrix](https://thepihut.com/products/rgb-full-colour-led-matrix-panel-2-5mm-pitch-64x64-pixels).

This is emulation is far from perfect, but hopefully allows a quicker development cycle than deploying to the physical
hardware. In particular problems may include:

* Full Python3.x is used, so syntatic and sematic differences with MicroPython won't be picked up.
* Your PC is many times more powerful than the RP2040 chip, so CPU limits won't be picked up.
* Our emulation of built-in functionality may be incomplete or incorrect.
* Sensors or additional hardware is not emulated.

Any help improving these limitations is most welcome. Please see [CONTRIBUTING.md](https://github.com/andrewjw/i75/blob/main/CONTRIBUTING.md) for more details.
