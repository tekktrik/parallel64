// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef PYPORTIO_H
#define PYPORTIO_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>


int pyportio_init_ports(const uint16_t *addresses, uint16_t num_ports);
PyObject* pyportio_parse_write(uint16_t address, PyObject *args);
PyObject* pyportio_parse_read(uint16_t address);
PyObject* pyportio_parse_multiwrite(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address);
PyObject* pyportio_parse_multiread(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address);


#endif /* PYPORTIO_H */
