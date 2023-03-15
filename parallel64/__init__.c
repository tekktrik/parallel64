// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"


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

    if (PyType_Ready(&_BasePortType) < 0) {
        return NULL;
    }
    Py_INCREF(&_BasePortType);
    PyModule_AddObject(module, "_BasePort", (PyObject *)&_BasePortType);

    return module;

}