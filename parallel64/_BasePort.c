// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>


typedef struct {
    PyObject_HEAD
} _BasePortObject;


//static PyObject* _BasePort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
//    return type->tp_alloc(type, 0);
//}


static void _BasePort_dealloc(_BasePortObject *self) {
    PyObject_GC_UnTrack(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


PyTypeObject _BasePortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64._BasePort",
    .tp_basicsize = sizeof(_BasePortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Base class for all ports",
    .tp_dealloc = (destructor)_BasePort_dealloc,
};
