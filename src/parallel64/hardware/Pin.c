// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>
#include <stdbool.h>

#include "core/portio.h"
#include "gpio/GPIO.h"
#include "hardware/Pin.h"


static PyObject* Pin_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(PinObject, type, 0);
}


static int Pin_init(PinObject *self, PyObject *args) {


    // Parse arguments (unique)
    PyObject *gpio;
    uint16_t reg_addr;
    uint8_t bit_index, drive_mode, pull, direction;
    bool hw_inverted, input_allowed, output_allowed, propagate_dir;

    if (!PyArg_ParseTuple(
        args,
        "OHBBBBBBBB",
        &gpio,
        &reg_addr,
        &bit_index,
        &direction,
        &hw_inverted,
        &input_allowed,
        &output_allowed,
        &drive_mode,
        &pull,
        &propagate_dir)
    ) {
        return -1;
    }

    GPIOObject *temp = self->gpio;
    Py_INCREF(gpio);
    self->gpio = (GPIOObject *)gpio;
    Py_XDECREF(temp);

    self->reg_addr = reg_addr;
    self->bit_index = bit_index;
    self->in_use = false;
    self->direction = input_allowed ? PORT_DIR_REVERSE : direction;
    self->hw_inverted = hw_inverted;
    self->input_allowed = input_allowed;
    self->output_allowed = output_allowed;
    self->drive_mode = drive_mode;
    self->pull = pull;
    self->propagate_dir = propagate_dir;

    // TODO: Add pull mode

    return 0;

}

PinObject* create_Pin(
    GPIOObject *gpio,
    uint16_t reg_addr,
    uint8_t bit_index,
    port_dir_t direction,
    bool hw_inverted,
    bool input_allowed,
    bool output_allowed,
    drive_mode_t drive_mode,
    pull_mode_t pull,
    bool propagate_dir
) {

    PyObject *args = Py_BuildValue(
        "OHBBBBBBBB",
        (PyObject *)gpio,
        reg_addr,
        bit_index,
        (uint8_t)direction,
        (uint8_t)hw_inverted,
        (uint8_t)input_allowed,
        (uint8_t)output_allowed,
        (uint8_t)drive_mode,
        (uint8_t)pull,
        (uint8_t)propagate_dir
    );
    PyObject *hw_mod = PyImport_ImportModule("parallel64.hardware");
    PyObject *pin_class = PyObject_GetAttrString(hw_mod, "Pin");
    PyObject *pin = PyObject_CallObject(pin_class, args);

    return (PinObject *)pin;

}


static int Pin_traverse(PinObject *self, visitproc visit, void *arg) {
    Py_VISIT(self->gpio);
    return 0;
}

static int Pin_clear(PinObject *self) {
    Py_CLEAR(self->gpio);
    return 0;
}

static void Pin_dealloc(PinObject *self) {
    PyObject_GC_UnTrack(self);
    Pin_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static Py_hash_t Pin_hash(PyObject *self) {
    Py_hash_t hash_value = 0;
    hash_value |= PIN_REGISTER(self);
    hash_value <<= 3;
    hash_value |= PIN_BITINDEX(self);
    return hash_value;
}

static PyObject* Pin_get_register(PyObject *self, void *closure) {
    return PyLong_FromLong(PIN_REGISTER(self));
}

static PyObject* Pin_get_bit_index(PyObject *self, void *closure) {
    return PyLong_FromLong(PIN_BITINDEX(self));
}

static PyObject* Pin_get_input_allowed(PyObject *self, void *closure) {
    return PyBool_FromLong(PIN_INPUTALLOWED(self));
}

static PyObject* Pin_get_output_allowed(PyObject *self, void *closure) {
    return PyBool_FromLong(PIN_OUTPUTALLOWED(self));
}

static PyObject* Pin_get_in_use(PyObject *self, void *closure) {
    return PyBool_FromLong(PIN_INUSE(self));
}


static PyGetSetDef Pin_getsetters[] = {
    {"register", (getter)Pin_get_register, NULL, "Register associated with this Pin", NULL},
    {"bit_index", (getter)Pin_get_bit_index, NULL, "Bit index on the register associated with this Pin", NULL},
    {"input_allowed", (getter)Pin_get_input_allowed, NULL, "Whether input is allowed for Pin", NULL},
    {"output_allowed", (getter)Pin_get_output_allowed, NULL, "Whether output is allowed for this Pin", NULL},
    {"in_use", (getter)Pin_get_in_use, NULL, "Whether the Pin is currently in use for for I/O", NULL},
    {NULL}
};


PyTypeObject PinType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.hardware.Pin",
    .tp_basicsize = sizeof(PinObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an port pins",
    .tp_alloc = PyType_GenericAlloc,
    .tp_new = (newfunc)Pin_new,
    .tp_init = (initproc)Pin_init,
    .tp_dealloc = (destructor)Pin_dealloc,
    .tp_traverse = (traverseproc)Pin_traverse,
    .tp_clear = (inquiry)Pin_clear,
    .tp_free = PyObject_GC_Del,
    .tp_hash = (hashfunc)Pin_hash,
    .tp_getset = Pin_getsetters,
};
