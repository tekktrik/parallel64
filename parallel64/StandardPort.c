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
    return (PyObject *)PyObject_NewVar(StandardPortObject, type, 0);
}


static int StandardPort_init(StandardPortObject *self, PyObject *args, PyObject *kwds) {
    
    const uint16_t spp_address;
    bool reset_control = true;

    static char *keywords[] = {"spp_base_address", "reset_control", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "H|p", keywords, &spp_address, &reset_control)) {
        return -1;
    }

    if (parallel64_init_ports(spp_address, 3) != INIT_SUCCESS) {
        // TODO: Set more specific error
        return -1;
    }

    // TODO: Reset port if needed

    self->spp_address = spp_address;

    return 0;

}


static void StandardPort_dealloc(StandardPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static inline PyObject* StandardPort_write_spp_data(PyObject *self, PyObject *args) {
    parallel64_parse_write(SPPDATA(((StandardPortObject *)self)->spp_address), args);
}


static PyObject* StandardPort_get_port_address(PyObject *self, void *closure) {
    uint16_t address = ((StandardPortObject *)self)->spp_address + (uint16_t)closure;
    return (PyObject *)PyLong_FromLong(address);
}


static PyMethodDef StandardPort_methods[] = {
    {"write_spp_data", (PyCFunction)StandardPort_write_spp_data, METH_VARARGS, "Get the data from the SPP data register"},
    {NULL}
};


static PyGetSetDef StandardPort_getsetters[] = {
    {"spp_data_address", (getter)StandardPort_get_port_address, NULL, "SPP data address", (void *)0},
    {"spp_status_address", (getter)StandardPort_get_port_address, NULL, "SPP status address", (void *)1},
    {"spp_control_address", (getter)StandardPort_get_port_address, NULL, "SPP control address", (void *)2},
    {NULL}
};


PyTypeObject StandardPortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.StandardPort",
    .tp_basicsize = sizeof(StandardPortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Class for representing an SPP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)StandardPort_dealloc,
    .tp_new = (newfunc)StandardPort_new,
    .tp_init = (initproc)StandardPort_init,
    .tp_getset = StandardPort_getsetters,
    .tp_free = PyObject_Del,
    .tp_base = &_BasePortType,
    .tp_methods = &StandardPort_methods,
};
