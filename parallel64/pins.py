# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

import threading
from typing import List, Tuple


class Pin:
    """Class representing a pin"""

    def __init__(
        self, pin_number: int, bit_index: int, register: int, hw_inverted: bool = False
    ) -> None:
        self.pin_number = pin_number
        self.bit_index = bit_index
        self.register = register
        self._hw_inverted = hw_inverted
        self._allow_input = None
        self._allow_output = None

    @property
    def hw_inverted(self) -> bool:
        """Returns whether a pin is hardware inverted"""
        return self._hw_inverted

    @property
    def output_allowed(self) -> bool:
        """Returns whether a pin allows output"""
        return self._allow_output

    @property
    def input_allowed(self) -> bool:
        """Returns whether a pin allows input"""
        return self._allow_input


class DataPin(Pin):
    """Class representing an individual data pin, including a
    class-wide threading.Lock for I/O operations

    :ivar register_lock: A class-wide thread lock useful for
        making I/O safe code
    :vartype register_lock: threading.Lock
    """

    register_lock = threading.Lock()

    def __init__(
        self, pin_number: int, bit_index: int, register: int, is_bidir: bool
    ) -> None:
        super().__init__(pin_number, bit_index, register, False)
        self._allow_input = True if is_bidir else False
        self._allow_output = True


class StatusPin(Pin):
    """Class representing an individual status pin, including a
    class-wide threading.Lock for I/O operations

    :ivar register_lock: A class-wide thread lock useful for
        making I/O safe code
    :vartype register_lock: threading.Lock
    """

    register_lock = threading.Lock()

    def __init__(
        self, pin_number: int, bit_index: int, register: int, hw_inverted: bool = False
    ) -> None:
        super().__init__(pin_number, bit_index, register, hw_inverted)
        self._allow_input = True
        self._allow_output = False


class ControlPin(Pin):
    """Class representing an individual control pin, including a
    class-wide threading.Lock for I/O operations

    :ivar register_lock: A class-wide thread lock useful for
        making I/O safe code
    :vartype register_lock: threading.Lock
    """

    register_lock = threading.Lock()

    def __init__(
        self, pin_number: int, bit_index: int, register: int, hw_inverted: bool = False
    ) -> None:
        super().__init__(pin_number, bit_index, register, hw_inverted)
        self._allow_input = True
        self._allow_output = True


class Pins:
    """Class representing all the pins for a given port (connected to
    registers).  Interaction with this class typically takes place by
    manipulating the 'pins' attribute of an instance of 'GPIOPort':

    .. code-block::

        import parallel64
        gpio = parallel64.GPIOPort(0x1234)
        input_pin = gpio.pins.D0
        pin_value = gpio.read_pin(input_pin)

    Data Pins:
    D0, D1, D2, D3, D4, D5, D6, D7

    Status Pins:
    ACK, BUSY, PAPER_OUT, SELECT_IN, ERROR

    Control Pins:
    STROBE, AUTO_LINEFEED, INITIALIZE, SELECT_PRINTER
    """

    def __init__(self, data_address: int, is_bidir: bool) -> None:
        self.STROBE = ControlPin(1, 0, data_address + 2, True)
        self.AUTO_LINEFEED = ControlPin(14, 1, data_address + 2, True)
        self.INITIALIZE = ControlPin(16, 2, data_address + 2)
        self.SELECT_PRINTER = ControlPin(17, 3, data_address + 2, True)

        self.ACK = StatusPin(10, 6, data_address + 1)
        self.BUSY = StatusPin(11, 7, data_address + 1, True)
        self.PAPER_OUT = StatusPin(12, 5, data_address + 1)
        self.SELECT_IN = StatusPin(13, 4, data_address + 1)
        self.ERROR = StatusPin(15, 3, data_address + 1)

        self.D0 = DataPin(2, 0, data_address, is_bidir)
        self.D1 = DataPin(3, 1, data_address, is_bidir)
        self.D2 = DataPin(4, 2, data_address, is_bidir)
        self.D3 = DataPin(5, 3, data_address, is_bidir)
        self.D4 = DataPin(6, 4, data_address, is_bidir)
        self.D5 = DataPin(7, 5, data_address, is_bidir)
        self.D6 = DataPin(8, 6, data_address, is_bidir)
        self.D7 = DataPin(9, 7, data_address, is_bidir)

    @property
    def pin_list(self) -> List[Tuple[str, Pin]]:
        """Returns a list of pins and their names"""
        return [
            (pin_name, pin)
            for pin_name, pin in self.__dict__.items()
            if isinstance(pin, Pin)
        ]

    def get_pin_number(self, pin_number: int) -> Pin:
        """Returns a pin based off of the pin number

        :rtype: Pin
        """
        # TODO: Add ValueError if out of bounds
        return (pin for _, pin in self.pin_list if pin.pin_number == pin_number)[0]
