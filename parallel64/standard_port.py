import ctypes
import json
import os
import sys

class StandardPort:

    def __init__(self, spp_base_address, windll_location=None):
    
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
        if windll_location == None:
            parent_folder = os.path.join(__file__, "..", "..")
            inpout_folder = [os.path.abspath(folder) for folder in os.listdir(parent_folder) if folder.startswith("InpOutBinaries")][0]
            if sys.maxsize > 2**32:
                windll_location = os.path.join(inpout_folder, "x64", "inpoutx64.dll")
            else:
                windll_location = os.path.join(inpout_folder, "Win32", "inpout32.dll")
        self._parallel_port = ctypes.WinDLL(windll_location)
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            spp_base_add = int(json_contents["spp_base_address"], 16)
            windll_loc = json_contents["windll_location"], 16
            return cls(spp_base_add, windll_location)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")
            
    def setForwardDirection(self):
        control_byte = self.readControlRegister()
        new_control_byte = 0b11011111 & control_byte
        self.writeControlRegister(new_control_byte)
        
    def setReverseDirection(self):
        control_byte = self.readControlRegister()
        new_control_byte = 0b00100000 | control_byte
        self.writeControlRegister(new_control_byte)
        
    def resetControlForSPPHandshake(self):
        control_byte = self.readControlRegister()
        pre_control_byte = 0b11110000 & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.writeControlRegister(new_control_byte)

    def writeControlRegister(self, control_byte):
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def readControlRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def readStatusRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    def writeSPPData(self, data):
        self.resetControlForSPPHandshake()
        self.setForwardDirection()
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data)
        
    def readSPPData(self):
        self.resetControlForSPPHandshake()
        self.setReverseDirection()
        return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)