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


def test_DigitalInOut_switch_io():
    port = parallel64.ports.StandardPort(100, bidirectional=True)
    gpio = parallel64.gpio.GPIO(port)

    dio = parallel64.digitalio.DigitalInOut(gpio.D0)
    dio.direction = parallel64.digitalio.Direction.INPUT

    if dio.direction != parallel64.digitalio.Direction.INPUT:
        assert False

    try:
        dio.switch_to_output()
    except:
        assert False

    if dio.direction != parallel64.digitalio.Direction.OUTPUT:
        assert False

    try:
        dio.switch_to_input()
    except:
        assert False

    if dio.direction != parallel64.digitalio.Direction.INPUT:
        assert False
