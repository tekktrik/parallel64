# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests import of ports submodule
"""


def test_ports_import():
    try:
        import parallel64.ports
    except:
        assert False
