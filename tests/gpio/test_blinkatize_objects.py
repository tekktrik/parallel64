# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests the import objects created due to blinkatize() functionality
"""

import parallel64.ports
import parallel64.gpio
import parallel64.hardware
import parallel64.digitalio


def test_blinkatize_objects():
    port = parallel64.ports.StandardPort(100)
    gpio = parallel64.gpio.GPIO(port)

    gpio.blinkatize()

    import digitalio
    import microcontroller

    assert microcontroller.Pin == parallel64.hardware.Pin

    assert digitalio.DigitalInOut == parallel64.digitalio.DigitalInOut
    assert digitalio.Pull == parallel64.digitalio.Pull
    assert digitalio.Direction == parallel64.digitalio.Direction
    assert digitalio.DriveMode == parallel64.digitalio.DriveMode
