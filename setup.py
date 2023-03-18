# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Installation script for parallel64.
"""

from setuptools import setup, Extension

import sys

extra_args = {}
if sys.platform == "win32":
    extra_args = {
        "package_data": {
            "parallel64": [
                "ports/inpoutx64/*.dll",
            ]
        },
    }

module = Extension(
    "parallel64.ports",
    [
        "src/parallel64/ports/moduleports.c",
        "src/parallel64/ports/_BasePort.c",
        "src/parallel64/ports/StandardPort.c",
    ],
)

setup(
    ext_modules=[module],
    packages=["parallel64"],
    package_dir={"": "src"},
    **extra_args,
)
