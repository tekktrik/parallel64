// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "StandardPort.h"
#include "EnhancedPort.h"
#include "ExtendedPort.h"
#include "helper/modsetup.h"


static struct PyModuleDef parallel64ports_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "ports",
    .m_doc = "Behind the scenes extension for operating the parallel port",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_ports(void) {

    PyObject *module = PyModule_Create(&parallel64ports_module);
    if (!module) {
        return NULL;
    }

    IMPORTMOD("enum");
    IMPORTMOD("parallel64.constants");

    ADDNEWTYPE(StandardPort, module);
    ADDNEWTYPE(EnhancedPort, module);
    ADDNEWTYPE(ExtendedPort, module);

    return module;

}
