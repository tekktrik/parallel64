// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef MODSETUP_H
#define MODSETUP_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define ADDNEWTYPE(NEW_TYPE, MODULE_OBJ) do \
{ \
    if (PyType_Ready(&NEW_TYPE##Type) < 0) { \
        return NULL; \
    } \
    Py_INCREF(&NEW_TYPE##Type); \
    PyModule_AddObject(MODULE_OBJ, #NEW_TYPE, (PyObject *)&NEW_TYPE##Type); \
} while (0)

#define IMPORTMOD(NAME) if (PyImport_ImportModule(NAME) == NULL) return NULL

#endif /* MODSETUP_H */
