# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Installation script for parallel64.
"""

from setuptools import setup, Extension

ports_module = Extension(
    "parallel64.ports",
    [
        "src/parallel64/ports/moduleports.c",
        "src/parallel64/ports/pyportio.c",
        "src/parallel64/ports/StandardPort.c",
        "src/parallel64/ports/EnhancedPort.c",
        "src/parallel64/ports/ExtendedPort.c",
    ],
    include_dirs=[
        "include",
        "src/parallel64",
    ],
)

gpio_module = Extension(
    "parallel64.gpio",
    [
        "src/parallel64/gpio/modulegpio.c",
        "src/parallel64/gpio/GPIO.c",
        "src/parallel64/hardware/Pin.c",
        "src/parallel64/ports/StandardPort.c",
        "src/parallel64/ports/pyportio.c",
    ],
    include_dirs=[
        "include",
        "src/parallel64/",
    ],
)

hardware_module = Extension(
    "parallel64.hardware",
    [
        "src/parallel64/hardware/modulehardware.c",
        "src/parallel64/hardware/Pin.c",
        "src/parallel64/gpio/GPIO.c",
        "src/parallel64/ports/StandardPort.c",
        "src/parallel64/ports/pyportio.c",
    ],
    include_dirs=[
        "include",
        "src/parallel64",
    ],
)


setup(
    ext_modules=[
        ports_module,
        gpio_module,
        hardware_module,
    ],
)
