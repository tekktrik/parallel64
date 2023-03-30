# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests import of gpio submodule
"""

def test_gpio_import():
    try:
        import parallel64.gpio
    except:
        assert False
