// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>
#include <stdbool.h>

#include "ports/portio.h"
#include "pyportio.h"
#include "StandardPort.h"

#if defined(_WIN32)
bool funcinit = false;
#endif


int pyportio_init_ports(const uint16_t *addresses, uint16_t num_ports) {

    init_result_t init_result = INIT_SUCCESS;

    #if !defined(_WIN32)

    int res = 0;
    for (uint16_t index = 0; index < num_ports; index++) {
        res = ioperm(addresses[index], 1, 1);
        if (res != 0) {
            // TODO: Depermission ports?
            init_result = INIT_PERMISSION_ERROR;
            break;
        }
    }

    #else
    if (!funcinit) {
        PyObject *mod = PyImport_AddModule("parallel64");
        PyObject *filestring = PyObject_GetAttrString(mod, "__file__");
        const char *constfilechars = PyUnicode_AsUTF8(filestring);
        Py_DECREF(filestring);
        char *filechars = malloc(strlen(constfilechars));
        strncpy(filechars, constfilechars, strlen(constfilechars) + 1);
        filechars[strlen(constfilechars) - 11] = '\0';
        char *dllpath = strcat(filechars, "ports");
        free(filechars);
        dllpath = strcat(dllpath, "\\inpoutx64");
        dllpath = strcat(dllpath, "\\inpoutx64");

        init_result = portio_load_dll(dllpath);
    }
    #endif

    switch (init_result) {
    case INIT_SUCCESS:
        #if defined(_WIN32)
        funcinit = true;
        #endif
        return 0;
    case INIT_DLLLOAD_ERROR:
        PyErr_SetString(
            PyExc_OSError,
            "Unable to load the DLL"
        );
    case INIT_PERMISSION_ERROR:
        PyErr_SetString(
            PyExc_OSError,
            "Unable gain permission for the port"
        );
    }

    return -1;

}


PyObject* pyportio_parse_write(uint16_t address, PyObject *args) {
    const uint8_t value;

    if (!PyArg_ParseTuple(args, "b", &value)) {
        return NULL;
    }

    writeport(address, value);
    Py_RETURN_NONE;
}

PyObject* pyportio_parse_read(uint16_t address) {
    return PyLong_FromLong(readport(address));
}


PyObject* pyportio_parse_multiwrite(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address) {
    Py_buffer data;

    if (!PyArg_ParseTuple(args, "y*", &data)) {
        return NULL;
    }

    const bool is_bidir = ISBIDIR(self);

    portio_reset_control_pins(base_address, is_bidir);
    portio_set_port_direction(base_address, PORT_DIR_FORWARD);

    for (Py_ssize_t index = 0; index < data.len; index++) {
        writeport(target_address, *((uint8_t *)data.buf + index));
    }

    Py_RETURN_NONE;
}


PyObject* pyportio_parse_multiread(PyObject *self, PyObject *args, uint16_t base_address, uint16_t target_address) {
    Py_ssize_t length;

    if (!PyArg_ParseTuple(args, "n", &length)) {
        return NULL;
    }

    const bool is_bidir = ISBIDIR(self);

    uint8_t *buffer = (uint8_t *)malloc(sizeof(uint8_t) * length);

    portio_reset_control_pins(base_address, is_bidir);
    portio_set_port_direction(base_address, PORT_DIR_REVERSE);

    for (Py_ssize_t index = 0; index < length; index++) {
        buffer[index] = readport(target_address);
    }

    PyObject *new_result = Py_BuildValue("y#", buffer, length);
    free(buffer);

    return new_result;
}
