import ctypes
import json
from simple_port import SimplePort

class GPIOPort(SimplePort):

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