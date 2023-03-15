// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"


static int parallel64_exec(PyObject *module) {
    PyTypeObject *_BasePort_type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &_BasePort_Spec,
        NULL
    );
    if (_BasePort_type == NULL) {
        return -1;
    }
    int type_added = PyModule_AddType(module, _BasePort_type);
    Py_DECREF(_BasePort_type);
    if (type_added != 0) {
        return -1;
    }
    return 0;
}


static PyModuleDef_Slot parallel64_slots[] = {
    {Py_mod_exec, parallel64_exec},
    {0, NULL}
};


static struct PyModuleDef _parallel64module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "parallel64",
    .m_doc = "Behind the scenes extension for operating the parallel port",
    .m_size = 0,
    .m_slots = parallel64_slots,
};

PyMODINIT_FUNC PyInit_parallel64(void) {
    return PyModuleDef_Init(&_parallel64module);
}