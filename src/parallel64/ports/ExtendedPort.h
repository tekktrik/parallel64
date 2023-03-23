// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef EXTENDEDPORT_H
#define EXTENDEDPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

#include "EnhancedPort.h"


#define P64_AS_EXTENDED(OBJECT) ((ExtendedPortObject *)OBJECT)

#define ECP_ADDRESS(OBJECT) (((ExtendedPortObject *)OBJECT)->ecp_address)

#define ECR_COMMMODE_BITINDEX 5


typedef struct {
    EnhancedPortObject super;
    uint16_t ecp_address;
} ExtendedPortObject;


extern PyTypeObject ExtendedPortType;


bool ExtendedPort_self_init(ExtendedPortObject *self, uint16_t spp_address, uint16_t ecp_address, PyObject *is_bidir, bool reset_control);


#endif /* EXTENDEDPORT_H */
