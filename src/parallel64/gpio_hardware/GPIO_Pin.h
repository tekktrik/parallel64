// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef GPIO_PIN_H
#define GPIO_PIN_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "core/portio.h"


#define GPIO_PORT(OBJECT) (((GPIOObject *)OBJECT)->port)

#define PIN_REGISTER(OBJECT) (((PinObject *)OBJECT)->reg_addr)
#define PIN_BITINDEX(OBJECT) (((PinObject *)OBJECT)->bit_index)
#define PIN_INUSE(OBJECT) (((PinObject *)OBJECT)->bit_index)
#define PIN_DIRECTION(OBJECT) (((PinObject *)OBJECT)->direction)
#define PIN_HWINVERTED(OBJECT) (((PinObject *)OBJECT)->hw_inverted)
#define PIN_INPUTALLOWED(OBJECT) (((PinObject *)OBJECT)->input_allowed)
#define PIN_OUTPUTALLOWED(OBJECT) (((PinObject *)OBJECT)->output_allowed)

typedef struct gpioobj GPIOObject;
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
} GPIOObject;


extern PyTypeObject GPIOType;


typedef struct pinobj {
    PyObject_HEAD
    GPIOObject *gpio;
    uint16_t reg_addr;
    uint8_t bit_index;
    bool in_use;
    port_dir_t direction;
    bool hw_inverted;
    bool input_allowed;
    bool output_allowed;
} PinObject;


extern PyTypeObject PinType;


PinObject* create_Pin(
    GPIOObject *gpio,
    uint16_t reg_addr,
    uint8_t bit_index,
    port_dir_t direction,
    bool hw_inverted,
    bool input_allowed,
    bool output_allowed
);



#endif /* GPIO_PIN_H */
