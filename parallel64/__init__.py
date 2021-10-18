import sys

if sys.platform != 'win32':
    raise Exception("parallel64 is meant for Windows systems only")

import os
import ctypes
import time
import json
from enum import Enum
from typing import Optional, List, Tuple
from .pins import Pins, Pin
from .constants import Direction, CommMode


class StandardPort:
    '''The class for representing the SPP port

    :param spp_base_address: The base address for the port, representing the SPP port data register
    :type spp_base_address: int
    :param windll_location: The location of the DLL required to use the parallel port, default is to use the one \
    included in this package
    :type windll_location: str, optional
    :param reset_control: Whether the control register should be reset upon initialization, default is to reset it (True)
    :type reset_control: bool, optional
    '''
    
    def __init__(self, spp_base_address: int, windll_location: Optional[str] = None, reset_control: bool = True):
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
        if windll_location == None:
            parent_folder = os.path.join(__file__, "..")
            inpout_folder = [os.path.abspath(os.path.join(parent_folder, folder)) for folder in os.listdir(parent_folder) if folder == "inpoutdlls"][0]
            if sys.maxsize > 2**32:
                windll_location = os.path.join(inpout_folder, "inpoutx64.dll")
            else:
                windll_location = os.path.join(inpout_folder, "inpout32.dll")
        self._windll_location = windll_location
        self._parallel_port = ctypes.WinDLL(windll_location)
        self._is_bidir = True if self._test_bidirectional() else False
        if reset_control:
            self.spp_handshake_control_reset()
        
    @classmethod
    def from_json(cls, json_filepath: str) -> 'StandardPort':
        '''Factory method for creating and instance of StandardPort from a JSON file containing the necessary information

        :param json_filepath: Filepath to the JSON
        :type json_filepath: str
        :return: An instance of StandardPort
        :rtype: StandardPort
        '''

        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            spp_base_add = int(json_contents["spp_base_address"], 16)
            try:
                windll_loc = json_contents["windll_location"]
            except KeyError:
                windll_loc = None
            return cls(spp_base_add, windll_loc)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")
        
    def get_direction(self) -> Direction:
        '''Get the current direction of the port

        :return: Direction of the port
        :rtype: Direction
        '''

        control_byte = self.read_control_register()
        direction_byte = (1 << 5) & control_byte
        return Direction(direction_byte >> 5)
    
    def set_direction(self, direction: Direction):
        '''Sets the direction of the port

        :param direction: The direction to set the port
        :type direction: Direction
        '''

        control_byte = self.read_control_register()
        new_control_byte = (direction.value << 5) | control_byte
        self.write_control_register(new_control_byte)
        
    def set_reverse(self):
        '''Sets the port to reverse (input)
        '''
        self.set_direction(Direction.REVERSE)
        
    def set_forward(self):
        '''Sets the port to forward (output)
        '''
        self.set_direction(Direction.FORWARD)
        
    def _test_bidirectional(self) -> bool:
        '''Tests whether the port has bidirectional support

        :return: Whether the port is bidirectional
        :rtype: bool
        '''

        curr_dir = self.get_direction()
        self.set_reverse()
        isBidir = not bool(self.get_direction().value)
        self.set_direction(curr_dir)
        return isBidir
        
    def is_bidirectional(self) -> bool:
        '''Returns whether the port is bidirectional, based on the test performed during __init__

        :return: Whether the port was confirmed to be bidirectional
        :rtype: bool
        '''
        return self._is_bidir
        
    def write_data_register(self, data_byte: int):
        '''Writes to the Data register

        :param data_byte: A byte of data
        :type data_byte: int
        '''
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data_byte)
        
    def read_data_register(self) -> int:
        '''Reads from the data register

        :return: The information in the Data register
        :rtype: int
        :raises Exception: if the port is unable to read due to lack of bidirectionality support
        '''

        if self._is_bidir:
            return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)
        else:
            raise Exception("This port was detected not to be bidirectional, data cannot be read using the data register/pins")

    def write_control_register(self, control_byte: int):
        '''Writes to the Control register

        :param control_byte: A byte of data
        :type control_byte: int
        '''
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def read_control_register(self) -> int:
        '''Reads from the Control register
        
        :return: The information in the Control register
        :rtype: int
        '''
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def read_status_register(self) -> int:
        '''Reads from the Status register
        
        :return: The information in the Status register
        :rtype: int
        '''
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    def write_spp_data(self, data: int, hold_while_busy: bool = True):
        '''Writes data via SPP
        
        :param data: The data to be transmitted
        :type data: int
        :param hold_while_busy: Whether code should be blocked until the Busy line communicates the device is done receiving the data, \
        default behavior is blocking (True)
        :type hold_while_busy: bool
        '''

        self.spp_handshake_control_reset()
        if self.is_bidirectional():
            self.set_forward()
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
        '''Reads data on the SPP data register, while managing the SPP handshake resources similar to a write operation
        
        :return: The data on the Data pins
        :rtype: int
        '''

        if self.is_bidirectional():
            self.spp_handshake_control_reset()
            self.set_reverse()
            return self.read_data_register()
        else:
            raise OSError("This port was detected not to be bidirectional, data cannot be read using the data register/pins")
        
    def spp_handshake_control_reset(self):
        '''Resets the Control register for the SPP handshake
        '''

        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)


