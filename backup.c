// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#if defined(_WIN32)
#include <windows.h>
typedef void (__stdcall *wport)(short, short);
typedef unsigned char (__stdcall *rport)(short);
wport writeport;
rport readport;
#elif defined(__linux__) || defined(BSD)
#include <sys/io.h>
#define writeport(PORT, VALUE) outb(VALUE, PORT)
#define readport(PORT) inb(PORT)
#endif

static PyObject* _parallel64_init_ports(PyObject *self, PyObject *args, PyObject *kwargs) {

    const unsigned long port_address;
    const unsigned long num_ports;

    static char *keywords[] = {"address", "num", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "kk", keywords, &port_address, &num_ports)) {
        return NULL;
    }

    int res = 0;
    #if defined(__linux__) || defined(BSD)
    res = ioperm(port_address, num_ports, 1);
    #else
    HINSTANCE dll = LoadLibrary("inpoutx64.dll");
    if (dll == NULL) {
        PyErr_SetString(
            PyExc_OSError,
            "Unable to load DLL"
        );
        return NULL;
    }
    writeport = (wport)GetProcAddress(dll, "DlPortWritePortUchar");
    readport = (rport)GetProcAddress(dll, "DlPortReadPortUchar");
    #endif
    if (res != 0) {
        PyErr_SetString(
            PyExc_OSError,
            "Insufficient permissions to operate port - please run as administrator"
        );
        return NULL;
    }
    Py_RETURN_NONE;

}

static PyObject* _parallel64_write(PyObject *self, PyObject *args, PyObject *kwargs) {

    const unsigned long port_address;
    const unsigned char value;

    static char *keywords[] = {"address", "value", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "kb", keywords, &port_address, &value)) {
        return NULL;
    }

    writeport(port_address, value);

    Py_RETURN_NONE;

}

static PyObject* _parallel64_read(PyObject *self, PyObject *args, PyObject *kwargs) {

    const unsigned long port_address;

    static char *keywords[] = {"address", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "k", keywords, &port_address)) {
        return NULL;
    }

    const unsigned char value = readport(port_address);

    return PyLong_FromLong(value);

}

static PyMethodDef _Parallel64Methods[] = {
    {"init_ports", _parallel64_init_ports, METH_VARARGS | METH_KEYWORDS, "Initialize the parallel port for the given addresses."},
    {"write", _parallel64_write, METH_VARARGS | METH_KEYWORDS, "Write a value to the specified port."},
    {"read", _parallel64_read, METH_VARARGS | METH_KEYWORDS, "Read a value from the specified port."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _parallel64module = {
    PyModuleDef_HEAD_INIT,
    "parallel64",
    "Behind the scenes extension for operating the parallel port",
    -1,
    _Parallel64Methods
};

PyMODINIT_FUNC PyInit__parallel64(void) {
    return PyModule_Create(&_parallel64module);
}
