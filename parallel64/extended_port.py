import ctypes
import json

class ExtendedPort:

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

    def __init__(self, spp_base_address, ecp_base_address, windll_location):
    
        self._spp_data_address = int(spp_base_address, 16)
        self._status_address = int(spp_base_address, 16) + 1
        self._control_address = int(spp_base_address, 16) + 2
        self._epp_address_address = int(spp_base_address, 16) + 3
        self._epp_data_address = int(spp_base_address, 16) + 4
        self._ecr_address = int(ecp_base_address, 16) + 2
        self._parallel_port = ctypes.WinDLL(windll_location)
        
        set_epp_mode = (1 << 7)
        self._parallel_port.DlPortWritePortUchar(self._ecr_address, set_epp_mode)
        self._parallel_port.DlPortWritePortUchar(self._ecr_address)
        
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
    
    def writeControlRegister(self, control_byte):
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def readControlRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def readStatusRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    def writeSPPData(self, data):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00000100)
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data)
        
    def readSPPData(self):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00100100)
        return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)