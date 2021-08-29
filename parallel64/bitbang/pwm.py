import time
import multiprocessing as mp

class PWM:
    
    def __init__(self, gpio_port, pwm_pin, duty_cycle=0, cycle_time=0.001):
        self._port = gpio_port
        self._pin = pwm_pin
        self._duty_cycle = duty_cycle
        self.cycle_time
        self._pwm_process = None
        
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
            
    def _pwmCycle(self):
        on_time = cycle_time*self._duty_cycle
        off_time = cycle_time - on_time
        while True:
            self._port.writePin(self._pin, True)
            on_delay = time.monotonic() + on_time
            while time.monotonic() < on_delay:
                pass
            self._port.writePin(self._pin, False)
            off_delay = time.monotonic() + off_time
            while time.monotonic() < off_delay:
                pass
            
            
    def startCycle(self):
        self._pwm_process = mp.Process(target=_pwmCycle)
        self._pwm_process.daemon = True
        self._pwm_process.start()
        
    def endCycle(self):
        self._pwm_process.terminate()
        while self._pwm_process.is_alive:
            pass
        self._pwm_process.join()