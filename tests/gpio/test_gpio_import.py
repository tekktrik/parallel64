# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests the blinkatize() functionality
"""

def test_gpio_import():
    try:
        import parallel64.gpio
    except:
        assert False
