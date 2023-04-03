# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.hardware.Pin
"""

import parallel64.ports
import parallel64.gpio
import parallel64.digitalio


def test_Pin_hash():
    port = parallel64.ports.StandardPort(0x378)
    gpio = parallel64.gpio.GPIO(port)
    pin = gpio.D0

    pin_reg = pin.register
    pin_bit = pin.bit_index
    hash_value = pin_reg << 3 | pin_bit

    assert hash(pin) == hash_value


def test_Pin_register():
    register = 100
    port = parallel64.ports.StandardPort(register)
    gpio = parallel64.gpio.GPIO(port)
    pin = gpio.D0

    assert pin.register == register


def test_Pin_bit_index():
    port = parallel64.ports.StandardPort(0x378)
    gpio = parallel64.gpio.GPIO(port)
    pin = gpio.D2

    assert pin.bit_index == 2


def test_Pin_input_allowed():
    port = parallel64.ports.StandardPort(0x378, bidirectional=False)
    gpio = parallel64.gpio.GPIO(port)
    input_pin = gpio.PAPER_OUT
    output_pin = gpio.D4

    assert input_pin.input_allowed
    assert not output_pin.input_allowed


def test_Pin_output_allowed():
    port = parallel64.ports.StandardPort(0x378, bidirectional=False)
    gpio = parallel64.gpio.GPIO(port)
    input_pin = gpio.BUSY
    output_pin = gpio.SELECT_PRINTER

    assert not input_pin.output_allowed
    assert output_pin.output_allowed


def test_Pin_in_use():
    port = parallel64.ports.StandardPort(0x378, bidirectional=False)
    gpio = parallel64.gpio.GPIO(port)
    used_pin = gpio.D5
    unused_pin = gpio.D0
    _ = parallel64.digitalio.DigitalInOut(used_pin)

    assert used_pin.in_use
    assert not unused_pin.in_use
