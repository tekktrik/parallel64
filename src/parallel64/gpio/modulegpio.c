// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "helper/modsetup.h"
#include "GPIO.h"


static struct PyModuleDef parallel64gpio_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "gpio",
    .m_doc = "GPIO interface for parallel ports",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_gpio(void) {

    PyObject *module = PyModule_Create(&parallel64gpio_module);
    if (!module) {
        return NULL;
    }

    ADDNEWTYPE(GPIO, module);

    return module;

}
