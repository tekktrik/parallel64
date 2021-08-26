import ctypes
import json
from enum import Enum
from simple_port import SimplePort

class GPIOPort(SimplePort):

    class Pins:
        
        def __init__(self, pin_number, bit_index, register, hw_inverted=False):
            self.pin_number = pin_number
            self.bit_index = bit_index
            self.register = register
            self.hw_inverted = hw_inverted

    # class GPIOPins(Enum):
        
        # def isHardwareInverted(self):
            # return self.hw_inverted
        
        # @classmethod
        # def getViablePinNumbers(cls):
            # return set(pin.pin_number for pin in cls)
            
        # @classmethod
        # def isViablePin(cls, pin_number):
            # return pin_number in cls.getViablePinNumbers()
        
    class OutputPins(Pins):
        STROBE = self.Pin(1, 0, self._control_address, True)
        AUTO_LINEFEED = self.Pin(14, 1, self._control_address, True)
        INITIALIZE = self.Pin(16, 2, self._control_address, False)
        SELECT_PRINTER = self.Pin(17, 3, self._control_address, True)
        
    class InputPins(Pins):
        ACK = 10
        BUSY = 11
        PAPER_OUT = 12
        SELECT_IN = 13
        ERROR = 15
    
    class InputOutputPins(Pins):
    
        D0 = 2
        D1 = 3
        D2 = 4
        D3 = 5
        D4 = 6
        D5 = 7
        D6 = 8
        D7 = 9
    
    def readPin(self, pin):
        if isinstance(pin, int):
            try:
                
        try:
            if ins:
                bit_index = bit_index - 2
                byte_read = self._parallel_port.readSPPData()
                bit_mask = (1 << bit_index)
                return (bit_mask & byte_read) >> bit_index
        except TypeError:
            raise TypeError("Pin requested must be an integer")