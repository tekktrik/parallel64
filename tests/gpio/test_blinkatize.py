# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

import parallel64.ports
import parallel64.gpio

def test_blinkatize():

    port = parallel64.ports.StandardPort(100)
    gpio = parallel64.gpio.GPIO(port)

    gpio.blinkatize()

    try:
        import board
        import digitalio
        #import busio
    except:
        assert False
