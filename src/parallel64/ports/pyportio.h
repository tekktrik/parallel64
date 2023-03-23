// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

// TODO: Move later

#ifndef PYPORTIO_H
#define PYPORTIO_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>


int pyportio_init_ports(const uint16_t *addresses, uint16_t num_ports);
PyObject* pyportio_parse_multiwrite(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address);
PyObject* pyportio_parse_multiread(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address);


#endif /* PYPORTIO_H */
