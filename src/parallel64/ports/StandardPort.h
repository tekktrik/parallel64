// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef STANDARDPORT_H
#define STANDARDPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "_BasePort.h"

typedef struct {
    _BasePortObject super;
    uint16_t spp_address;
} StandardPortObject;

extern PyTypeObject StandardPortType;

#endif /* STANDARDPORT_H */
