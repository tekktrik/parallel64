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

#endif /* _BASEPORT_H */
