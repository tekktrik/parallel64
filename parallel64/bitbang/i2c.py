from time import monotonic
import warnings

class I2C:
    
    def __init__(self, gpio_port, sda_pin, scl_pin, baudrate):
        self._port = gpio_port
        self._SDA = sda_pin
        self._SCL = scl_pin
        self._baudrate = baudrate
        self._delay = (1/self.baudrate)/2
        
    @property
    def SDA(self):
        return self._SDA
    
    @SDA.setter
    def SDA(self, sda_pin):
        if sda_pin.isOutputAllowed() and sda_pin.isInputAllowed():
            # Give a warning if this pin is a DataPin
            self._sda = sda_pin
        else:
            raise Exception("Cannot set this pin as SDA: input and/or output is not allowed")
        pass
    
    @property
    def SCL(self):
        return self._SCL
    
    @SCL.setter
    def SCL(self, scl_pin):
        if scl_pin.isOutputAllowed():
            self._scl = scl_pin
        else:
            raise Exception("Cannot set this pin as SCL: output is not allowed")
    
    @property
    def baudrate(self):
        return self._baudrate
    
    @baudrate.setter
    def baudrate(self, baudrate):
        # Check if this baudrate is allow (is that even a thing?)
        self._baudrate = baudrate
        
    #def _startComm(self)
    