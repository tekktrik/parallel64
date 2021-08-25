from parallel_port import port_errors

class SimplePort:

    def writeControlRegister(self, control_byte):
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def readControlRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def readStatusRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    def writeSPPData(self, data):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00000100)
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data)
        
    def readSPPData(self):
        self._parallel_port.DlPortWritePortUchar(self._control_address, 0b00100100)
        return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)

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
                