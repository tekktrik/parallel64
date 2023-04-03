# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests the blinkatize() functionality
"""

import parallel64.ports
import parallel64.gpio


def test_blinkatize():
    port = parallel64.ports.StandardPort(0x378)
    gpio = parallel64.gpio.GPIO(port)

    gpio.blinkatize()

    try:
        import board
        import digitalio
        import microcontroller

        # import busio
    except:
        assert False
