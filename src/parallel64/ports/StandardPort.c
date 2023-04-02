// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>
#include <stdbool.h>

#include "core/portio.h"
#include "pyportio.h"
#include "StandardPort.h"


static PyObject* StandardPort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(StandardPortObject, type, 0);
}


static int StandardPort_init(StandardPortObject *self, PyObject *args, PyObject *kwds) {

    // Parse arguments (unique)
    const uint16_t spp_address;
    bool reset_control = true;
    PyObject *is_bidir = Py_None;

    static char *keywords[] = {"spp_base_address", "reset_control", "bidirectional", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "H|$pO", keywords, &spp_address, &reset_control, &is_bidir)) {
        return -1;
    }

    // Initialize structure (should be used in subclasses)
    if (!StandardPort_self_init(self, spp_address, is_bidir, reset_control)) {
        return -1;
    }

    PORTTYPE(self) = "spp_port";

    return 0;

}

bool StandardPort_self_init(StandardPortObject *self, uint16_t spp_address, PyObject *is_bidir, bool reset_control) {

    // Initialize ports
    const uint16_t addresses[] = {
        SPP_DATA_ADDR(spp_address),
        SPP_STATUS_ADDR(spp_address),
        SPP_CONTROL_ADDR(spp_address)
    };
    const uint16_t num_addresses = sizeof(addresses) / sizeof(uint16_t);
    if (pyportio_init_ports(addresses, num_addresses) < 0) {
        return false;
    }

    // Initialize variables
    self->spp_address = spp_address;

    if (is_bidir == Py_True) {
        self->is_bidir = true;
    }
    else if (is_bidir == Py_False) {
        self->is_bidir = false;
    }
    else if (is_bidir == Py_None) {
        self->is_bidir = portio_test_bidirectionality(spp_address);
    }
    else {
        // TODO: Raise an exception
    }

    // Manipulate port (unique)
    if (reset_control) portio_reset_control_pins(spp_address, self->is_bidir);

    return true;

}


static void StandardPort_dealloc(StandardPortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject* StandardPort_write_spp_data(PyObject *self, PyObject *args, PyObject *kwds) {

    Py_buffer data;
    bool hold_setting = true;

    static char *keywords[] = {"", "hold_while_busy", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "y*|$p", keywords, &data, &hold_setting)) {
        return NULL;
    }

    const uint16_t spp_base_addr = SPPADDRESS(self);
    const bool is_bidir = ISBIDIR(self);

    if (is_bidir) portio_set_port_direction(spp_base_addr, PORT_DIR_FORWARD);

    for (Py_ssize_t index = 0; index < data.len; index++) {
        portio_reset_control_pins(spp_base_addr, is_bidir);
        writeport(SPP_DATA_ADDR(spp_base_addr), *((uint8_t *)data.buf + index));
        uint8_t status = readport(SPP_STATUS_ADDR(spp_base_addr));
        if (P64_CHECKBIT_UINT8(status, BUSY_BITINDEX)) {
            // TODO: Raise port busy OS error
        }
        uint8_t curr_control = readport(SPP_CONTROL_ADDR(spp_base_addr));
        writeport(SPP_CONTROL_ADDR(spp_base_addr), P64_SETBIT_ON(curr_control, 1));
        portio_delay_us(5);
        writeport(SPP_CONTROL_ADDR(spp_base_addr), curr_control);
        if (hold_setting) {
            while (true) {
                uint8_t current_status = readport(SPP_STATUS_ADDR(spp_base_addr));
                if (P64_CHECKBIT_UINT8(current_status, BUSY_BITINDEX)) break;
            }
        }
    }
    Py_RETURN_NONE;
}

static PyObject* StandardPort_write_data_register(PyObject *self, PyObject *args) {
    return pyportio_parse_write(SPP_DATA_ADDR(SPPADDRESS(self)), args);
}

static PyObject* StandardPort_write_control_register(PyObject *self, PyObject *args) {
    return pyportio_parse_write(SPP_CONTROL_ADDR(SPPADDRESS(self)), args);
}

static PyObject* StandardPort_read_data_register(PyObject *self, PyObject *args) {
    return pyportio_parse_read(SPP_DATA_ADDR(SPPADDRESS(self)));
}

