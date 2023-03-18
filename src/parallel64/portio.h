// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef PORTIO_H
#define PORTIO_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <stdint.h>

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


typedef enum {
    INIT_SUCCESS,
    INIT_PERMISSION_ERROR,
    INIT_DLLLOAD_ERROR
} init_result_t;


static inline init_result_t parallel64_init_ports(uint16_t address, uint16_t num_ports) {

    int res = 0;
    #if !defined(_WIN32)
    res = ioperm(address, num_ports, 1);
    if (res != 0) {
        return INIT_PERMISSION_ERROR;
    }
    #else

    PyObject *mod = PyImport_ImportModule("parallel64");
    PyObject *filestring = PyObject_GetAttrString(mod, "__file__");
    char *filechars = PyUnicode_AsUTF8(filestring);
    filechars[strlen(filechars) - 11] = '\0';
    char *dllpath = strcat(filechars, "inpoutx64");
    Py_DECREF(mod);

    HINSTANCE dll = LoadLibrary(dllpath);
    if (dll == NULL) {
        return INIT_DLLLOAD_ERROR;
    }
    writeport = (wport)GetProcAddress(dll, "DlPortWritePortUchar");
    readport = (rport)GetProcAddress(dll, "DlPortReadPortUchar");
    #endif
    return INIT_SUCCESS;

}

static inline void _parallel64_write(uint16_t address, uint16_t value) {
    writeport(address, value);
}

static inline u_char _parallel64_read(uint16_t address) {
    return readport(address);
}

#endif /* PORTIO_H */
