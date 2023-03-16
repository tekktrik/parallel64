#ifndef _BASEPORT_H
#define _BASEPORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct {
    PyObject_HEAD
} _BasePortObject;

extern PyTypeObject _BasePortType;

#endif /* _BASEPORT_H */