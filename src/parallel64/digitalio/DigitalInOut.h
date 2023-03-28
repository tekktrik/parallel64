// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef DIGITALIO_H
#define DIGITALIO_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "hardware/Pin.h"


#define DIGINOUT_PIN(OBJECT) (((DigitalInOutObject *)OBJECT)->pin)


typedef struct dioobj {
    PyObject_HEAD
    PinObject *pin;
} DigitalInOutObject;


extern PyTypeObject DigitalInOutType;


#endif /* DIGITIALIO_H */
