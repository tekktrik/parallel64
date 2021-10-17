import json
import os
import sys
from enum import Enum

class ExtendedPort:
            
    class CommunicationMode(Enum):
        
        SPP = 0
        BYTE = 1
        #SPP_FIFO = 2
        #ECP_FIFO = 3
        EPP = 4
        #FIFO_TEST = 6
        #CONFIG = 7
            
    def __init__(self, ecp_base_address, windll_location=None):
        self._ecr_address = ecp_base_address + 2
        if windll_location == None:
            parent_folder = os.path.join(__file__, "..")
            inpout_folder = [os.path.abspath(os.path.join(parent_folder, folder)) for folder in os.listdir(__file__) if folder == "inpoutdlls"][0]
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
        
    def setCommunicationMode(self, comm_mode):
        self.writeECR(comm_mode.value << 5)
        
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def writeECR(self, data):
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, (1 << 7))
        
    def readECR(self):
        return self._parallel_port.DlPortReadPortUchar(self._ecr_address)