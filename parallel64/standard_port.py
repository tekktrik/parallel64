import os
import sys
import ctypes
from enum import Enum

class StandardPort:

    class Direction(Enum):
    
        REVERSE = 0
        FORWARD = 1
    
    def __init__(self, spp_base_address, windll_location=None, reset_control=True):
        self._spp_data_address = spp_base_address
        self._status_address = spp_base_address + 1
        self._control_address = spp_base_address + 2
        if windll_location == None:
            #parent_folder = os.path.join(__file__, "..", "..")
            #inpout_folder = [os.path.abspath(folder) for folder in os.listdir(parent_folder) if folder.startswith("InpOutBinaries")][0]
            inpout_folder = [os.path.abspath(folder) for folder in os.listdir(__file__) if folder == "inpoutdlls"][0]
            if sys.maxsize > 2**32:
                windll_location = os.path.join(inpout_folder, "inpoutx64.dll")
            else:
                windll_location = os.path.join(inpout_folder, "inpout32.dll")
        self._windll_location = windll_location
        self._parallel_port = ctypes.WinDLL(windll_location)
        self._is_bidir = True if self._testBidirectional() else False
        if reset_control:
            self.resetControlForSPPHandshake()
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            spp_base_add = int(json_contents["spp_base_address"], 16)
            windll_loc = json_contents["windll_location"]
            return cls(spp_base_add, windll_location)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")
        
    def getDirection(self):
        control_byte = self.readControlRegister()
        direction_byte = (1 << 5) & control_byte
        return self.Direction(direction_byte >> 5)
    
    def setDirection(self, direction):
        direction_byte = direction.value << 5
        control_byte = self.readControlRegister()
        new_control_byte = (1 << 5) | control_byte
        self.writeControlRegister(new_control_byte)
        
    def setReverseDirection(self):
        self.setDirection(self.Direction.REVERSE)
        
    def setForwardDirection(self):
        self.setDirection(self.Direction.FORWARD)
        
    def _testBidirectional(self):
        curr_dir = self.getDirection()
        self.setReverseDirection()
        isBidir = not bool(self.getDirection().value)
        self.setDirection(curr_dir)
        return isBidir
        
    def isBidirectional(self):
        return self._is_bidir
        
    def writeDataRegister(self, data_byte):
        self._parallel_port.DlPortWritePortUchar(self._spp_data_address, data_byte)
        
    def readDataRegister(self):
        #if self.isBidirectional():
        #    return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)
        #else:
        #    raise Exception("This port was detected not to be bidirectional, data cannot be read using the data register/pins")
        
        return self._parallel_port.DlPortReadPortUchar(self._spp_data_address)

    def writeControlRegister(self, control_byte):
        self._parallel_port.DlPortWritePortUchar(self._control_address, control_byte)
        
    def readControlRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._control_address)
        
    def readStatusRegister(self):
        return self._parallel_port.DlPortReadPortUchar(self._status_address)
        
    #-------------------------------- Need to write protocol for SPP
        
    def writeSPPData(self, data, hold_while_busy=True):
        self.resetControlForSPPHandshake()
        self.setForwardDirection()
        self.writeDataRegister(data)
        if not bool((self.readStatusRegister() & (1 << 7)) >> 7):
            raise OSError("Port is busy")
        curr_control = self.readControlRegister()
        self.writeControlRegister(curr_control | 0b00000001)
        time.sleep(0.001)
        self.writeControlRegister(curr_control)
        if hold_while_busy:
            while not bool((self.readStatusRegister() & (1 << 7)) >> 7):
                pass
        
    def readSPPData(self):
        if self.isBidirectional():
            self.resetControlForSPPHandshake()
            self.setReverseDirection()
            return self.readDataRegister()
        else:
            raise OSError("This port was detected not to be bidirectional, data cannot be read using the data register/pins")
        
    def resetControlForSPPHandshake(self):
        control_byte = self.readControlRegister()
        pre_control_byte = 0b11110000 & control_byte
        new_control_byte = 0b00000100 | pre_control_byte
        self.writeControlRegister(new_control_byte)