# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.ports.EnhancedPort
"""

import parallel64.ports


def test_EnhancedPort_init():
    try:
        _ = parallel64.ports.EnhancedPort(100)
    except:
        assert False


def test_EnhancedPort_write_epp_data():
    port = parallel64.ports.EnhancedPort(100)

    try:
        port.write_epp_data(b"Test!")
    except:
        assert False


def test_EnhancedPort_read_epp_data():
    length = 5
    port = parallel64.ports.EnhancedPort(100)

    result = port.read_epp_data(length)

    assert isinstance(result, bytes)
    assert len(result) == length


def test_EnhancedPort_write_epp_address():
    port = parallel64.ports.EnhancedPort(100)

    try:
        port.write_epp_address(b"Test!")
    except:
        assert False


def test_EnhancedPort_read_epp_address():
    length = 5
    port = parallel64.ports.EnhancedPort(100)

    result = port.read_epp_address(length)

    assert isinstance(result, bytes)
    assert len(result) == length


def test_EnhancedPort_epp_address_address():
    base_address = 100
    port = parallel64.ports.EnhancedPort(base_address)

    result = port.epp_address_address

    assert isinstance(result, int)
    assert result == base_address + 3


def test_EnhancedPort_epp_data_address():
    base_address = 100
    port = parallel64.ports.EnhancedPort(base_address)

    result = port.epp_data_address

    assert isinstance(result, int)
    assert result == base_address + 4
