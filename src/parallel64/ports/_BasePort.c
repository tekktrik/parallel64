// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"




static int _BasePort_init(_BasePortObject *self, PyObject *args, PyObject *kwds) {

    const uint16_t spp_address;
    bool reset_control = true;

    static char *keywords[] = {"spp_base_address", "reset_control", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "H|p", keywords, &spp_address, &reset_control)) {
        return -1;
    }

    init_result_t init_result = portio_init_ports(spp_address, 3);
    switch (init_result) {
    case INIT_SUCCESS:
        break;
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

static void _BasePort_dealloc(_BasePortObject *self) {
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject* _BasePort_write_data_register(PyObject *self, PyObject *args) {
    return portio_parse_write(SPPDATA(((_BasePortObject *)self)->spp_address), args);
}

static PyObject* _BasePort_write_control_register(PyObject *self, PyObject *args) {
    return portio_parse_write(SPPCONTROL(((_BasePortObject *)self)->spp_address), args);
}

static PyObject* _BasePort_read_data_register(PyObject *self, PyObject *args) {
    return portio_parse_read(SPPDATA(((_BasePortObject *)self)->spp_address));
}

static PyObject* _BasePort_read_status_register(PyObject *self, PyObject *args) {
    return portio_parse_read(SPPSTATUS(((_BasePortObject *)self)->spp_address));
}

static PyObject* _BasePort_read_control_register(PyObject *self, PyObject *args) {
    return portio_parse_read(SPPCONTROL(((_BasePortObject *)self)->spp_address));
}

//static PyObject* StandardPort_test_bidirectionality(PyObject *self, PyObject *args) {
//
//}


static PyObject* _BasePort_get_port_address(PyObject *self, void *closure) {
    return PyLong_FromLong(((_BasePortObject *)self)->spp_address + *(uint16_t *)closure);
}

static PyObject* _BasePort_get_direction(PyObject *self, PyObject *args) {
    PyObject *constmod = PyImport_AddModule("parallel64.constants");
    PyObject *direnum = PyObject_GetAttrString(constmod, "Direction");
    uint8_t direction_byte = portio_get_port_direction(((_BasePortObject *)self)->spp_address);
    PyObject *direction = PyObject_CallFunction(direnum, "(i)", direction_byte);
    return direction;
}

static int _BasePort_set_direction(PyObject *self, PyObject *value, void *closure) {
    const uint16_t spp_base_addr = ((_BasePortObject *)self)->spp_address;
    PyObject *dirobjvalue = PyObject_GetAttrString(value, "value");
    port_dir_t dirvalue = (port_dir_t)PyLong_AsLong(dirobjvalue);
    portio_set_port_direction(spp_base_addr, dirvalue);
    return 0;
}


static PyGetSetDef _BasePort_getsetters[] = {
    {"spp_data_address", (getter)_BasePort_get_port_address, NULL, "SPP data address", &(uint16_t){0}},
    {"spp_status_address", (getter)_BasePort_get_port_address, NULL, "SPP status address", &(uint16_t){1}},
    {"spp_control_address", (getter)_BasePort_get_port_address, NULL, "SPP control address", &(uint16_t){2}},
    {"direction", (getter)_BasePort_get_direction, (setter)_BasePort_set_direction, "Direction of the port", NULL},
    {NULL}
};

static PyMethodDef _BasePort_methods[] = {
    {"write_data_register", (PyCFunction)_BasePort_write_data_register, METH_VARARGS, "Write data to the SPP data register"},
    {"write_control_register", (PyCFunction)_BasePort_write_control_register, METH_VARARGS, "Write data to the SPP control register"},
    {"read_data_register", (PyCFunction)_BasePort_read_data_register, METH_NOARGS, "Read data from the SPP data register"},
    {"read_status_register", (PyCFunction)_BasePort_read_status_register, METH_NOARGS, "Read data from the SPP status register"},
    {"read_control_register", (PyCFunction)_BasePort_read_control_register, METH_NOARGS, "Read data from the SPP control register"},
    {NULL}
};


PyTypeObject _BasePortType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.ports._BasePort",
    .tp_basicsize = sizeof(_BasePortObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Base class for all ports",
    .tp_init = (initproc)_BasePort_init,
    .tp_dealloc = (destructor)_BasePort_dealloc,
    .tp_methods = _BasePort_methods,
    .tp_getset = _BasePort_getsetters,
};
