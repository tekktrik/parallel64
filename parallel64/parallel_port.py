import ctypes
import json
import os
import sys
from parallel64.standard_port import StandardPort
from parallel64.enhanced_port import EnhancedPort
from parallel64.extended_port import ExtendedPort
from parallel64.gpio_port import GPIOPort

class ParallelPort:
    
    def __init__(self, spp_base_address=None, ecp_base_address=None, windll_location=None, port_modes=[]):
        self.StandardPort = None
        self.EnhancedPort = None
        self.ExtendedPort = None
        self.GPIOPort = None
        self.modes = port_modes
        for mode in self.modes:
            if mode.lower() == "spp":
                self.StandardPort = StandardPort(spp_base_address, windll_location)
            if mode.lower() == "epp":
                self.EnhancedPort = EnhancedPort(spp_base_address, windll_location)
            if mode.lower() == "ecp":
                self.ExtendedPort = ExtendedPort(ecp_base_address, windll_location)
            if mode.lower() == "gpio":
                self.GPIOPort = GPIOPort(spp_base_address, windll_location)
        
    @classmethod
    def fromJSON(cls, json_filepath):
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            if json_contents["spp_base_address"] != None:
                spp_base_add = int(json_contents["spp_base_address"], 16)
            if json_contents["spp_base_address"] != None:
                ecp_base_add = int(json_contents["spp_base_address"], 16)
            windll_loc = json_contents["windll_location"]
            port_modes = json_contents["port_modes"]
            return cls(spp_base_add, ecp_base_add, windll_location, port_modes)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")