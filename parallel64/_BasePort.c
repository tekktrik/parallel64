// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>


typedef struct {
    PyObject_HEAD
} _BasePortObject;


//static PyObject* _BasePort_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
//    return type->tp_alloc(type, 0);
//}


static void _BasePort_dealloc(_BasePortObject *self) {
    PyObject_GC_UnTrack(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyType_Slot _BasePortType_slots[] = {
    {Py_tp_doc, (void *)PyDoc_STR("Base class for all ports")},
    {Py_tp_dealloc, (destructor)_BasePort_dealloc},
    {Py_tp_getattro, PyObject_GenericGetAttr},
    {Py_tp_setattro, PyObject_GenericSetAttr},
    {Py_tp_alloc, PyType_GenericAlloc},
    {Py_tp_new, PyType_GenericNew},
};


PyType_Spec _BasePort_Spec = {
    .name = "parallel64._BasePort",
    .basicsize = sizeof(_BasePortObject),
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .slots = _BasePortType_slots,
};


bool parallel64__BasePort_setup(PyObject *module) {
    PyObject *type = PyType_FromModuleAndSpec(module, &_BasePort_Spec, NULL);
    return type != NULL;
}
