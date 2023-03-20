// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <stdbool.h>
#include "portio.h"
#include "_BasePort.h"
#include "StandardPort.h"

// TODO: Remove this later
#include <stdio.h>


static PyObject* StandardPort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(StandardPortObject, type, 0);
}


static int StandardPort_init(StandardPortObject *self, PyObject *args, PyObject *kwds) {
    if (_BasePortType.tp_init((PyObject *)self, args, kwds) < 0) {
        return -1;
    }
    return 0;
}


static void StandardPort_dealloc(StandardPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


PyTypeObject StandardPortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.ports.StandardPort",
    .tp_basicsize = sizeof(StandardPortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an SPP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)StandardPort_dealloc,
    .tp_new = (newfunc)StandardPort_new,
    .tp_init = (initproc)StandardPort_init,
    .tp_free = PyObject_GC_Del,
    .tp_base = &_BasePortType,
};
