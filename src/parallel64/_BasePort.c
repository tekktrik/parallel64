// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"


static void _BasePort_dealloc(_BasePortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


PyTypeObject _BasePortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.ports._BasePort",
    .tp_basicsize = sizeof(_BasePortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Base class for all ports",
    .tp_dealloc = (destructor)_BasePort_dealloc,
};
