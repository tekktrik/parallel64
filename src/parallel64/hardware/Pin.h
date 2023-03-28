// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef PIN_H
#define PIN_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "core/portio.h"
#include "gpio/GPIO.h"


#define PIN_REGISTER(OBJECT) (((PinObject *)OBJECT)->reg_addr)
#define PIN_BITINDEX(OBJECT) (((PinObject *)OBJECT)->bit_index)
#define PIN_INUSE(OBJECT) (((PinObject *)OBJECT)->bit_index)
#define PIN_DIRECTION(OBJECT) (((PinObject *)OBJECT)->direction)
#define PIN_HWINVERTED(OBJECT) (((PinObject *)OBJECT)->hw_inverted)
#define PIN_INPUTALLOWED(OBJECT) (((PinObject *)OBJECT)->input_allowed)
#define PIN_OUTPUTALLOWED(OBJECT) (((PinObject *)OBJECT)->output_allowed)

typedef struct gpioobj GPIOObject;


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
    drive_mode_t drive_mode;
    bool propagate_dir;
} PinObject;


extern PyTypeObject PinType;


PinObject* create_Pin(
    GPIOObject *gpio,
    uint16_t reg_addr,
    uint8_t bit_index,
    port_dir_t direction,
    bool hw_inverted,
    bool input_allowed,
    bool output_allowed,
    drive_mode_t drive_mode,
    bool propagate_dir
);



#endif /* PIN_H */
