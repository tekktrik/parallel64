import os
import sys
import ctypes
import time
import json
from enum import Enum
from typing import Optional


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
        
    #-------------------------------- Need to write protocol for SPP
        
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