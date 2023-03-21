// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef ENHANCEDPORT_H
#define ENHANCEDPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "StandardPort.h"

typedef struct {
    StandardPortObject super;
} EnhancedPortObject;

extern PyTypeObject EnhancedPortType;

#endif /* ENHANCEDPORT_H */
