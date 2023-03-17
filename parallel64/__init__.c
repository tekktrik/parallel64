// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"
#include "StandardPort.h"

#define ADDNEWTYPE(NEW_TYPE, MODULE_OBJ) do \
{ \
    if (PyType_Ready(&NEW_TYPE##Type) < 0) { \
        return NULL; \
    } \
    Py_INCREF(&NEW_TYPE##Type); \
    PyModule_AddObject(MODULE_OBJ, #NEW_TYPE, (PyObject *)&NEW_TYPE##Type); \
} while (0);\


static struct PyModuleDef parallel64module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "parallel64",
    .m_doc = "Behind the scenes extension for operating the parallel port",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_parallel64(void) {

    PyObject *module = PyModule_Create(&parallel64module);
    if (!module) {
        return NULL;
    }

    ADDNEWTYPE(_BasePort, module)
    ADDNEWTYPE(StandardPort, module)

    return module;

}