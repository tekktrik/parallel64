import json
from enum import Enum
from simple_port import SimplePort
import port_errors

class ExtendedPort(SimplePort):

    class DataConverter:
        
        @classmethod
        def hexstr_to_int(cls, trimmed_hex_str):
            return int("0x" + trimmed_hex_str, 16)
        
        @classmethod
        def binstr_to_int(cls, trimmed_bin_str):
            return int("0b" + trimmed_bin_str, 2)
            
        @classmethod
        def int_to_hexstr(cls, int_data):
            return ''.join('%02x'%int(hex(int_data), 16))
            
        @classmethod
        def int_to_binstr(cls, int_data):
            return '{:08b}'.format(int_data)
            
    #class CommunicationMode(Enum):
    #    
    #    SPP = 0
    #    EPP = 1
            
    def __init__(self, spp_base_address, ecp_base_address, windll_location, start_mode=None):
        super.__init__(spp_base_address, windll_location)
        self._ecr_address = int(ecp_base_address, 16) + 2
        
    #def setCommunicationMode(self, comm_mode):
    #    if comm_mode is self.CommunicationMode.SPP:
    #        self.setSPPCommunicationMode()
    #    elif comm_mode os self.CommunicationMode.EPP
    #        self.setEPPCommunicationMode()
    #    else:
    #        raise port_errors.InvalidCommunicationMode("Received invalid communication mode, mode not changed", comm_mode)
        
    def setSPPCommunicationMode(self):
        self.writeECRData(0)
        
    def setEPPCommunicationMode(self):
        self.writeECRData(1 << 7)
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        return cls(json_contents["spp_base_address"], json_contents["ecp_base_address"], json_contents["windll_location"])
        
    def writeEPPAddress(self, address):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00000100)
        self._parallel_port.DlPortWritePortUchar(self._epp_address_address, address)
        
    def readEPPAddress(self):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00100100)
        return self._parallel_port.DlPortReadPortUchar(self._epp_address_address)
        
    def writeEPPData(self, data):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00000100)
        self._parallel_port.DlPortWritePortUchar(self._epp_data_address, data)
        
    def readEPPData(self):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00100100)
        return self._parallel_port.DlPortReadPortUchar(self._epp_data_address)
        
    def writeECRData(self, data):
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, (1 << 7))
        
    def readECRData(self):
        return self._parallel_port.DlPortReadPortUchar(self._ecr_address)