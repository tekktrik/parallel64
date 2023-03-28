// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "StandardPort.h"
#include "EnhancedPort.h"
#include "ExtendedPort.h"
#include "helper/modsetup.h"
#include "helper/enumfactory.h"


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

    ADDNEWTYPE(StandardPort, module);
    ADDNEWTYPE(EnhancedPort, module);
    ADDNEWTYPE(ExtendedPort, module);

    pyenum_t direction_enum[] = {
        {"FORWARD", 0},
        {"REVERSE", 1},
    };
    PyObject *direction_pyenum = create_enum("Direction", direction_enum, 2);
    PyModule_AddObject(module, "Direction", direction_pyenum);

    pyenum_t commmode_enum[] = {
        {"SPP", 0},
        {"BYTE", 1},
        {"EPP", 4},
    };
    PyObject *commmode_pyenum = create_enum("CommMode", commmode_enum, 3);
    PyModule_AddObject(module, "CommMode", commmode_pyenum);

    return module;

}
