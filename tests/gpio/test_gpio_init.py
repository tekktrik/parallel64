# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests the blinkatize() functionality
"""

import parallel64.ports
import parallel64.gpio
import parallel64.hardware

def test_gpio_init():

    port = parallel64.ports.StandardPort(100)

    try:
        _ = parallel64.gpio.GPIO(port)
    except:
        assert False


def test_gpio_init_typeerror():

    try:
        _ = parallel64.gpio.GPIO(100)
    except TypeError:
        assert True
    else:
        assert False
