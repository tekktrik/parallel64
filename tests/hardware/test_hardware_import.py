# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests import of hardware submodule
"""


def test_hardware_import():
    try:
        import parallel64.hardware
    except:
        assert False
