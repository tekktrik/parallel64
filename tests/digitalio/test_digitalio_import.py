# SPDX-FileCopyrightText: 2023 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Tests import of digitalio submodule
"""

def test_digitalio_import():
    try:
        import parallel64.digitalio
    except:
        assert False
