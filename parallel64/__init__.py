import sys

if sys.platform == 'win32':
    #if platform.architecture()[0] == '64bit':
    from .parallel_port import ParallelPort
    from .standard_port import StandardPort
    from .enhanced_port import EnhancedPort
    from .extended_port import ExtendedPort
    from .gpio_port import GPIOPort
    #else:
    #    raise Exception("parallel64 is mean for 64-bit systems only, 32-bit systems may still be able to use packages like pyparallel")
else:
    raise Exception("parallel64 is meant for Windows systems only")