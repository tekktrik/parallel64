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


PinObject* create_Pin(
    GPIOObject *gpio,
    uint16_t reg_addr,
    uint8_t bit_index,
    port_dir_t direction,
    bool hw_inverted,
    bool input_allowed,
    bool output_allowed
) {

    PinObject *pin = PyObject_GC_NewVar(PinObject, &PinType, 0);

    pin->gpio = gpio;
    Py_INCREF(gpio);

    pin->reg_addr = reg_addr;
    pin->bit_index = bit_index;
    pin->direction = direction;
    pin->hw_inverted = hw_inverted;
    pin->input_allowed = input_allowed;
    pin->output_allowed = output_allowed;

    pin->in_use = false;

    return pin;

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
    hash_value <<= 4;
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
    .tp_dealloc = (destructor)Pin_dealloc,
    .tp_traverse = (traverseproc)Pin_traverse,
    .tp_clear = (inquiry)Pin_clear,
    .tp_free = PyObject_GC_Del,
    .tp_hash = (hashfunc)Pin_hash,
    .tp_getset = Pin_getsetters,
};
