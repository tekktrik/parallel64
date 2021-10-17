import os
import sys
import ctypes
import time
import json
from enum import Enum
from typing import Optional


class StandardPort:

    class Direction(Enum):
    
        REVERSE = 0
        FORWARD = 1
    
    def __init__(self, spp_base_address: int, windll_location: Optional[str] = None, reset_control: bool = True):
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
        if windll_location == None:
            parent_folder = os.path.join(__file__, "..")
            #inpout_folder = [os.path.abspath(folder) for folder in os.listdir(parent_folder) if folder.startswith("InpOutBinaries")][0]
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
        control_byte = self.read_control_register()
        direction_byte = (1 << 5) & control_byte
        return self.Direction(direction_byte >> 5)
    
    def set_direction(self, direction: Direction):
        #direction_byte = direction.value << 5
        control_byte = self.read_control_register()
        new_control_byte = (direction << 5) | control_byte
        self.write_control_register(new_control_byte)
        
    def set_reverse(self):
        self.set_direction(self.Direction.REVERSE)
        
    def set_forward(self):
        self.set_direction(self.Direction.FORWARD)
        
    def _test_bidirectional(self) -> bool:
        curr_dir = self.get_direction()
        self.set_reverse()
        isBidir = not bool(self.get_direction().value)
        self.set_direction(curr_dir)
        return isBidir
        
    def is_bidirectional(self) -> bool:
        return self._is_bidir
        
    def write_data_register(self, data_byte: int):
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data_byte)
        
    def read_data_register(self) -> int:
        if self._is_bidir:
            return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)
        else:
            raise Exception("This port was detected not to be bidirectional, data cannot be read using the data register/pins")

    def write_control_register(self, control_byte: int):
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def read_control_register(self) -> int:
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def read_status_register(self) -> int:
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    #-------------------------------- Need to write protocol for SPP
        
    def write_spp_data(self, data: int, hold_while_busy: bool = True):
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
        if self.is_bidirectional():
            self.spp_handshake_control_reset()
            self.set_reverse()
            return self.read_data_register()
        else:
            raise OSError("This port was detected not to be bidirectional, data cannot be read using the data register/pins")
        
    def spp_handshake_control_reset(self):
        control_byte = self.read_control_register()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.write_control_register(new_control_byte)