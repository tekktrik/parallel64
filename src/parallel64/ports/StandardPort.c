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


static PyMethodDef StandardPort_methods[] = {
    {"write_spp_data", (PyCFunction)StandardPort_write_spp_data, METH_VARARGS | METH_KEYWORDS, "Write data via SPP protocol"},
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
    .tp_base = &_BasePortType,
    .tp_methods = StandardPort_methods
};
