from enum import Enum

class Direction(Enum):
    '''Enum class representing the current direction of the port
    '''

    REVERSE = 0
    FORWARD = 1

class CommMode(Enum):
    
    SPP = 0
    BYTE = 1
    #SPP_FIFO = 2
    #ECP_FIFO = 3
    EPP = 4
    #FIFO_TEST = 6
    #CONFIG = 7