class ExtendedPort:
    '''The class for representing the ECP port.  Currently, this class only works with the Extended Capabilities Register as opposed to the ECP port.

    :param ecp_base_address: The base address for the port, representing the ECP port data register
    :type ecp_base_address: int
    :param windll_location: The location of the DLL required to use the parallel port, default is to use the one \
    included in this package
    :type windll_location: str, optional
    '''
            
    def __init__(self, ecp_base_address: int, windll_location: Optional[str] = None):
        self._ecr_address = ecp_base_address + 2
        if windll_location == None:
            parent_folder = os.path.join(__file__, "..")
            inpout_folder = [os.path.abspath(os.path.join(parent_folder, folder)) for folder in os.listdir(parent_folder) if folder == "inpoutdlls"][0]
            
            if sys.maxsize > 2**32:
                windll_location = os.path.join(inpout_folder, "inpoutx64.dll")
            else:
                windll_location = os.path.join(inpout_folder, "inpout32.dll")
        self._windll_location = windll_location
        self._parallel_port = ctypes.WinDLL(windll_location)
    
    @classmethod
    def from_json(cls, json_filepath: str) -> 'ExtendedPort':
        '''Factory method for creating and instance of ExtendedPort from a JSON file containing the necessary information

        :param json_filepath: Filepath to the JSON
        :type json_filepath: str
        :return: An instance of ExtendedPort
        :rtype: ExtendedPort
        '''
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            ecp_base_add = int(json_contents["ecp_base_address"], 16)
            try:
                windll_loc = json_contents["windll_location"]
            except KeyError:
                windll_loc = None
            return cls(ecp_base_add, windll_loc)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")
        
    def set_comm_mode(self, mode: CommMode):
        '''Set the communication mode in the ECR

        :param mode: The mode to set in the ECR
        :type mode: ExtendedPort.CommunicationMode
        '''
        self.write_ecr_register(mode.value << 5)
        
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def write_ecr_register(self, data: int):
        '''Write data to the Extended Capabilities Register (ECR)
        
        :param data: The data to write to the register
        :type data: int
        '''
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, data)
        
    def read_ecr_register(self) -> int:
        '''Read data in the Extended Capabilities Register (ECR)
        
        :return: The data in the register
        :rtype: int
        '''
        return self._parallel_port.DlPortReadPortUchar(self._ecr_address)


class EnhancedPort(StandardPort):
    '''The class for representing the EPP port.  It is an extension of the StandardPort (SPP), so it's methods can be used as well

    :param spp_base_address: The base address for the port, representing the SPP port data register
    :type spp_base_address: int
    :param windll_location: The location of the DLL required to use the parallel port, default is to use the one \
    included in this package
    :type windll_location: str, optional
    '''
            
    def __init__(self, spp_base_address: int, windll_location: Optional[str] = None):
        super().__init__(spp_base_address, windll_location)
        self._epp_address_address = spp_base_address + 3
        self._epp_data_address = spp_base_address + 4
        
    def write_epp_address(self, address: int):
        '''Write data to the EPP Address register (Address Write Cycle)
        
        :param address: The information to write
        :type address: int
        '''

        self.spp_handshake_control_reset()
        self.set_forward()
        self._parallel_port.DlPortWritePortUchar(self._epp_address_address, address)
        
    def read_epp_address(self) -> int:
        '''Read data from the EPP Address register (Address Read Cycle)
        
        :return: The information read
        :rtype: int
        '''

        self.spp_handshake_control_reset()
        self.set_reverse()
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def write_epp_data(self, data: int):
        '''Write data to the EPP Data register (Data Write Cycle)
        
        :param data: The information to write
        :type data: int
        '''

        self.spp_handshake_control_reset()
        self.set_forward()
        self._parallel_port.DlPortWritePortUchar(self._epp_data_address, data)
        
    def read_epp_data(self) -> int:
        '''Read data from the EPP Data register (Data Read Cycle)
        
        :return: The information read
        :rtype: int
        '''
        self.spp_handshake_control_reset()
        self.set_reverse()
        return self._parallel_port.DlPortReadPortUchar(self._epp_data_address)


