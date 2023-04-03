# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests settings of various pins with parallel64.digitalio.DigitalInOut
"""

import parallel64.ports
import parallel64.gpio
from parallel64.digitalio import DigitalInOut, Direction, Pull, DriveMode

from digitalio_DigitalInOut_matrix import dio_test_settings


def test_DigitalInOut_unidirectional_data_pins():
    port_uni = parallel64.ports.StandardPort(0x378, bidirectional=False)
    gpio_uni = parallel64.gpio.GPIO(port_uni)

    data_pin_uni = gpio_uni.D0
    data_dio_uni = DigitalInOut(data_pin_uni)

    settings = {
        "input": ValueError,
        "output": {
            "pull": {
                "get": AttributeError,
                "set": [
                    (Pull.UP, AttributeError),
                    (Pull.DOWN, AttributeError),
                    (None, AttributeError),
                ],
            },
            "drive_mode": {
                "get": None,
                "set": [
                    (DriveMode.PUSH_PULL, None),
                    (DriveMode.OPEN_DRAIN, ValueError),
                ],
            },
            "value": {"get": None, "set": [(True, None), (False, None)]},
        },
    }

    dio_test_settings(data_dio_uni, settings)


def test_DigitalInOut_bidirectional_data_pins():
    port_bi = parallel64.ports.StandardPort(0x378, bidirectional=True)
    gpio_bi = parallel64.gpio.GPIO(port_bi)

    data_pin_bi = gpio_bi.D0
    data_dio_bi = DigitalInOut(data_pin_bi)

    settings = {
        "input": {
            "pull": {
                "get": None,
                "set": [(Pull.UP, ValueError), (Pull.DOWN, ValueError), (None, None)],
            },
            "drive_mode": {
                "get": AttributeError,
                "set": [
                    (DriveMode.PUSH_PULL, None),
                    (DriveMode.OPEN_DRAIN, ValueError),
                ],
            },
            "value": {
                "get": None,
                "set": [(True, AttributeError), (False, AttributeError)],
            },
        },
        "output": {
            "pull": {
                "get": AttributeError,
                "set": [
                    (Pull.UP, AttributeError),
                    (Pull.DOWN, AttributeError),
                    (None, AttributeError),
                ],
            },
            "drive_mode": {
                "get": None,
                "set": [
                    (DriveMode.PUSH_PULL, None),
                    (DriveMode.OPEN_DRAIN, ValueError),
                ],
            },
            "value": {"get": None, "set": [(True, None), (False, None)]},
        },
    }

    dio_test_settings(data_dio_bi, settings)


def test_DigitalInOut_status_pins():
    port = parallel64.ports.StandardPort(0x378, bidirectional=True)
    gpio = parallel64.gpio.GPIO(port)

    status_pin = gpio.ACK
    status_dio = DigitalInOut(status_pin)

    settings = {
        "input": {
            "pull": {
                "get": None,
                "set": [(Pull.UP, ValueError), (Pull.DOWN, ValueError), (None, None)],
            },
            "drive_mode": {
                "get": AttributeError,
                "set": [
                    (DriveMode.PUSH_PULL, None),
                    (DriveMode.OPEN_DRAIN, ValueError),
                ],
            },
            "value": {
                "get": None,
                "set": [(True, AttributeError), (False, AttributeError)],
            },
        },
        "output": ValueError,
    }

    dio_test_settings(status_dio, settings)


def test_DigitalInOut_control_pins():
    port = parallel64.ports.StandardPort(0x378, bidirectional=True)
    gpio = parallel64.gpio.GPIO(port)

    control_pin = gpio.STROBE
    control_dio = DigitalInOut(control_pin)

    settings = {
        "input": {
            "pull": {
                "get": None,
                "set": [(Pull.UP, None), (Pull.DOWN, ValueError), (None, ValueError)],
            },
            "drive_mode": {
                "get": AttributeError,
                "set": [
                    (DriveMode.PUSH_PULL, ValueError),
                    (DriveMode.OPEN_DRAIN, None),
                ],
            },
            "value": {
                "get": None,
                "set": [(True, AttributeError), (False, AttributeError)],
            },
        },
        "output": {
            "pull": {
                "get": AttributeError,
                "set": [
                    (Pull.UP, AttributeError),
                    (Pull.DOWN, AttributeError),
                    (None, AttributeError),
                ],
            },
            "drive_mode": {
                "get": None,
                "set": [
                    (DriveMode.PUSH_PULL, ValueError),
                    (DriveMode.OPEN_DRAIN, None),
                ],
            },
            "value": {"get": None, "set": [(True, None), (False, None)]},
        },
    }

    dio_test_settings(control_dio, settings)
