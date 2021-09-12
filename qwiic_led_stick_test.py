import parallel64

class LEDStick:

    class COMMANDS:
        WRITE_ALL_LED_BRIGHTNESS = 0x77

    def __init__(self, port, i2c_address, sda_pin, scl_pin):
        self._port = port
        self._i2c_address = i2c_address
        self._sda_pin = sda_pin
        self._scl_pin = scl_pin
        self._i2c = parallel64.bitbang.bitbang_i2c.I2C(port, self._sda_pin, self._scl_pin)
        
    def setLEDBrightness(self, value):
        return self._i2c.write(self._i2c_address, [self.COMMANDS.WRITE_ALL_LED_BRIGHTNESS, value])
        
port = parallel64.GPIOPort(0xEEFC)
led_stick = LEDStick(port, 0x23, port.Pins.STROBE, port.Pins.AUTO_LINEFEED)
print(led_stick.setLEDBrightness(15))