from parallel_port import ParallelPort
from tekkport import tekkport_errors

class TekkPort(ParallelPort):

    def readDataBitIndex(self, bit_index):
        if (bit_index >= 0) and (bit_index <=7) and isinstance(bit_index, int):
            byte_read = self._parallel_port.readSPPData()
            bit_mask = (1 << bit_index)
            return (bit_mask & byte_read) >> bit_index
        else:
            data_bit_error = tekkport_errors.BitIndexError("Bad bit index given")
            if (bit_index < 0) or (bit_index > 7):
                data_bit_error.addError(data_bit_error.BitIndexErrorCodes.INDEX_OUT_OF_RANGE)
            if not isinstance(bit_index, int):
                data_bit_error.addError(data_bit_error.BitIndexErrorCodes.NON_INTEGER_INDEX)
            raise data_bit_error
    
    def readPin(self, pin_number):
        if (pin_number >= 2) and (pin_number <= 9):
            try:
                return self.readDataBitIndex(pin_number - 1)
            except tekkport_errors.BitIndexError as bierror
                