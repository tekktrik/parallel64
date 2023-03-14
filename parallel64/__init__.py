# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""

`parallel64`

Functionality fo interfacing with a parallel port


* Author(s): Alec Delaney

"""

import time
import _parallel64
from parallel64.pins import Pins, Pin
from parallel64.constants import Direction, CommMode


# pylint: disable=too-few-public-methods
class _BasePort:
    """
    Base class for all ports
    """


class StandardPort(_BasePort):
    """
    The class for representing the SPP port

    :param int spp_base_address: The base address for the port, representing the
        SPP port data register
    :param bool reset_control: (optional) Whether the control register should be
        reset upon initialization, default is to reset it (True)
    """

    def __init__(
        self,
        spp_base_address: int,
        reset_control: bool = True,
    ) -> None:
        _parallel64.init_ports(spp_base_address, 3)
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
        self._is_bidir = self._test_bidirectional()
        if reset_control:
            self.spp_handshake_control_reset()

    @classmethod

    @property
    def direction(self) -> Direction:
        """Get the current direction of the port"""

        control_byte = self.read_control_register()
        direction_byte = (1 << 5) & control_byte
        return Direction(direction_byte >> 5)

    @direction.setter
    def direction(self, direction: Direction) -> None:

        control_byte = self.read_control_register()
        new_control_byte = (direction.value << 5) | control_byte
        self.write_control_register(new_control_byte)

    def _test_bidirectional(self) -> bool:
        """Tests whether the port has bidirectional support

        :return: Whether the port is bidirectional
        :rtype: bool
        """

        curr_dir = self.direction
        self.direction = Direction.REVERSE
        is_bidir = not bool(self.direction.value)
        self.direction = curr_dir
        return is_bidir

    @property
    def is_bidirectional(self) -> bool:
        """Returns whether the port is bidirectional, based on the test performed
        during ``__init__()``
        """
        return self._is_bidir

    def write_data_register(self, data_byte: int) -> None:
        """Writes to the Data register

        :param data_byte: A byte of data
        :type data_byte: int
        """
        import os
        _parallel64.write(self._spp_data_address, data_byte)

    def read_data_register(self) -> int:
        """Reads from the data register

        :return: The information in the Data register
        :rtype: int
        :raises OSError: If the port is not bidirectional
        """

        if self._is_bidir:
            return _parallel64.read(self._spp_data_address)

        raise OSError(
            "This port was detected not to be bidirectional, data cannot be "
            "read using the data register/pins"
        )

    def write_control_register(self, control_byte: int) -> None:
        """Writes to the Control register

        :param control_byte: A byte of data
        :type control_byte: int
        """
        _parallel64.write(self._control_address, control_byte)

    def read_control_register(self) -> int:
        """Reads from the Control register

        :return: The information in the Control register
        :rtype: int
        """
        return _parallel64.read(self._control_address)

    def read_status_register(self) -> int:
        """Reads from the Status register

        :return: The information in the Status register
        :rtype: int
        """
        return _parallel64.read(self._status_address)

    def write_spp_data(self, data: int, hold_while_busy: bool = True) -> None:
        """Writes data via SPP

        :param int data: The data to be transmitted
        :param bool hold_while_busy: Whether code should be blocked until the Busy
            line communicates the device is done receiving the data, default
            behavior is blocking (True)
        :raises OSError: If the port is busy
        """

        self.spp_handshake_control_reset()
        if self.is_bidirectional:
            self.direction = Direction.FORWARD
        self.write_data_register(data)
        if not bool((self.read_status_register() & (1 << 7)) >> 7):
            raise OSError("Port is busy")
        curr_control = self.read_control_register()
        self.write_control_register(curr_control | 0b00000001)
        time.sleep(0.001)
        self.write_control_register(curr_control)
        if hold_while_busy:
            while not bool((self.read_status_register() & (1 << 7)) >> 7):
                pass

    def read_spp_data(self) -> int:
        """Reads data on the SPP data register, while managing the SPP handshake
        resources similar to a write operation

        :return: The data on the Data pins
        :rtype: int
        :raises OSError: If the port is not bidirectional
        """

        if self.is_bidirectional:
            self.spp_handshake_control_reset()
            self.direction = Direction.REVERSE
            return self.read_data_register()

        raise OSError(
            "This port was detected not to be bidirectional, data cannot be "
            "read using the data register/pins"
        )

    def spp_handshake_control_reset(self) -> None:
        """Resets the Control register for the SPP handshake"""

        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)


class ExtendedPort(_BasePort):
    """
    The class for representing the ECP port.  Currently, this class only works
    with the Extended Capabilities Register as opposed to the ECP port.

    :param int ecp_base_address: The base address for the port, representing the
        ECP port data register
    """

    def __init__(self, ecp_base_address: int) -> None:
        _parallel64.init_ports(ecp_base_address + 2, 1)
        self._ecr_address = ecp_base_address + 2

    @property
    def comm_mode(self) -> CommMode:
        """The communication mode in the ECR"""
        mode = self.read_ecr_register()
        return CommMode(mode >> 5)

    @comm_mode.setter
    def comm_mode(self, mode: CommMode) -> None:
        self.write_ecr_register(mode.value << 5)

    def write_ecr_register(self, data: int) -> None:
        """Write data to the Extended Capabilities Register (ECR)

        :param data: The data to write to the register
        :type data: int
        """
        _parallel64.write(self._ecr_address, data)

    def read_ecr_register(self) -> int:
        """Read data in the Extended Capabilities Register (ECR)

        :return: The data in the register
        :rtype: int
        """
        return _parallel64.read(self._ecr_address)


class EnhancedPort(StandardPort):
    """
    The class for representing the EPP port.  It is an extension of the
    StandardPort (SPP), so its methods can be used as well.

    :param int spp_base_address: The base address for the port, representing
        the SPP port data register
    """

    def __init__(self, spp_base_address: int) -> None:
        super().__init__(spp_base_address)
        _parallel64.init_ports(spp_base_address + 3, 2)
        self._epp_address_address = spp_base_address + 3
        self._epp_data_address = spp_base_address + 4

    def write_epp_address(self, address: int) -> None:
        """Write data to the EPP Address register (Address Write Cycle)

        :param address: The information to write
        :type address: int
        """

        self.spp_handshake_control_reset()
        self.direction = Direction.FORWARD
        _parallel64.write(self._epp_address_address, address)

    def read_epp_address(self) -> int:
        """Read data from the EPP Address register (Address Read Cycle)

        :return: The information read
        :rtype: int
        """

        self.spp_handshake_control_reset()
        self.direction = Direction.REVERSE
        return _parallel64.read(self._epp_address_address)

    def write_epp_data(self, data: int) -> None:
        """Write data to the EPP Data register (Data Write Cycle)

        :param data: The information to write
        :type data: int
        """

        self.spp_handshake_control_reset()
        self.direction = Direction.FORWARD
        _parallel64.write(self._epp_data_address, data)

    def read_epp_data(self) -> int:
        """Read data from the EPP Data register (Data Read Cycle)

        :return: The information read
        :rtype: int
        """
        self.spp_handshake_control_reset()
        self.direction = Direction.REVERSE
        return _parallel64.read(self._epp_data_address)


class GPIOPort(StandardPort):
    """
    The class for representing GPIO-like functionality of the port, useful for
    interacting with connected devices in ways outside of established parallel port
    communication protocols.  It inherits from the StandardPort class, however, so
    those methods are available as well.

    :param int spp_base_address: The base address for the port, representing the
        SPP port data register
    :param bool clear_gpio: (optional) Whether to clear pins and reset to low
        upon initialization, default is to reset pins (True)
    :param bool reset_control: (optional) Whether to reset the control register
        (according to SPP handshake protocol) upon initialization, default is
        not to reset the register (False). Note this takes place BEFORE clearing
        the pins via the ``clear_gpio`` argument.
    """

    def __init__(
        self,
        spp_base_address: int,
        clear_gpio: bool = True,
        reset_control: bool = False,
    ) -> None:
        super().__init__(spp_base_address, reset_control)
        self.pins = Pins(self._spp_data_address, self.is_bidirectional)
        if clear_gpio:
            self.write_data_register(0)
            self.reset_control_pins()

    def read_pin(self, pin: Pin) -> bool:
        """Read the state of the given pin

        :param pin: The pin to read
        :type pin: Pin
        :return: The state of the pin
        :rtype: bool
        :raises OSError: If the pin is output-only
        """

        if pin.input_allowed:
            register_byte = _parallel64.read(pin.register)
            bit_mask = 1 << pin.bit_index
            bit_result = bool((bit_mask & register_byte) >> pin.bit_index)
            return (not bit_result) if pin.hw_inverted else bit_result
        raise OSError("Input not allowed on pin " + str(pin.pin_number))

    def write_pin(self, pin: Pin, value: bool) -> None:
        """Set the state of the given pin

        :param Pin pin: The pin to set
        :param bool value: The state to set the pin
        :raises OSError: If the pin is input-only
        """

        if pin.output_allowed:
            register_byte = _parallel64.read(pin.register)
            current_bit = ((1 << pin.bit_index) & register_byte) >> pin.bit_index
            current_value = (not current_bit) if pin.hw_inverted else current_bit
            if bool(current_value) != value:
                bit_mask = 1 << pin.bit_index
                byte_result = bit_mask ^ register_byte
                _parallel64.write(pin.register, byte_result)
        else:
            raise OSError("Output not allowed on pin " + str(pin.pin_number))

    def reset_data_pins(self) -> None:
        """Reset the data pins (to low)"""
        self.write_spp_data(0)

    def reset_control_pins(self) -> None:
        """Reset the control pins (to low)"""

        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)
