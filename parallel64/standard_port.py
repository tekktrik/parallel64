import ctypes
import json

class StandardPort:

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

    def __init__(self, spp_base_address, windll_location):
    
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
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
        
    def resetControlForSPPHandshake(self)
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
                