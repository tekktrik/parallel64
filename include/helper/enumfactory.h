// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef ENUMFACTORY_H
#define ENUMFACTORY_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct {
    char *name;
    int64_t value;
} pyenum_t;

static inline PyObject* create_enum(char *enum_name, pyenum_t *enum_values, uint64_t num_values) {
    PyObject *enum_mod = PyImport_ImportModule("enum");
    PyObject *enum_class = PyObject_GetAttrString(enum_mod, "Enum");
    PyObject *class_name = PyUnicode_FromString(enum_name);
    PyObject *val_dict = PyDict_New();
    for (uint64_t index = 0; index < num_values; index++) {
        const char *name = enum_values[index].name;
        PyDict_SetItemString(
            val_dict,
            enum_values[index].name,
            PyLong_FromLongLong(enum_values[index].value)
        );
    }
    return PyObject_CallFunction(enum_class, "(NN)", class_name, val_dict);
}

#endif /* ENUMFACTORY_H */
