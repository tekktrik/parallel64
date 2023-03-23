// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "core/portio.h"
#include "pyportio.h"
#include "StandardPort.h"
#include "EnhancedPort.h"


static PyObject* EnhancedPort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(EnhancedPortObject, type, 0);
}

static int EnhancedPort_init(EnhancedPortObject *self, PyObject *args, PyObject *kwds) {

    // Parse arguments (unique)
    const uint16_t spp_address;
    bool reset_control = true;
    PyObject *is_bidir = Py_None;

    static char *keywords[] = {"spp_base_address", "reset_control", "bidirectional", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "H|$pO", keywords, &spp_address, &reset_control, &is_bidir)) {
        return -1;
    }

    // Initialize structure (should be used in subclasses)
    if (!EnhancedPort_self_init(self, spp_address, is_bidir, reset_control)) {
        return -1;
    }

    return 0;

}


bool EnhancedPort_self_init(EnhancedPortObject *self, uint16_t spp_address, PyObject *is_bidir, bool reset_control) {

    const uint16_t addresses[] = {
        EPP_DATA_ADDR(spp_address),
        EPP_ADDRESS_ADDR(spp_address)
    };
    const uint16_t num_addresses = sizeof(addresses) / sizeof(uint16_t);
    if (pyportio_init_ports(addresses, num_addresses) < 0) {
        return false;
    }

    return StandardPort_self_init(P64_AS_STANDARD(self), spp_address, is_bidir, reset_control);

}


static void EnhancedPort_dealloc(EnhancedPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject* EnhancedPort_write_epp_data(PyObject *self, PyObject *args) {
    return pyportio_parse_multiwrite(self, args, SPPADDRESS(self), EPP_DATA_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_read_epp_data(PyObject *self, PyObject *args) {
    return pyportio_parse_multiread(self, args, SPPADDRESS(self), EPP_DATA_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_write_epp_address(PyObject *self, PyObject *args) {
    return pyportio_parse_multiwrite(self, args, SPPADDRESS(self), EPP_ADDRESS_ADDR(SPPADDRESS(self)));
}

static PyObject* EnhancedPort_read_epp_address(PyObject *self, PyObject *args) {
    return pyportio_parse_multiread(self, args, SPPADDRESS(self), EPP_ADDRESS_ADDR(SPPADDRESS(self)));
}


static PyObject* EnhancedPort_get_port_address(PyObject *self, void *closure) {
    return PyLong_FromLong(((StandardPortObject *)self)->spp_address + *(uint16_t *)closure);
}


static PyGetSetDef EnhancedPort_getsetters[] = {
    {"epp_address_address", (getter)EnhancedPort_get_port_address, NULL, "EPP address address", &(uint16_t){3}},
    {"epp_data_address", (getter)EnhancedPort_get_port_address, NULL, "EPP data address", &(uint16_t){4}},
    {NULL}
};


static PyMethodDef EnhancedPort_methods[] = {
    {"write_epp_data", (PyCFunction)EnhancedPort_write_epp_data, METH_VARARGS, "Write data via EPP protocol"},
    {"write_epp_address", (PyCFunction)EnhancedPort_write_epp_address, METH_VARARGS, "Write address via EPP protocol"},
    {"read_epp_data", (PyCFunction)EnhancedPort_read_epp_data, METH_VARARGS, "Read data via EPP protocol"},
    {"read_epp_address", (PyCFunction)EnhancedPort_read_epp_address, METH_VARARGS, "Read address via EPP protocol"},
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
    .tp_base = &StandardPortType,
    .tp_methods = EnhancedPort_methods,
    .tp_getset = EnhancedPort_getsetters
};
