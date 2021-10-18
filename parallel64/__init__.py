import sys

if sys.platform != 'win32':
    raise Exception("parallel64 is meant for Windows systems only")

import os
import ctypes
import time
import json
from enum import Enum
from typing import Optional, List, Tuple
import threading


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

    class Direction(Enum):
        '''Enum class representing the current direction of the port
        '''
    
        REVERSE = 0
        FORWARD = 1
    
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
        return self.Direction(direction_byte >> 5)
    
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
        self.set_direction(self.Direction.REVERSE)
        
    def set_forward(self):
        '''Sets the port to forward (output)
        '''
        self.set_direction(self.Direction.FORWARD)
        
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
            
    class CommunicationMode(Enum):
        
        SPP = 0
        BYTE = 1
        #SPP_FIFO = 2
        #ECP_FIFO = 3
        EPP = 4
        #FIFO_TEST = 6
        #CONFIG = 7
            
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
        
    def set_comm_mode(self, comm_mode: CommunicationMode):
        self.write_ecr_register(comm_mode.value << 5)
        
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def write_ecr_register(self, data: int):
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, data)
        
    def read_ecr_register(self) -> int:
        return self._parallel_port.DlPortReadPortUchar(self._ecr_address)


class EnhancedPort(StandardPort):
            
    def __init__(self, spp_base_address: int, windll_location: Optional[str] = None):
        super().__init__(spp_base_address, windll_location)
        self._epp_address_address = spp_base_address + 3
        self._epp_data_address = spp_base_address + 4
        
    def write_epp_address(self, address: int):
        self.spp_handshake_control_reset()
        self.set_forward()
        self._parallel_port.DlPortWritePortUchar(self._epp_address_address, address)
        
    def read_epp_address(self) -> int:
        self.spp_handshake_control_reset()
        self.set_reverse()
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def write_epp_data(self, data: int):
        self.spp_handshake_control_reset()
        self.set_forward()
        self._parallel_port.DlPortWritePortUchar(self._epp_data_address, data)
        
    def read_epp_data(self) -> int:
        self.spp_handshake_control_reset()
        self.set_reverse()
        return self._parallel_port.DlPortReadPortUchar(self._epp_data_address)


class GPIOPort(StandardPort):
    
    class Pins:
    
        class Pin:

            def __init__(self, pin_number: int, bit_index: int, register: int, hw_inverted: bool = False):
                self.pin_number = pin_number
                self.bit_index = bit_index
                self.register = register
                self._hw_inverted = hw_inverted
                self._allow_input = None
                self._allow_output = None
                
            def is_hw_inverted(self) -> bool:
                return self._hw_inverted
                
            def is_output_allowed(self) -> bool:
                return self._allow_output
                
            def iw_input_allowed(self) -> bool:
                return self._allow_input
            
        class DataPin(Pin):
            
            register_lock = threading.Lock()
            
            def __init__(self, pin_number, bit_index, register, is_bidir):
                super().__init__(pin_number, bit_index, register, False)
                self._allow_input = True if is_bidir else False
                self._allow_output = True
                
        class StatusPin(Pin):
            
            register_lock = threading.Lock()
            
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = False
                
        class ControlPin(Pin):
                
            register_lock = threading.Lock()
                
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = True
        
        def __init__(self, data_address: int, is_bidir: bool):
            self.STROBE = self.ControlPin(1, 0, data_address+2, True)
            self.AUTO_LINEFEED = self.ControlPin(14, 1, data_address+2, True)
            self.INITIALIZE = self.ControlPin(16, 2, data_address+2)
            self.SELECT_PRINTER = self.ControlPin(17, 3, data_address+2, True)
            
            self.ACK = self.StatusPin(10, 6, data_address+1)
            self.BUSY = self.StatusPin(11, 7, data_address+1, True)
            self.PAPER_OUT = self.StatusPin(12, 5, data_address+1)
            self.SELECT_IN = self.StatusPin(13, 4, data_address+1)
            self.ERROR = self.StatusPin(15, 3, data_address+1)

            self.D0 = self.DataPin(2, 0, data_address, is_bidir)
            self.D1 = self.DataPin(3, 1, data_address, is_bidir)
            self.D2 = self.DataPin(4, 2, data_address, is_bidir)
            self.D3 = self.DataPin(5, 3, data_address, is_bidir)
            self.D4 = self.DataPin(6, 4, data_address, is_bidir)
            self.D5 = self.DataPin(7, 5, data_address, is_bidir)
            self.D6 = self.DataPin(8, 6, data_address, is_bidir)
            self.D7 = self.DataPin(9, 7, data_address, is_bidir)
        
        def get_named_pin_list(self) -> List[Tuple[str, Pin]]:
            pin_dict = self.__dict__.items()
            return [pin_name for pin_name in pin_dict if pin_name != "_parallel_port"]
            
        def get_pin_list(self) -> List[Pin]:
            return [pin[1] for pin in self.get_named_pin_list()]
            
        def get_pin_name_list(self) -> List[str]:
            return [pin[0] for pin in self.get_named_pin_list()]
                
    def __init__(self, data_address: int, windll_location: Optional[str] = None, clear_gpio: bool = True, reset_control: bool = False):
        super().__init__(data_address, windll_location, reset_control)
        self.Pins = self.Pins(self._spp_data_address, self.is_bidirectional())
        if clear_gpio:
            self.write_data_register(0)
            self.reset_control_pins()
        
    def read_pin(self, pin: Pins.Pin) -> bool:
        if pin.iw_input_allowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            bit_mask = 1 << pin.bit_index
            bit_result = bool((bit_mask & register_byte) >> pin.bit_index)
            return (not bit_result) if pin.is_hw_inverted() else bit_result
        else:
            raise Exception("Input not allowed on pin " + str(pin.pin_number))
            
    def write_pin(self, pin: Pins.Pin, value: bool):
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
        self.write_spp_data(0)
        
    def reset_control_pins(self):
        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)


class ParallelPort:
    
    def __init__(self, spp_base_address: int = None, ecp_base_address: int = None, windll_location: Optional[str] = None, port_modes: List[str] = []):
        self.StandardPort = None
        self.EnhancedPort = None
        self.ExtendedPort = None
        self.GPIOPort = None
        self.modes = port_modes
        for mode in self.modes:
            if mode.lower() == "spp":
                self.StandardPort = StandardPort(spp_base_address, windll_location)
            if mode.lower() == "epp":
                self.EnhancedPort = EnhancedPort(spp_base_address, windll_location)
            if mode.lower() == "ecp":
                self.ExtendedPort = ExtendedPort(ecp_base_address, windll_location)
            if mode.lower() == "gpio":
                self.GPIOPort = GPIOPort(spp_base_address, windll_location)
        
    @classmethod
    def from_json(cls, json_filepath: str) -> 'ParallelPort':
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