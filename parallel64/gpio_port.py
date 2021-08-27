import ctypes
import json
import inspect
from enum import Enum
from parallel64.standard_port import StandardPort
from parallel64.bitbang.i2c import I2C

class GPIOPort(StandardPort):
    
    class Pins:
    
        class Pin:

            def __init__(self, pin_number, bit_index, register, allow_input, allow_output, hw_inverted=False):
                self.pin_number = pin_number
                self.bit_index = bit_index
                self.register = register
                self._allow_input = allow_input
                self._allow_output = allow_output
                self._hw_inverted = hw_inverted
                
            def isInputAllowed(self):
                return self._allow_input
                
            def isOutputAllowed(self):
                return self._allow_output
                
            def isHardwareInverted(self):
                return self._hw_inverted
        
        def __init__(self, data_address):
            self.STROBE = self.Pin(1, 0, data_address+2, True, True, True)
            self.AUTO_LINEFEED = self.Pin(14, 1, data_address+2, True, True, True)
            self.INITIALIZE = self.Pin(16, 2, data_address+2, True, True)
            self.SELECT_PRINTER = self.Pin(17, 3, data_address+2, True, True, True)
            
            self.ACK = self.Pin(10, 6, data_address+1, True, False)
            self.BUSY = self.Pin(11, 7, data_address+1, True, False, True)
            self.PAPER_OUT = self.Pin(12, 5, data_address+1, True, False)
            self.SELECT_IN = self.Pin(13, 4, data_address+1, True, False)
            self.ERROR = self.Pin(15, 3, data_address+1, True, False)

            self.D0 = self.Pin(2, 0, data_address, True, True)
            self.D1 = self.Pin(3, 1, data_address, True, True)
            self.D2 = self.Pin(4, 2, data_address, True, True)
            self.D3 = self.Pin(5, 3, data_address, True, True)
            self.D4 = self.Pin(6, 4, data_address, True, True)
            self.D5 = self.Pin(7, 5, data_address, True, True)
            self.D6 = self.Pin(8, 6, data_address, True, True)
            self.D7 = self.Pin(9, 7, data_address, True, True)
        
        def getNamedPinList(self):
            pin_dict = self.__dict__.items()
            return [pin_name for pin_name in pin_dict if pin[0] != "_parallel_port"]
            
        def getPinList(self):
            return [pin[1] for pin in self.getNamedPinList()]
            
        def getPinNames(self):
            return [pin[0] for pin in self.getNamedPinList()]
                
    def __init__(self, data_address, windll_location=None):
        super().__init__(data_address, windll_location)
        self.Pins = self.Pins(self._spp_data_address)
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
                register_byte =  self._parallel_port.DlPortWritePortUchar(pin.register, byte_result)
        else:
            raise Exception("Output not allowed on pin " + str(pin.pin_number))
            
    def resetDataPins(self):
        self.writeSPPData(0)
        
    def resetControlPins(self):
        control_byte = self.readControlRegister()
        pre_control_byte = 0b11110000 & control_byte
        new_control_byte = 0b00001011 | pre_control_byte
        self.writeControlRegister(new_control_byte)
                
    def setupI2C(self, sda_pin, scl_pin, baudrate=400000):
        return I2C(self, sda_pin, scl_pin, baudrate)