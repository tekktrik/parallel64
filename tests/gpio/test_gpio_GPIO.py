# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.gpio.GPIO
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


def test_gpio_properties():

    port = parallel64.ports.StandardPort(100)
    gpio = parallel64.gpio.GPIO(port)

    assert hasattr(gpio, "D0")
    assert hasattr(gpio, "D1")
    assert hasattr(gpio, "D2")
    assert hasattr(gpio, "D3")
    assert hasattr(gpio, "D4")
    assert hasattr(gpio, "D5")
    assert hasattr(gpio, "D6")
    assert hasattr(gpio, "D7")

    assert hasattr(gpio, "ACK")
    assert hasattr(gpio, "BUSY")
    assert hasattr(gpio, "PAPER_OUT")
    assert hasattr(gpio, "SELECT_IN")
    assert hasattr(gpio, "ERROR")

    assert hasattr(gpio, "STROBE")
    assert hasattr(gpio, "AUTO_LINEFEED")
    assert hasattr(gpio, "INITIALIZE")
    assert hasattr(gpio, "SELECT_PRINTER")

    assert(isinstance(gpio.port_id, str))
    assert(gpio.port_id == gpio.board_id)


def test_gpio_pintype():

    port = parallel64.ports.StandardPort(100)
    gpio = parallel64.gpio.GPIO(port)

    assert isinstance(gpio.D0, parallel64.hardware.Pin)

