import ctypes
import json
import inspect
from enum import Enum
from parallel64.standard_port import StandardPort
from parallel64.bitbang.i2c import I2C

class GPIOPort(StandardPort):
    
    class Pins:
    
        class Pin:

            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                self.pin_number = pin_number
                self.bit_index = bit_index
                self.register = register
                self._hw_inverted = hw_inverted
                self._allow_input = None
                self._allow_output = None
                
            def isHardwareInverted(self):
                return self._hw_inverted
                
            def isOutputAllowed(self):
                return self._allow_output
            
        class DataPin(Pin):
            
            def __init__(self, pin_number, bit_index, register, is_bidir):
                super().__init__(pin_number, bit_index, register, False)
                self._allow_input = True if is_bidir else False
                self._allow_output = True
                
        class StatusPin(Pin):
            
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = False
                
        class ControlPin(Pin):
                
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = True
        
        def __init__(self, data_address, status_address, control_address, is_bidir):
            self.STROBE = self.ControlPin(1, 0, control_address, hw_inverted=True)
            self.AUTO_LINEFEED = self.ControlPin(14, 1, control_address, hw_inverted=True)
            self.INITIALIZE = self.ControlPin(16, 2, control_address)
            self.SELECT_PRINTER = self.ControlPin(17, 3, control_address, hw_inverted=True)
            
            self.ACK = self.StatusPin(10, 6, status_address)
            self.BUSY = self.StatusPin(11, 7, status_address, hw_inverted=True)
            self.PAPER_OUT = self.StatusPin(12, 5, status_address)
            self.SELECT_IN = self.StatusPin(13, 4, status_address)
            self.ERROR = self.StatusPin(15, 3, status_address)

            self.D0 = self.DataPin(2, 0, data_address, is_bidir)
            self.D1 = self.DataPin(3, 1, data_address, is_bidir)
            self.D2 = self.DataPin(4, 2, data_address, is_bidir)
            self.D3 = self.DataPin(5, 3, data_address, is_bidir)
            self.D4 = self.DataPin(6, 4, data_address, is_bidir)
            self.D5 = self.DataPin(7, 5, data_address, is_bidir)
            self.D6 = self.DataPin(8, 6, data_address, is_bidir)
            self.D7 = self.DataPin(9, 7, data_address, is_bidir)
        
        def getNamedPinList(self):
            pin_dict = self.__dict__.items()
            return [pin_name for pin_name in pin_dict if pin[0] != "_parallel_port"]
            
        def getPinList(self):
            return [pin[1] for pin in self.getNamedPinList()]
            
        def getPinNames(self):
            return [pin[0] for pin in self.getNamedPinList()]
                
    def __init__(self, data_address, windll_location=None):
        super().__init__(data_address, windll_location)
        self.Pins = self.Pins(self._spp_data_address, self._status_address, self._control_address, self.isBidirectional())
        
    def readPin(self, pin):
        if pin.isInputAllowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            bit_mask = 1 << pin.bit_index
            bit_result = bool((bit_mask & register_byte) >> pin.bit_index)
            return (not bit_result) if pin.isHardwareInverted() else bit_result
        else:
            raise Exception("Input not allowed on pin " + str(pin.pin_number))
            
    def writePin(self, pin, value):
        register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
        current_bit = ((1 << pin.bit_index) & register_byte) >> pin.bit_index
        current_value = (not current_bit) if pin.isHardwareInverted() else current_bit
        if bool(current_value) != value:
            bit_mask = 1 << pin.bit_index
            byte_result = (bit_mask ^ register_byte)
            register_byte =  self._parallel_port.DlPortWritePortUchar(pin.register, byte_result)