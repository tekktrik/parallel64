import sys
import platform

if sys.platform == 'win32':
    if platform.architecture()[0] != '64bit':
        from parallel64.simple_port import SimplePort
        from parallel64.extended_port import ExtendedPort
    else:
        raise Exception("parallel64 is mean for 64-bit systems only, 32-bit systems may still be able to use packages like pyparallel")
else:
    raise Exception("parallel64 is meant for Windows systems only")