class GPIOPort(StandardPort):
    '''The class for representing GPIO-like functionality of the port, useful for interacting with connected devices in ways
    outside of established parallel port communication protocols.  It inherits from the StandardPort class, however, so those
    methods are available as well.
    
    :param spp_base_address: The base address for the port, representing the SPP port data register
    :type spp_base_address: int
    :param windll_location: The location of the DLL required to use the parallel port, default is to use the one \
    included in this package
    :type windll_location: str, optional
    :param clear_gpio: Whether to clear pins and reset to low upon initialization, default is to reset pins(True)
    :type clear_gpio: bool, optional
    :param reset_control: Whether to reset the control register (according to SPP handshake protocol) upon initialization, \
    default is not to reset the register (False). Note this takes place BEFORE clearing the pins via the clear_gpio argument.
    '''
                
    def __init__(self, spp_base_address: int, windll_location: Optional[str] = None, clear_gpio: bool = True, reset_control: bool = False):
        super().__init__(spp_base_address, windll_location, reset_control)
        self.Pins = self.Pins(self._spp_data_address, self.is_bidirectional())
        if clear_gpio:
            self.write_data_register(0)
            self.reset_control_pins()
        
    def read_pin(self, pin: Pin) -> bool:
        '''Read the state of the given pin

        :param pin: The pin to read
        :type pin: Pin
        :return: The state of the pin
        :rtype: bool
        '''

        if pin.iw_input_allowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            bit_mask = 1 << pin.bit_index
            bit_result = bool((bit_mask & register_byte) >> pin.bit_index)
            return (not bit_result) if pin.is_hw_inverted() else bit_result
        else:
            raise Exception("Input not allowed on pin " + str(pin.pin_number))
            
    def write_pin(self, pin: Pin, value: bool):
        '''Set the state of the given pin

        :param pin: The pin to set
        :type pin: Pin
        :param value: The state to set the pin
        :type value: bool
        '''

        if pin.is_output_allowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            current_bit = ((1 << pin.bit_index) & register_byte) >> pin.bit_index
            current_value = (not current_bit) if pin.is_hw_inverted() else current_bit
            if bool(current_value) != value:
                bit_mask = 1 << pin.bit_index
                byte_result = (bit_mask ^ register_byte)
                self._parallel_port.DlPortWritePortUchar(pin.register, byte_result)
        else:
            raise Exception("Output not allowed on pin " + str(pin.pin_number))
            
    def reset_data_pins(self):
        '''Reset the data pins (to low)
        '''
        self.write_spp_data(0)
        
    def reset_control_pins(self):
        '''Reset the control pins (to low)
        '''

        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)


class ParallelPort:
    '''The class represent multifunction ports.  If a port has multiple functionalities (or use desire such functionality, such as
    a port the can perform EPP protocol as well as GPIO-like pin manipulation), this class is essential a wrapper class for holding
    all such ports.

    :param spp_base_address: The SPP base address, only needed for ports that require it
    :type spp_base_address: int, optional
    :param ecp_base_address: The ECP base address, only needed for ports that require it
    :type ecp_base_address: int, optional
    :param windll_location: The location of the DLL required to use the parallel port, default is to use the one \
    included in this package
    :type windll_location: str, optional
    :param port_modes: The modes to be stored in the ParallelPort object
    :type port_modes: list(str), optional
    '''
    
    def __init__(self, spp_base_address: Optional[int] = None, ecp_base_address: Optional[int] = None, windll_location: Optional[str] = None, port_modes: List[str] = []):
        self.spp = None
        self.epp = None
        self.ecp = None
        self.gpio = None
        self.modes = port_modes
        for mode in self.modes:
            if mode.lower() == "spp":
                self.spp = StandardPort(spp_base_address, windll_location)
            if mode.lower() == "epp":
                self.epp = EnhancedPort(spp_base_address, windll_location)
            if mode.lower() == "ecp":
                self.ecp = ExtendedPort(ecp_base_address, windll_location)
            if mode.lower() == "gpio":
                self.gpio = GPIOPort(spp_base_address, windll_location)
        
    @classmethod
    def from_json(cls, json_filepath: str) -> 'ParallelPort':
        '''Factory method for creating and instance of ParallelPort from a JSON file containing the necessary information

        :param json_filepath: Filepath to the JSON
        :type json_filepath: str
        :return: An instance of ParallelPort
        :rtype: ParallelPort
        '''
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            if json_contents["spp_base_address"] != None:
                spp_base_add = int(json_contents["spp_base_address"], 16)
            if json_contents["ecp_base_address"] != None:
                ecp_base_add = int(json_contents["ecp_base_address"], 16)
            try:
                windll_loc = json_contents["windll_location"]
            except KeyError:
                windll_loc = None
            port_modes = json_contents["port_modes"]
            return cls(spp_base_add, ecp_base_add, windll_loc, port_modes)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")