import threading
from typing import List, Tuple

class Pin:
    '''Class representing a pin
    '''

    def __init__(self, pin_number: int, bit_index: int, register: int, hw_inverted: bool = False):
        self.pin_number = pin_number
        self.bit_index = bit_index
        self.register = register
        self._hw_inverted = hw_inverted
        self._allow_input = None
        self._allow_output = None
        
    def is_hw_inverted(self) -> bool:
        '''Returns whether a pin is hardware inverted
        
        :rtype: bool
        '''
        return self._hw_inverted
        
    def is_output_allowed(self) -> bool:
        '''Returns whether a pin allows output
        
        :rtype: bool
        '''
        return self._allow_output
        
    def iw_input_allowed(self) -> bool:
        '''Returns whether a pin allows input
        
        :rtype: bool
        '''
        return self._allow_input

class DataPin(Pin):
    '''Class representing an individual data pin, including a class-wide threading.Lock for I/O operations
    '''
    
    register_lock = threading.Lock()
    
    def __init__(self, pin_number, bit_index, register, is_bidir):
        super().__init__(pin_number, bit_index, register, False)
        self._allow_input = True if is_bidir else False
        self._allow_output = True
        
class StatusPin(Pin):
    '''Class representing an individual status pin, including a class-wide threading.Lock for I/O operations
    '''
    
    register_lock = threading.Lock()
    
    def __init__(self, pin_number, bit_index, register, hw_inverted=False):
        super().__init__(pin_number, bit_index, register, hw_inverted)
        self._allow_input = True
        self._allow_output = False
        
class ControlPin(Pin):
    '''Class representing an individual control pin, including a class-wide threading.Lock for I/O operations
    '''
        
    register_lock = threading.Lock()
        
    def __init__(self, pin_number, bit_index, register, hw_inverted=False):
        super().__init__(pin_number, bit_index, register, hw_inverted)
        self._allow_input = True
        self._allow_output = True

class Pins:
    '''Class representing all the pins for the port (connected to registers)

    Data Pins:
    D0, D1, D2, D3, D4, D5, D6, D7

    Status Pins:
    ACK, BUSY, PAPER_OUT, SELECT_IN, ERROR

    Control Pins:
    STROBE, AUTO_LINEFEED, INITIALIZE, SELECT_PRINTER
    '''
    
    def __init__(self, data_address: int, is_bidir: bool):
        self.STROBE = ControlPin(1, 0, data_address+2, True)
        self.AUTO_LINEFEED = ControlPin(14, 1, data_address+2, True)
        self.INITIALIZE = ControlPin(16, 2, data_address+2)
        self.SELECT_PRINTER = ControlPin(17, 3, data_address+2, True)
        
        self.ACK = StatusPin(10, 6, data_address+1)
        self.BUSY = StatusPin(11, 7, data_address+1, True)
        self.PAPER_OUT = StatusPin(12, 5, data_address+1)
        self.SELECT_IN = StatusPin(13, 4, data_address+1)
        self.ERROR = StatusPin(15, 3, data_address+1)

        self.D0 = DataPin(2, 0, data_address, is_bidir)
        self.D1 = DataPin(3, 1, data_address, is_bidir)
        self.D2 = DataPin(4, 2, data_address, is_bidir)
        self.D3 = DataPin(5, 3, data_address, is_bidir)
        self.D4 = DataPin(6, 4, data_address, is_bidir)
        self.D5 = DataPin(7, 5, data_address, is_bidir)
        self.D6 = DataPin(8, 6, data_address, is_bidir)
        self.D7 = DataPin(9, 7, data_address, is_bidir)
    
    def get_named_pin_list(self) -> List[Tuple[str, Pin]]:
        '''Returns a list of pins and their names
        
        :rtype: list((str, Pin))
        '''
        return list(self.__dict__.items())
        #return [pin_name for pin_name in pin_dict if pin_name != "_parallel_port"]
        
    def get_pin_list(self) -> List[Pin]:
        '''Returns a list of pins

        :rtype: list(Pin)
        '''
        return [pin[1] for pin in self.get_named_pin_list()]
        
    def get_pin_name_list(self) -> List[str]:
        '''Return a list of pin names
        
        :rtype: list(str)
        '''
        return [pin[0] for pin in self.get_named_pin_list()]

    def get_pin_by_number(self, pin_number: int) -> Pin:
        '''Returns a pin based off of the pin number
        
        :rtype: Pin
        '''
        pin_list = self.get_pin_list()
        return [pin for pin in pin_list if pin.pin_number == pin_number][0]