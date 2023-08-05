# Remote I2C

A SMBus class-compatible TCP proxy allowing you to host or connect to a Remote I2C
session with minimal effort.

My use case for writing this module is to allow me to work with I2C on a Raspberry Pi
that is on my network, without having to install anything that takes up too much memory
or processing power. I serve this thin SMBus server module on the Pi, then I can develop
as I please on my computer and interact with the I2C bus as if it was on my own machine.



# Important Notes

This module was developed:
* quickly
* without tests
* for the purpose of development

It is NOT:
* a replacement for an actual local I2C connection (*particularly* for real-time comms)
* guaranteed to be free of bugs
* suitable for production use (unless you're happy to take your chances)



# Install

Install with pip:

```bash
pip install remote-i2c
```



# Example

## On the I2C Host (e.g., Raspberry Pi)

1. Ensure that I2C is enabled! (```sudo raspi-config```)
1. Ensure that the user you're operating under has permission to access the I2C hardware! (e.g., part of the i2c group)
1. Run the remote-i2c module directly with the python interpreter from the command line:
    ```bash
    python3 -m remote_i2c
    ```
1. Alternatively, run the module from a python script:
    ```python
    #!/usr/bin/env python3

    # Import the RemoteI2CServer class
    from remote_i2c import RemoteI2CServer

    # Create the server (see docstring for additional args)
    server = RemoteI2CServer()

    # Start the server (blocks forever!)
    server.serve()
    ```


## On the I2C Client (e.g., Desktop/Laptop)

```python
#!/usr/bin/env python3

# Import the RemoteI2CClient class
from remote_i2c import RemoteI2CClient

# Connect to the I2C Host (see docstring for additional args)
remote_i2c_host = '192.168.1.2'
bus = RemoteI2CClient(remote_i2c_host)
bus.connect()

# Perform I2C operations as you normally would with SMBus2
addr = 0x67
reg = 0xf2
value = bus.read_byte_data(addr, reg)
bus.write_byte_data(addr, reg, value + 1 % 0xff)

# Disconnect when you're done, if you feel the need
bus.disconnect()
```



# Author

Daniel 'Vector' Kerr (<vector@vector.id.au> | [https://vector.id.au](https://vector.id.au))



# License

Copyright © 2019 Daniel 'Vector' Kerr (<vector@vector.id.au>)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.