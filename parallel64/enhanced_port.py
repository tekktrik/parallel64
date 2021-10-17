import json
from enum import Enum
from .standard_port import StandardPort

class EnhancedPort(StandardPort):
            
    def __init__(self, spp_base_address, windll_location=None):
        super().__init__(spp_base_address, windll_location)
        self._epp_address_address = spp_base_address + 3
        self._epp_data_address = spp_base_address + 4
        
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
        
    def writeEPPAddress(self, address):
        self.resetControlForSPPHandshake()
        self.setForwardDirection()
        self._parallel_port.DlPortWritePortUchar(self._epp_address_address, address)
        
    def readEPPAddress(self):
        self.resetControlForSPPHandshake()
        self.setReverseDirection()
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def writeEPPData(self, data):
        self.resetControlForSPPHandshake()
        self.setForwardDirection()
        self._parallel_port.DlPortWritePortUchar(self._epp_data_address, data)
        
    def readEPPData(self):
        self.resetControlForSPPHandshake()
        self.setReverseDirection()
        return self._parallel_port.DlPortReadPortUchar(self._epp_data_address)