# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

import parallel64.ports
import parallel64.gpio

port = parallel64.ports.StandardPort(100, bidirectional=True)
gpio = parallel64.gpio.GPIO(port)

pin = gpio.SELECT_IN

pin_dict = {pin: 42}
print(pin_dict[pin])
