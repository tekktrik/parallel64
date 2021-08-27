import sys

if sys.platform == 'win32':
    #if platform.architecture()[0] == '64bit':
    from parallel64.standard_port import StandardPort
    from parallel64.enhanced_port import EnhancedPort
    from parallel64.extended_port import ExtendedPort
    from parallel64.gpio_port import GPIOPort
    #else:
    #    raise Exception("parallel64 is mean for 64-bit systems only, 32-bit systems may still be able to use packages like pyparallel")
else:
    raise Exception("parallel64 is meant for Windows systems only")