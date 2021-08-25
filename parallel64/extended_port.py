import json
from enum import Enum
from simple_port import SimplePort
import port_errors

class ExtendedPort(SimplePort):
            
    class CommunicationMode(Enum):
        
        SPP = 0
        BYTE = 1
        #SPP_FIFO = 2
        #ECP_FIFO = 3
        EPP = 4
        #FIFO_TEST = 6
        #CONFIG = 7
            
    def __init__(self, spp_base_address, ecp_base_address, windll_location):
        super.__init__(spp_base_address, windll_location)
        self._epp_address_address = spp_base_address + 3
        self._epp_data_address = spp_base_address + 4
        self._ecr_address = ecp_base_address + 2
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            spp_base_add = int(json_contents["spp_base_address"], 16)
            ecp_base_add = int(json_contents["ecp_base_address"], 16)
            windll_loc = json_contents["windll_location"], 16
            return cls(spp_base_add, ecp_base_add, windll_location)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")
        
    def setCommunicationMode(self, comm_mode):
        self.writeECR(comm_mode.value << 5)
        
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
        
    def writeECR(self, data):
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, (1 << 7))
        
    def readECR(self):
        return self._parallel_port.DlPortReadPortUchar(self._ecr_address)