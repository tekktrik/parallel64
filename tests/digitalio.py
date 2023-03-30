# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

import parallel64.ports
import parallel64.gpio
import parallel64.hardware

port = parallel64.ports.StandardPort(100, bidirectional=True)
gpio = parallel64.gpio.GPIO(port)

gpio.blinkatize()

import board
import digitalio
import microcontroller

print("X")
# print(dir(board.D2))
print(board.D2.register)
thing = board.D2
print("Y")

# Data pins
dio_data = digitalio.DigitalInOut(board.D2)
dio_data.direction = digitalio.Direction.INPUT

# Status pins
dio = digitalio.DigitalInOut(board.STROBE)

print("SSS")
