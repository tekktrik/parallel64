# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.digitalio.DigitalInOut
"""

import parallel64.ports
import parallel64.gpio
import parallel64.digitalio


def test_DigitalInOut_init():
    port = parallel64.ports.StandardPort(100)
    gpio = parallel64.gpio.GPIO(port)

    try:
        _ = parallel64.digitalio.DigitalInOut(gpio.D0)
    except:
        assert False


def test_DigitalInOut_init_typeerror():
    try:
        _ = parallel64.digitalio.DigitalInOut(100)
    except TypeError:
        assert True
    else:
        assert False
