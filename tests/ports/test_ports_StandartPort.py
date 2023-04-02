# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests parallel64.ports.StandardPort
"""

import parallel64.ports


def test_StandartPort_init():
    try:
        _ = parallel64.ports.StandardPort(100)
    except:
        assert False


def test_StandardPort_write_spp_data():
    port = parallel64.ports.StandardPort(100)

    try:
        port.write_spp_data(b"Test!", hold_while_busy=False)
    except:
        assert False


def test_StandardPort_write_data_register():
    port = parallel64.ports.StandardPort(100)

    try:
        port.write_data_register(10)
    except:
        assert False


def test_StandardPort_write_control_register():
    port = parallel64.ports.StandardPort(100)

    try:
        port.write_control_register(10)
    except:
        assert False


def test_StandardPort_read_data_register():
    port = parallel64.ports.StandardPort(100)

    try:
        result = port.read_data_register()
    except:
        assert False

    assert isinstance(result, int)


def test_StandardPort_read_status_register():
    port = parallel64.ports.StandardPort(100)

    try:
        result = port.read_status_register()
    except:
        assert False

    assert isinstance(result, int)


def test_StandardPort_read_control_register():
    port = parallel64.ports.StandardPort(100)

    try:
        result = port.read_control_register()
    except:
        assert False

    assert isinstance(result, int)


def test_StandardPort_test_bidirectionality():
    port = parallel64.ports.StandardPort(100)

    try:
        result = port.test_bidirectionality()
    except:
        assert False

    assert isinstance(result, bool)


def test_StandardPort_reset_control_register():
    port = parallel64.ports.StandardPort(100)

    try:
        port.reset_control_register()
    except:
        assert False


def test_StandardPort_direction():
    port = parallel64.ports.StandardPort(100, bidirectional=True)

    port.direction = parallel64.ports.Direction.REVERSE

    direction = port.direction

    assert isinstance(direction, parallel64.ports.Direction)


def test_StandardPort_bidirectional():
    uni_port = parallel64.ports.StandardPort(100, bidirectional=False)
    bi_port = parallel64.ports.StandardPort(100, bidirectional=True)

    assert not uni_port.bidirectional
    assert bi_port.bidirectional


def test_StandardPort_registers():
    base_address = 100
    port = parallel64.ports.StandardPort(base_address, bidirectional=False)

    assert port.spp_data_address == base_address
    assert port.spp_status_address == base_address + 1
    assert port.spp_control_address == base_address + 2
