# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

import parallel64.ports

thing = parallel64.ports.StandardPort(100)
thing.read_data_register()
