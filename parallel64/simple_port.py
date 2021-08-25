import ctypes
import json

class SimplePort:

    def __init__(self, spp_base_address, ecp_base_address, windll_location):
    
        self._spp_data_address = int(spp_base_address, 16)
        self._status_address = int(spp_base_address, 16) + 1
        self._control_address = int(spp_base_address, 16) + 2
        self._epp_address_address = int(spp_base_address, 16) + 3
        self._epp_data_address = int(spp_base_address, 16) + 4
        self._parallel_port = ctypes.WinDLL(windll_location)
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        return cls(json_contents["spp_base_address"], json_contents["windll_location"])

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

    def readDataBitIndex(self, bit_index):
        if (bit_index >= 0) and (bit_index <=7) and isinstance(bit_index, int):
            byte_read = self._parallel_port.readSPPData()
            bit_mask = (1 << bit_index)
            return (bit_mask & byte_read) >> bit_index
        else:
            if (bit_index < 0) or (bit_index > 7):
                raise IndexError("Bit requested "+str(bit_index)+"is not accessible")
            if not isinstance(bit_index, int):
                raise TypeError("Bit requested must be an integer")
    
    def readPin(self, pin_number):
        try:
            if (pin_number >= 2) and (pin_number <= 9):
                return self.readDataBitIndex(pin_number - 1)
        except TypeError:
            raise TypeError("Pin requested must be an integer")
                