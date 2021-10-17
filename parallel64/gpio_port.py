import ctypes
import json
import inspect
import threading
from enum import Enum
from .standard_port import StandardPort
from . import bitbang

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
                
            def isInputAllowed(self):
                return self._allow_input
            
        class DataPin(Pin):
            
            register_lock = threading.Lock()
            
            def __init__(self, pin_number, bit_index, register, is_bidir):
                super().__init__(pin_number, bit_index, register, False)
                self._allow_input = True if is_bidir else False
                self._allow_output = True
                
        class StatusPin(Pin):
            
            register_lock = threading.Lock()
            
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = False
                
        class ControlPin(Pin):
                
            register_lock = threading.Lock()
                
            def __init__(self, pin_number, bit_index, register, hw_inverted=False):
                super().__init__(pin_number, bit_index, register, hw_inverted)
                self._allow_input = True
                self._allow_output = True
        
        def __init__(self, data_address, is_bidir):
            self.STROBE = self.ControlPin(1, 0, data_address+2, True)
            self.AUTO_LINEFEED = self.ControlPin(14, 1, data_address+2, True)
            self.INITIALIZE = self.ControlPin(16, 2, data_address+2)
            self.SELECT_PRINTER = self.ControlPin(17, 3, data_address+2, True)
            
            self.ACK = self.StatusPin(10, 6, data_address+1)
            self.BUSY = self.StatusPin(11, 7, data_address+1, True)
            self.PAPER_OUT = self.StatusPin(12, 5, data_address+1)
            self.SELECT_IN = self.StatusPin(13, 4, data_address+1)
            self.ERROR = self.StatusPin(15, 3, data_address+1)

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
                
    def __init__(self, data_address, windll_location=None, clear_gpio=True, reset_control=False):
        super().__init__(data_address, windll_location, reset_control)
        self.Pins = self.Pins(self._spp_data_address, self.isBidirectional())
        if clear_gpio:
            self.writeDataRegister(0)
            self.resetControlPins()
            
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
        
    def readPin(self, pin):
        if pin.isInputAllowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            bit_mask = 1 << pin.bit_index
            bit_result = bool((bit_mask & register_byte) >> pin.bit_index)
            return (not bit_result) if pin.isHardwareInverted() else bit_result
        else:
            raise Exception("Input not allowed on pin " + str(pin.pin_number))
            
    def writePin(self, pin, value):
        if pin.isOutputAllowed():
            register_byte =  self._parallel_port.DlPortReadPortUchar(pin.register)
            current_bit = ((1 << pin.bit_index) & register_byte) >> pin.bit_index
            current_value = (not current_bit) if pin.isHardwareInverted() else current_bit
            if bool(current_value) != value:
                bit_mask = 1 << pin.bit_index
                byte_result = (bit_mask ^ register_byte)
                self._parallel_port.DlPortWritePortUchar(pin.register, byte_result)
        else:
            raise Exception("Output not allowed on pin " + str(pin.pin_number))
            
    def resetDataPins(self):
        self.writeSPPData(0)
        
    def resetControlPins(self):
        control_byte = self.readControlRegister()
        bidir_control_byte = 0b11110000 if self._is_bidir else 0b11010000
        pre_control_byte = bidir_control_byte & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.writeControlRegister(new_control_byte)
        
    def setupPWM(self, pwm_pin, duty_cycle, cycle_time):
        return bitbang.PWM(self, pwm_pin, duty_cycle, cycle_time)
                
    #def setupI2C(self, sda_pin, scl_pin):
    #    return I2C(self, sda_pin, scl_pin, baudrate)
