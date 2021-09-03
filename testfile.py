import time
import parallel64
from parallel64.bitbang.bitbang_pwm import PWM

port = parallel64.GPIOPort(0xEEFC)
port.writePin(port.Pins.INITIALIZE, True)
pwm = PWM(port, port.Pins.STROBE, 0.5, 0.01)
pwm.start()
print(3)
time.sleep(5)
pwm.stop()
pwm = PWM(port, port.Pins.STROBE, 0.25, 0.01)
pwm.start()
print(4)
time.sleep(5)
pwm.stop()