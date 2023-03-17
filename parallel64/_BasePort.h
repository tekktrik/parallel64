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


static inline PyObject* parallel64_parse_write(uint16_t address, PyObject *args) {
    const uint8_t value;

    if (!PyArg_ParseTuple(args, "b", &value)) {
        return NULL;
    }

    //parallel64_write(ADDRESS, value);
    writeport(address, value);
    Py_RETURN_NONE;
}

static inline PyObject* parallel64_parse_read(uint16_t address) {
    return PyLong_FromLong(readport(address));
}

#endif /* _BASEPORT_H */
