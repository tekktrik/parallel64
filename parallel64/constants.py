# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`parallel64.constants`

Constants as enums used for during typical operation of a
parrallel port


* Author(s): Alec Delaney

"""

from enum import Enum


class Direction(Enum):
    """Enum class representing the current direction of the port

    Used with :class:`parallel64.StandardPort`
    """

    REVERSE = 0
    FORWARD = 1


class CommMode(Enum):
    """Enum class representing the various protocols the ECR might
    be configureable for (port-dependent).  Note that more available
    modes may be added as this project progresses.

    Used with :class:`parallel64.ExtendedPort`
    """

    SPP = 0
    BYTE = 1
    # SPP_FIFO = 2
    # ECP_FIFO = 3
    EPP = 4
    # FIFO_TEST = 6
    # CONFIG = 7
