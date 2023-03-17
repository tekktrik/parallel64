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

    const uint16_t spp_address;
    bool reset_control = true;

    static char *keywords[] = {"spp_base_address", "reset_control", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "H|p", keywords, &spp_address, &reset_control)) {
        return -1;
    }

    init_result_t init_result = parallel64_init_ports(spp_address, 3);
    switch (init_result != INIT_SUCCESS) {
    case INIT_DLLLOAD_ERROR:
        PyErr_SetString(
            PyExc_OSError,
            "Unable to load the DLL"
        );
        return -1;
    case INIT_PERMISSION_ERROR:
        PyErr_SetString(
            PyExc_OSError,
            "Unable gain permission for the port"
        );
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

static inline PyObject* StandardPort_write_spp_control(PyObject *self, PyObject *args) {
    parallel64_parse_write(SPPCONTROL(((StandardPortObject *)self)->spp_address), args);
}

static inline PyObject* StandardPort_read_spp_data(PyObject *self, PyObject *args) {
    return parallel64_parse_read(SPPDATA(((StandardPortObject *)self)->spp_address));
}

static inline PyObject* StandardPort_read_spp_status(PyObject *self, PyObject *args) {
    return parallel64_parse_read(SPPSTATUS(((StandardPortObject *)self)->spp_address));
}

static inline PyObject* StandardPort_read_spp_control(PyObject *self, PyObject *args) {
    return parallel64_parse_read(SPPCONTROL(((StandardPortObject *)self)->spp_address));
}


static PyObject* StandardPort_get_port_address(PyObject *self, void *closure) {
    uint16_t address = ((StandardPortObject *)self)->spp_address + (uint16_t)closure;
    return PyLong_FromLong(address);
}


static PyMethodDef StandardPort_methods[] = {
    {"write_data_register", (PyCFunction)StandardPort_write_spp_data, METH_VARARGS, "Write data to the SPP data register"},
    {"write_control_register", (PyCFunction)StandardPort_write_spp_control, METH_VARARGS, "Write data to the SPP control register"},
    {"read_data_register", (PyCFunction)StandardPort_read_spp_data, METH_NOARGS, "Read data from the SPP data register"},
    {"read_status_register", (PyCFunction)StandardPort_read_spp_status, METH_NOARGS, "Read data from the SPP status register"},
    {"read_control_register", (PyCFunction)StandardPort_read_spp_control, METH_NOARGS, "Read data from the SPP control register"},
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
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an SPP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)StandardPort_dealloc,
    .tp_new = (newfunc)StandardPort_new,
    .tp_init = (initproc)StandardPort_init,
    .tp_getset = StandardPort_getsetters,
    .tp_free = PyObject_GC_Del,
    .tp_base = &_BasePortType,
    .tp_methods = &StandardPort_methods,
};
