// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef GPIO_H
#define GPIO_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "ports/portio.h"
#include "hardware/Pin.h"


#define GPIO_PORT(OBJECT) (((GPIOObject *)OBJECT)->port)


typedef struct pinobj PinObject;


typedef struct gpioobj {
    PyObject_HEAD

    PyObject *port;

    PinObject *strobe;
    PinObject *auto_linefeed;
    PinObject *initialize;
    PinObject *select_printer;

    PinObject *ack;
    PinObject *busy;
    PinObject *paper_out;
    PinObject *select_in;
    PinObject *error;

    PinObject *d0;
    PinObject *d1;
    PinObject *d2;
    PinObject *d3;
    PinObject *d4;
    PinObject *d5;
    PinObject *d6;
    PinObject *d7;

    PinObject **pinlist;
    bool pins_init;
} GPIOObject;


extern PyTypeObject GPIOType;


#endif /* GPIO_H */
