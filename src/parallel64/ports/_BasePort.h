// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef _BASEPORT_H
#define _BASEPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>

#include "portio.h"


typedef struct {
    PyObject_HEAD
} _BasePortObject;


extern PyTypeObject _BasePortType;

#endif /* _BASEPORT_H */