static PyObject* StandardPort_read_status_register(PyObject *self, PyObject *args) {
    return pyportio_parse_read(SPP_STATUS_ADDR(SPPADDRESS(self)));
}

static PyObject* StandardPort_read_control_register(PyObject *self, PyObject *args) {
    return pyportio_parse_read(SPP_CONTROL_ADDR(SPPADDRESS(self)));
}

static PyObject* StandardPort_test_bidirectionality(PyObject *self, PyObject *args) {
    const uint16_t spp_base_addr = SPPADDRESS(self);
    bool is_bidir = portio_test_bidirectionality(spp_base_addr);
    return PyBool_FromLong(is_bidir);
}

static PyObject* StandardPort_reset_control_register(PyObject *self, PyObject *args) {
    const uint16_t spp_base_addr = SPPADDRESS(self);
    portio_reset_control_pins(spp_base_addr, ISBIDIR(self));
    Py_RETURN_NONE;
}


static PyObject* StandardPort_get_port_address(PyObject *self, void *closure) {
    return PyLong_FromLong(((StandardPortObject *)self)->spp_address + *(uint16_t *)closure);
}

static PyObject* StandardPort_get_direction(PyObject *self, void *closure) {
    PyObject *constmod = PyImport_AddModule("parallel64.ports");
    PyObject *direnum = PyObject_GetAttrString(constmod, "Direction");
    uint8_t direction_byte = portio_get_port_direction(SPPADDRESS(self));
    PyObject *direction = PyObject_CallFunction(direnum, "(i)", direction_byte);
    return direction;
}

static int StandardPort_set_direction(PyObject *self, PyObject *value, void *closure) {
    const uint16_t spp_base_addr = SPPADDRESS(self);
    PyObject *dirobjvalue = PyObject_GetAttrString(value, "value");
    port_dir_t dirvalue = (port_dir_t)PyLong_AsLong(dirobjvalue);
    portio_set_port_direction(spp_base_addr, dirvalue);
    return 0;
}

static PyObject* StandardPort_get_bidirectional(PyObject *self, void *closure) {
    return PyBool_FromLong(((StandardPortObject *)self)->is_bidir);
}


static PyGetSetDef StandardPort_getsetters[] = {
    {"spp_data_address", (getter)StandardPort_get_port_address, NULL, "SPP data address", &(uint16_t){0}},
    {"spp_status_address", (getter)StandardPort_get_port_address, NULL, "SPP status address", &(uint16_t){1}},
    {"spp_control_address", (getter)StandardPort_get_port_address, NULL, "SPP control address", &(uint16_t){2}},
    {"direction", (getter)StandardPort_get_direction, (setter)StandardPort_set_direction, "Direction of the port", NULL},
    {"bidirectional", (getter)StandardPort_get_bidirectional, NULL, "Whether the port is bidirectional", NULL},
    {NULL}
};


static PyMethodDef StandardPort_methods[] = {
    {"write_data_register", (PyCFunction)StandardPort_write_data_register, METH_VARARGS, "Write data to the SPP data register"},
    {"write_control_register", (PyCFunction)StandardPort_write_control_register, METH_VARARGS, "Write data to the SPP control register"},
    {"read_data_register", (PyCFunction)StandardPort_read_data_register, METH_NOARGS, "Read data from the SPP data register"},
    {"read_status_register", (PyCFunction)StandardPort_read_status_register, METH_NOARGS, "Read data from the SPP status register"},
    {"read_control_register", (PyCFunction)StandardPort_read_control_register, METH_NOARGS, "Read data from the SPP control register"},
    {"test_bidirectionality", (PyCFunction)StandardPort_test_bidirectionality, METH_NOARGS, "Test the bidirectionality of the port"},
    {"reset_control_register", (PyCFunction)StandardPort_reset_control_register, METH_NOARGS, "Reset the control register's output pins"},
    {"write_spp_data", (PyCFunctionWithKeywords)StandardPort_write_spp_data, METH_VARARGS | METH_KEYWORDS, "Write data via SPP protocol"},
    {NULL}
};


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
    .tp_methods = StandardPort_methods,
    .tp_getset = StandardPort_getsetters,
};
