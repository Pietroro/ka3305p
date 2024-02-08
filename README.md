# K(A/D)3305P
Python3 library for USB serial control of the RND LAB 320-KA3305P/320-KD3305P power supply.

## KA3305P

The `ka3305pInstrument` class uses the python `serial` package which allows for communication with serial devices through `write` and `read`. The communication properties (BaudRate, Terminator, etc.) are set when invoking the serial object with `serial.Serial(...)`. For the RND LAB 320-KA3305P power supply: baud rate to 9600, 8 data bits, no parity, 1 stop bit.

## KD3305P
The `kd3305pInstrument` class is virtually identical to the class above, with the only difference being the channels being individually controllable, and the syntax of the serial commands being slightly different.

### Requires
The following python packages are required by the class. 

* serial

### Ubuntu 20.04 installation
* Install the serial requirement
    ```bash
    pip3 install pyserial
    ```
* To enable non-root-access communication with the RND lab Power Supply:
    * Find out the USERNAME using the `whoami` command
    * Add user to the "tty and "dialout" groups 
    ```bash
    usermod -a -G dialout USERNAME
    usermod -a -G tty USERNAME
    ```

