// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "helper/modsetup.h"
#include "GPIO_Pin.h"


static struct PyModuleDef parallel64hardware_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "hardware",
    .m_doc = "Hardware class(es) for GPIO",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_hardware(void) {

    PyObject *module = PyModule_Create(&parallel64hardware_module);
    if (!module) {
        return NULL;
    }

    ADDNEWTYPE(Pin, module);

    return module;

}
