class I2C:
    
    def __init__(self, gpio_port, sda_pin, scl_pin, baudrate):
        self.SDA = sda_pin
        self.SCL = scl_pin
        self.baudrate = baudrate
        self._delay = (1/self.baudrate)/2
        
    #def _startComm(self)
    