import time
import threading

class PWM:

    class PWMCycle():
    
        def __init__(self, pwm_object):
            self._pwm_object = pwm_object
            self._end_cycle = threading.Event()
            self._pwm_thread = threading.Thread(target=self.runCycle, args=())
            self._pwm_thread.daemon = True
            self._pwm_thread.start()
            
        def runCycle(self):
            
            on_time = self._pwm_object.cycle_time*self._pwm_object._duty_cycle
            off_time = self._pwm_object.cycle_time - on_time
            
            while not self._end_cycle.is_set():
                self._pwm_object._port.writePin(self._pwm_object._pin, True)
                on_delay = time.monotonic() + on_time
                while time.monotonic() < on_delay:
                    pass
                self._pwm_object._port.writePin(self._pwm_object._pin, False)
                off_delay = time.monotonic() + off_time
                while time.monotonic() < off_delay:
                    pass
            end_time = time.time()
                    
        def stopCycle(self):
            self._end_cycle.set()
            
        def shouldStop(self):
            return self._end_cycle.is_set()
    
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
        self._pwm_thread = self.PWMCycle(self)
        
    def endCycle(self):
        self._pwm_thread.stopCycle()