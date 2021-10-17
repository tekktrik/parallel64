import json
from typing import List, Optional
from .standard_port import StandardPort
from .enhanced_port import EnhancedPort
from .extended_port import ExtendedPort
from .gpio_port import GPIOPort

class ParallelPort:
    
    def __init__(self, spp_base_address: int = None, ecp_base_address: int = None, windll_location: Optional[str] = None, port_modes: List[str] = []):
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
    def from_json(cls, json_filepath: str) -> 'ParallelPort':
        with open(json_filepath, 'r') as json_file:
            json_contents = json.load(json_file)
        try:
            if json_contents["spp_base_address"] != None:
                spp_base_add = int(json_contents["spp_base_address"], 16)
            if json_contents["ecp_base_address"] != None:
                ecp_base_add = int(json_contents["ecp_base_address"], 16)
            try:
                windll_loc = json_contents["windll_location"]
            except KeyError:
                windll_loc = None
            port_modes = json_contents["port_modes"]
            return cls(spp_base_add, ecp_base_add, windll_loc, port_modes)
        except KeyError as err:
            raise KeyError("Unable to find " + str(err) + " parameter in the JSON file, see reference documentation")