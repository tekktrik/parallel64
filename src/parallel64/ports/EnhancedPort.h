// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef ENHANCEDPORT_H
#define ENHANCEDPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "StandardPort.h"


#define P64_AS_STANDARD(OBJECT) ((StandardPortObject *)OBJECT)


typedef struct {
    StandardPortObject super;
} EnhancedPortObject;


extern PyTypeObject EnhancedPortType;


bool EnhancedPort_self_init(EnhancedPortObject *self, uint16_t spp_address, PyObject *is_bidir, bool reset_control);


#endif /* ENHANCEDPORT_H */
