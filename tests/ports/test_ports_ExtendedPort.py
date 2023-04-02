# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.ports.ExtendedPort
"""

import parallel64.ports


def test_ExtendedPort_init():
    try:
        _ = parallel64.ports.ExtendedPort(100, 103)
    except:
        assert False


def test_ExtendedPort_write_ecp_ecr():
    port = parallel64.ports.ExtendedPort(100, 103)

    try:
        port.write_ecp_ecr(0b10000000)
    except:
        assert False


def test_ExtendedPort_read_ecp_ecr():
    length = 5
    port = parallel64.ports.ExtendedPort(100, 103)

    result = port.read_ecp_ecr()

    assert isinstance(result, int)


def test_ExtendedPort_comm_mode():
    port = parallel64.ports.ExtendedPort(100, 103)

    port.comm_mode = parallel64.ports.CommMode.EPP

    try:
        comm_mode = port.comm_mode
    except ValueError:
        pass
    else:
        assert False


def test_ExtendedPort_ecp_data_address():
    base_ecp_address = 103
    port = parallel64.ports.ExtendedPort(100, base_ecp_address)

    result = port.ecp_data_address

    assert isinstance(result, int)
    assert result == base_ecp_address


def test_ExtendedPort_ecp_config_address():
    base_ecp_address = 103
    port = parallel64.ports.ExtendedPort(100, base_ecp_address)

    result = port.ecp_config_address

    assert isinstance(result, int)
    assert result == base_ecp_address + 1


def test_ExtendedPort_ecp_ecr_address():
    base_ecp_address = 103
    port = parallel64.ports.ExtendedPort(100, base_ecp_address)

    result = port.ecp_ecr_address

    assert isinstance(result, int)
    assert result == base_ecp_address + 2
