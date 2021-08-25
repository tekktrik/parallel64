from enum import Enum

class TekkPortError:
    '''Base class for TekkPort errors
    '''
    
    def __init__(self, message):
        self.message = message
        
    def getMessage(self):
        return self.message
        
    def setMessage(self, message)
        self.message = message
    
class TekkPortMutliError(TekkPortError):
    '''Base class for TekkPort errors that can hold multiple errors
    '''
    
    def __init__(self, message):
        super().__init__(message)
        self.error_sum = 0
    
    def containsError(self, error_code):
        bitShift = int(math.log(error_code.value, 2))
        bitMask = 1 << bitShift
        return bool((bitMask & self.error_sum) >> bitShift)
        
    def addError(self, error_code):
        if not self.containsError(error_code):
            self.error_sum += error_code.value
            
    def hasAnyErrors(self):
        return not (self.error_sum == 0)
    
class BitIndexError(TekkPortMultiError):
    '''Exception raised when bit not available in byte, usually for reading/writing bits in the data line
    '''
    
    class BitIndexErrorCodes(Enum):
        INDEX_OUT_OF_RANGE = 1
        NON_INTEGER_INDEX = 2
    
    def __init__(self, message, index_attempted):
        super().__init__(message)
        self.index_attempted = index_attempted
        
    def getIndexAttempted(self):
        return self.index_attempted