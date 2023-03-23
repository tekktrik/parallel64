# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Installation script for parallel64.
"""

from setuptools import setup, Extension

module = Extension(
    "parallel64.ports",
    [
        "src/parallel64/ports/moduleports.c",
        "src/parallel64/ports/pyportio.c",
        "src/parallel64/ports/StandardPort.c",
        "src/parallel64/ports/EnhancedPort.c",
        "src/parallel64/ports/ExtendedPort.c",
    ],
)

setup(
    ext_modules=[module],
)
