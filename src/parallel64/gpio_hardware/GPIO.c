// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "core/portio.h"
#include "gpio_hardware/GPIO_Pin.h"
#include "ports/StandardPort.h"


static PyObject* GPIO_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    return (PyObject *)PyObject_GC_NewVar(GPIOObject, type, 0);
}


static bool GPIO_setup_pins(GPIOObject *self, StandardPortObject *port) {

    uint16_t spp_data_address = SPP_DATA_ADDR(port->spp_address);
    uint16_t spp_status_address = SPP_CONTROL_ADDR(port->spp_address);
    uint16_t spp_control_address = SPP_CONTROL_ADDR(port->spp_address);

    bool is_bidir = port->is_bidir;

    self->strobe = create_Pin(self, spp_control_address, 0, PORT_DIR_REVERSE, true, true, true);
    self->auto_linefeed = create_Pin(self, spp_control_address, 1, PORT_DIR_REVERSE, true, true, true);
    self->initialize = create_Pin(self, spp_control_address, 2, PORT_DIR_REVERSE, false, true, true);
    self->select_printer = create_Pin(self, spp_control_address, 3, PORT_DIR_REVERSE, true, true, true);

    self->ack = create_Pin(self, spp_status_address, 6, PORT_DIR_REVERSE, false, true, false);
    self->busy = create_Pin(self, spp_status_address, 7, PORT_DIR_REVERSE, true, true, false);
    self->paper_out = create_Pin(self, spp_status_address, 5, PORT_DIR_REVERSE, false, true, false);
    self->select_in = create_Pin(self, spp_status_address, 4, PORT_DIR_REVERSE, false, true, false);
    self->error = create_Pin(self, spp_status_address, 3, PORT_DIR_REVERSE, false, true, false);

    self->d0 = create_Pin(self, spp_data_address, 0, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d1 = create_Pin(self, spp_data_address, 1, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d2 = create_Pin(self, spp_data_address, 2, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d3 = create_Pin(self, spp_data_address, 3, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d4 = create_Pin(self, spp_data_address, 4, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d5 = create_Pin(self, spp_data_address, 5, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d6 = create_Pin(self, spp_data_address, 6, PORT_DIR_REVERSE, false, is_bidir, false);
    self->d7 = create_Pin(self, spp_data_address, 7, PORT_DIR_REVERSE, false, is_bidir, false);

    PinObject **pinlist = malloc(sizeof(PinObject *) * 17);
    pinlist[0] = self->strobe;
    pinlist[1] = self->d0;
    pinlist[2] = self->d1;
    pinlist[3] = self->d2;
    pinlist[4] = self->d3;
    pinlist[5] = self->d4;
    pinlist[6] = self->d5;
    pinlist[7] = self->d6;
    pinlist[8] = self->d7;
    pinlist[9] = self->ack;
    pinlist[10] = self->busy;
    pinlist[11] = self->paper_out;
    pinlist[12] = self->select_in;
    pinlist[13] = self->auto_linefeed;
    pinlist[14] = self->error;
    pinlist[15] = self->initialize;
    pinlist[16] = self->select_printer;
    self->pinlist = pinlist;

    return true;
}

static int GPIO_init(GPIOObject *self, PyObject *args, PyObject *kwds) {

    // Parse arguments (unique)
    PyObject *port = NULL;

    static char *keywords[] = {"port", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", keywords, &port)) {
        return -1;
    }

    if (!PyType_IsSubtype(Py_TYPE(port), &StandardPortType)) {
        // TODO: Set specific error
        return -1;
    };
    PyObject *temp = self->port;
    Py_INCREF(port);
    self->port = port;
    Py_XDECREF(temp);

    if (!GPIO_setup_pins(self, (StandardPortObject *)port)) {
        // TODO: Set specific error
        return -1;
    }

    return 0;

}


static int GPIO_traverse(GPIOObject *self, visitproc visit, void *arg) {
    Py_VISIT(self->port);

    Py_VISIT(self->strobe);
    Py_VISIT(self->auto_linefeed);
    Py_VISIT(self->initialize);
    Py_VISIT(self->select_printer);

    Py_VISIT(self->ack);
    Py_VISIT(self->busy);
    Py_VISIT(self->paper_out);
    Py_VISIT(self->select_in);
    Py_VISIT(self->error);

    Py_VISIT(self->d0);
    Py_VISIT(self->d1);
    Py_VISIT(self->d2);
    Py_VISIT(self->d3);
    Py_VISIT(self->d4);
    Py_VISIT(self->d5);
    Py_VISIT(self->d6);
    Py_VISIT(self->d7);

    return 0;
}

static int GPIO_clear(GPIOObject *self) {
    Py_CLEAR(self->port);

    Py_CLEAR(self->strobe);
    Py_CLEAR(self->auto_linefeed);
    Py_CLEAR(self->initialize);
    Py_CLEAR(self->select_printer);

    Py_CLEAR(self->ack);
    Py_CLEAR(self->busy);
    Py_CLEAR(self->paper_out);
    Py_CLEAR(self->select_in);
    Py_CLEAR(self->error);

    Py_CLEAR(self->d0);
    Py_CLEAR(self->d1);
    Py_CLEAR(self->d2);
    Py_CLEAR(self->d3);
    Py_CLEAR(self->d4);
    Py_CLEAR(self->d5);
    Py_CLEAR(self->d6);
    Py_CLEAR(self->d7);

    return 0;
}

static void GPIO_dealloc(GPIOObject *self) {
    PyObject_GC_UnTrack(self);
    free(self->pinlist);
    GPIO_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject* GPIO_get_pin(PyObject *self, void *closure) {
    PinObject *obj = ((GPIOObject *)self)->pinlist[*(uint8_t *)closure];
    Py_INCREF(obj);
    return (PyObject *)obj;
}


static PyGetSetDef GPIO_getsetters[] = {
    {"STROBE", (getter)GPIO_get_pin, NULL, "Strobe pin", &(uint8_t){0}},
    {"D0", (getter)GPIO_get_pin, NULL, "D0 pin", &(uint8_t){1}},
    {"D1", (getter)GPIO_get_pin, NULL, "D1 pin", &(uint8_t){2}},
    {"D2", (getter)GPIO_get_pin, NULL, "D2 pin", &(uint8_t){3}},
    {"D3", (getter)GPIO_get_pin, NULL, "D3 pin", &(uint8_t){4}},
    {"D4", (getter)GPIO_get_pin, NULL, "D4 pin", &(uint8_t){5}},
    {"D5", (getter)GPIO_get_pin, NULL, "D5 pin", &(uint8_t){6}},
    {"D6", (getter)GPIO_get_pin, NULL, "D6 pin", &(uint8_t){7}},
    {"D7", (getter)GPIO_get_pin, NULL, "D7 pin", &(uint8_t){8}},
    {"ACK", (getter)GPIO_get_pin, NULL, "ACK pin", &(uint8_t){9}},
    {"BUSY", (getter)GPIO_get_pin, NULL, "BUSY pin", &(uint8_t){10}},
    {"PAPER_OUT", (getter)GPIO_get_pin, NULL, "PAPER OUT pin", &(uint8_t){11}},
    {"SELECT_IN", (getter)GPIO_get_pin, NULL, "SELECT IN pin", &(uint8_t){12}},
    {"AUTO_LINEFEED", (getter)GPIO_get_pin, NULL, "AUTO LINEFEED pin", &(uint8_t){13}},
    {"ERROR", (getter)GPIO_get_pin, NULL, "ERROR pin", &(uint8_t){14}},
    {"INITIALIZE", (getter)GPIO_get_pin, NULL, "INITIALIZE pin", &(uint8_t){15}},
    {"SELECT_PRINTER", (getter)GPIO_get_pin, NULL, "SELECT PRINTER pin", &(uint8_t){16}},
    {NULL}
};


PyTypeObject GPIOType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "parallel64.gpio.GPIO",
    .tp_basicsize = sizeof(GPIOObject),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_doc = "Class for representing an EPP port",
    .tp_alloc = PyType_GenericAlloc,
    .tp_dealloc = (destructor)GPIO_dealloc,
    .tp_traverse = (traverseproc)GPIO_traverse,
    .tp_clear = (inquiry)GPIO_clear,
    .tp_new = (newfunc)GPIO_new,
    .tp_init = (initproc)GPIO_init,
    .tp_free = PyObject_GC_Del,
    .tp_getset = GPIO_getsetters
};
