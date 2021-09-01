import parallel64.bitbang.cython_protocols.bitbang_pwm as pwm_pyd

class PWM:
    
    def __init__(self, gpio_port, pwm_pin, duty_cycle=0, cycle_time=0.03):
        self._port = gpio_port
        self._pin = pwm_pin
        self._duty_cycle = duty_cycle
        self.cycle_time = cycle_time
        self._pwm_thread = None
        
    @property
    def pin(self):
        return self._pin
    
    @pin.setter
    def pin(self, pwm_pin):
        if pwm_pin.isOutputAllowed():
            self._pin = pwm_pin
        else:
            raise Exception("PWM output is not available on this pin; please use a pin capable of output")
            
    @property
    def duty_cycle(self):
        return self._duty_cycle
    
    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        if (0 <= duty_cycle) and (1 >= duty_cycle):
            self._duty_cycle = duty_cycle
        else:
            raise ValueError("Duty cycle must be between 0 and 1")    
            
    def startCycle(self):
        self._port.writePin(self._pin, False)
        self._pwm_thread = pwm_pyd.PWMCycle(self._port, self._pin, self._duty_cycle, self.cycle_time)
        
    def endCycle(self):
        self._pwm_thread.stopCycle()