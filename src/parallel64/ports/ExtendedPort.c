// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "core/portio.h"
#include "pyportio.h"
#include "EnhancedPort.h"
#include "ExtendedPort.h"


static PyObject* ExtendedPort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(ExtendedPortObject, type, 0);
}

static int ExtendedPort_init(ExtendedPortObject *self, PyObject *args, PyObject *kwds) {

    // Parse arguments (unique)
    const uint16_t spp_address;
    const uint16_t ecp_address;
    bool reset_control = true;
    PyObject *is_bidir = Py_None;

    static char *keywords[] = {"spp_base_address", "ecp_base_address", "reset_control", "bidirectional", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "HH|$pO", keywords, &spp_address, &ecp_address, &reset_control, &is_bidir)) {
        return -1;
    }

    // Initialize structure (should be used in subclasses)
    if (!ExtendedPort_self_init(self, spp_address, ecp_address, is_bidir, reset_control)) {
        return -1;
    }

    return 0;

}


bool ExtendedPort_self_init(ExtendedPortObject *self, uint16_t spp_address, uint16_t ecp_address, PyObject *is_bidir, bool reset_control) {

    const uint16_t addresses[] = {
        ECP_DATA_ADDR(ecp_address),
        ECP_CONFIG_ADDR(ecp_address),
        ECP_ECR_ADDR(ecp_address)
    };
    const uint16_t num_addresses = sizeof(addresses) / sizeof(uint16_t);
    if (pyportio_init_ports(addresses, num_addresses) < 0) {
        return false;
    }
    self->ecp_address = ecp_address;

    return EnhancedPort_self_init(P64_AS_ENHANCED(self), spp_address, is_bidir, reset_control);

}


static void ExtendedPort_dealloc(ExtendedPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}



static PyObject* ExtendedPort_write_ecp_ecr(PyObject *self, PyObject *args) {
    return pyportio_parse_write(ECP_ECR_ADDR(ECP_ADDRESS(self)), args);
}

static PyObject* ExtendedPort_read_ecp_ecr(PyObject *self, PyObject *args) {
    return pyportio_parse_read(ECP_ECR_ADDR(ECP_ADDRESS(self)));
}


static PyObject* ExtendedPort_get_port_address(PyObject *self, void *closure) {
    return PyLong_FromLong(ECP_DATA_ADDR(ECP_ADDRESS(self)) + *(uint16_t *)closure);
}

static PyObject* ExtendedPort_get_comm_mode(PyObject *self, void *closure) {
    PyObject *constmod = PyImport_AddModule("parallel64.constants");
    PyObject *commenum = PyObject_GetAttrString(constmod, "CommMode");
    uint8_t ecr_byte = readport(ECP_ECR_ADDR(ECP_ADDRESS(self)));
    uint8_t comm_mode = P64_CHECKBITS_SHIFT(ecr_byte, 7, ECR_COMMMODE_BITINDEX);
    PyObject *direction = PyObject_CallFunction(commenum, "(i)", comm_mode);
    return direction;
}

static int ExtendedPort_set_comm_mode(PyObject *self, PyObject *value, void *closure) {
    const uint16_t ecr_addr = ECP_ECR_ADDR(ECP_ADDRESS(self));
    PyObject *commmode_objvalue = PyObject_GetAttrString(value, "value");
    uint8_t commmode_value = (uint8_t)PyLong_AsLong(commmode_objvalue);
    uint8_t blank_ecr_byte = P64_SETBITS_OFF(readport(ecr_addr), 7, ECR_COMMMODE_BITINDEX);
    uint8_t ecr_byte = P64_SETBITS_ON(blank_ecr_byte, commmode_value, ECR_COMMMODE_BITINDEX);
    writeport(ecr_addr, ecr_byte);
    return 0;
}


static PyGetSetDef ExtendedPort_getsetters[] = {
    {"ecp_data_address", (getter)ExtendedPort_get_port_address, NULL, "ECP data address", &(uint16_t){0}},
    {"ecp_config_address", (getter)ExtendedPort_get_port_address, NULL, "ECP configuration address", &(uint16_t){1}},
    {"ecp_ecr_address", (getter)ExtendedPort_get_port_address, NULL, "ECP ECR address", &(uint16_t){2}},
    {"comm_mode", (getter)ExtendedPort_get_comm_mode, (setter)ExtendedPort_set_comm_mode, "Communication mode configured in the ECR"},
    {NULL}
};


static PyMethodDef ExtendedPort_methods[] = {
    {"write_ecp_ecr", (PyCFunction)ExtendedPort_write_ecp_ecr, METH_VARARGS, "Write data to the Extended Control Register"},
    {"read_ecp_ecr", (PyCFunction)ExtendedPort_read_ecp_ecr, METH_NOARGS, "Read data from the Extended Control Register"},
    {NULL}
};


PyTypeObject ExtendedPortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.ports.ExtendedPort",
    .tp_basicsize = sizeof(ExtendedPortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an ECP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)ExtendedPort_dealloc,
    .tp_new = (newfunc)ExtendedPort_new,
    .tp_init = (initproc)ExtendedPort_init,
    .tp_free = PyObject_GC_Del,
    .tp_base = &EnhancedPortType,
    .tp_methods = ExtendedPort_methods,
    .tp_getset = ExtendedPort_getsetters
};
