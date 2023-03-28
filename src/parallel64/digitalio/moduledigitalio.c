// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "helper/modsetup.h"
#include "helper/enumfactory.h"
#include "DigitalInOut.h"


static struct PyModuleDef parallel64digitalio_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "digitalio",
    .m_doc = "Digital I/O for parallel ports",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_digitalio(void) {

    PyObject *module = PyModule_Create(&parallel64digitalio_module);
    if (!module) {
        return NULL;
    }

    IMPORTMOD("enum");

    pyenum_t drivemode_enum[] = {
        {"PUSH_PULL", 0},
        {"OPEN_DRAIN", 1},
    };
    PyObject *drivemode_pyenum = create_enum("DriveMode", drivemode_enum, 2);
    PyModule_AddObject(module, "DriveMode", drivemode_pyenum);

    pyenum_t direction_enum[] = {
        {"INPUT", 0},
        {"OUTPUT", 1},
    };
    PyObject *direction_pyenum = create_enum("Direction", direction_enum, 2);
    PyModule_AddObject(module, "Direction", direction_pyenum);

    pyenum_t pull_enum[] = {
        {"UP", 0},
        {"DOWN", 1},
    };
    PyObject *pull_pyenum = create_enum("Pull", pull_enum, 2);
    PyModule_AddObject(module, "Pull", pull_pyenum);

    return module;

}
