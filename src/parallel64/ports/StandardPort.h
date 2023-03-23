// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef STANDARDPORT_H
#define STANDARDPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>


#define P64_AS_STANDARD(OBJECT) ((StandardPortObject *)OBJECT)

#define SPPADDRESS(OBJECT) (((StandardPortObject *)OBJECT)->spp_address)
#define ISBIDIR(OBJECT) (((StandardPortObject *)OBJECT)->is_bidir)


typedef struct {
    PyObject_HEAD
    uint16_t spp_address;
    bool is_bidir;
} StandardPortObject;


extern PyTypeObject StandardPortType;


bool StandardPort_self_init(StandardPortObject *self, uint16_t spp_address, PyObject *is_bidir, bool reset_control);


#endif /* STANDARDPORT_H */
