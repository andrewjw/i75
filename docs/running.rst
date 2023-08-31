=======
Running
=======

---------------
Running On A PC
---------------

To run your script simply follow `i75` with the path to your script. There are examples provided in the `examples`
directory, which can be run as follows.::

    i75 examples/clock/clock.py

-----------------------
Running On Interstate75
-----------------------

To install the library on your Interstate75 run `install.sh`. This will create a `i75` directory on the Raspberry Pi
Zero, and copy across the required files.

Install your script in the normal way, e.g.::

    ampy examples/clock/clock.py main.py

For `ampy` to work you need to tell it the correct device to use to communicate with Raspberry Pi Pico. To that either
run `install.sh -p /dev/tty.usbmodemN` or set the `AMPY_PORT` environment details. For more details about `ampy`,
check out [their documentation](https://github.com/scientifichackers/ampy).
