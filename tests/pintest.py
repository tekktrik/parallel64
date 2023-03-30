# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

import parallel64.ports
import parallel64.gpio
import parallel64.hardware

port = parallel64.ports.StandardPort(100, bidirectional=True)
gpio = parallel64.gpio.GPIO(port)

print("X")
# print(dir(board.D2))
print(gpio.D2.register)
print("Y")
print(isinstance(gpio.D2, parallel64.hardware.Pin))
