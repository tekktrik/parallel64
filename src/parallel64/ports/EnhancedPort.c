// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "EnhancedPort.h"
#include "portio.h"
#include "_BasePort.h"
#include "StandardPort.h"


static PyObject* EnhancedPort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(StandardPortObject, type, 0);
}

static int EnhancedPort_init(StandardPortObject *self, PyObject *args, PyObject *kwds) {
    if (StandardPortType.tp_init((PyObject *)self, args, kwds) < 0) {
        return -1;
    }
    return 0;
}


static void EnhancedPort_dealloc(StandardPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject* EnhancedPort_write_epp_data(PyObject *self, PyObject *args, PyObject *kwds) {
    return _BasePort_parse_multiwrite(self, args, kwds, SPPADDRESS(self), EPP_DATA_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_read_epp_data(PyObject *self, PyObject *args, PyObject *kwds) {
    return _BasePort_parse_multiread(self, args, kwds, SPPADDRESS(self), EPP_DATA_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_write_epp_address(PyObject *self, PyObject *args, PyObject *kwds) {
    return _BasePort_parse_multiwrite(self, args, kwds, SPPADDRESS(self), EPP_ADDRESS_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_read_epp_address(PyObject *self, PyObject *args, PyObject *kwds) {
    return _BasePort_parse_multiread(self, args, kwds, SPPADDRESS(self), EPP_ADDRESS_ADDR(SPPADDRESS(self)));
}


static PyMethodDef EnhancedPort_methods[] = {
    {"write_epp_data", (PyCFunction)EnhancedPort_write_epp_data, METH_VARARGS | METH_KEYWORDS, "Write data via EPP protocol"},
    {"write_epp_address", (PyCFunction)EnhancedPort_write_epp_address, METH_VARARGS | METH_KEYWORDS, "Write address via EPP protocol"},
    {"read_epp_data", (PyCFunction)EnhancedPort_read_epp_data, METH_VARARGS | METH_KEYWORDS, "Read data via EPP protocol"},
    {"read_epp_address", (PyCFunction)EnhancedPort_read_epp_address, METH_VARARGS | METH_KEYWORDS, "Read address via EPP protocol"},
    {NULL}
};


PyTypeObject EnhancedPortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.ports.EnhancedPort",
    .tp_basicsize = sizeof(EnhancedPortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an EPP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)EnhancedPort_dealloc,
    .tp_new = (newfunc)EnhancedPort_new,
    .tp_init = (initproc)EnhancedPort_init,
    .tp_free = PyObject_GC_Del,
    .tp_base = &_BasePortType,
    .tp_methods = EnhancedPort_methods
};
