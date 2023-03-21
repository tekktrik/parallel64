// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef _BASEPORT_H
#define _BASEPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>

#include "portio.h"


#define SPPADDRESS(OBJECT) (((_BasePortObject *)OBJECT)->spp_address)
#define ISBIDIR(OBJECT) (((_BasePortObject *)OBJECT)->is_bidir)


typedef struct {
    PyObject_HEAD
    uint16_t spp_address;
    bool is_bidir;
} _BasePortObject;


extern PyTypeObject _BasePortType;


static inline PyObject* _BasePort_parse_multiwrite(PyObject *self, PyObject *args, PyObject *kwds, uint16_t base_address, uint16_t target_address) {
    Py_buffer data;

    static char *keywords[] = {"", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "y*", keywords, &data)) {
        return NULL;
    }

    const bool is_bidir = ISBIDIR(self);

    portio_reset_control_pins(base_address, is_bidir);
    portio_set_port_direction(base_address, PORT_DIR_FORWARD);

    for (Py_ssize_t index = 0; index < data.len; index++) {
        writeport(target_address, *((uint8_t *)data.buf + index));
        portio_reset_control_pins(base_address, is_bidir);
    }

    Py_RETURN_NONE;
}

static inline PyObject* _BasePort_parse_multiread(PyObject *self, PyObject *args, PyObject *kwds, uint16_t base_address, uint16_t target_address) {
    Py_ssize_t length;

    static char *keywords[] = {"", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "n", keywords, &length)) {
        return NULL;
    }

    const bool is_bidir = ISBIDIR(self);

    uint8_t *buffer = (uint8_t *)malloc(sizeof(uint8_t) * length);

    portio_reset_control_pins(base_address, is_bidir);
    portio_set_port_direction(base_address, PORT_DIR_REVERSE);

    for (int index = 0; index < length; index++) {
        *(buffer + index) = readport(target_address);
        portio_reset_control_pins(base_address, is_bidir);
    }

    PyObject *new_result = Py_BuildValue("y#", buffer, length);
    free(buffer);
    return new_result;
}

#endif /* _BASEPORT_H */
