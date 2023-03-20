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


#define SPP_DATA_ADDR(ADDRESS) (ADDRESS)+0
#define SPP_STATUS_ADDR(ADDRESS) (ADDRESS)+1
#define SPP_CONTROL_ADDR(ADDRESS) (ADDRESS)+2

#define P64_CHECKBITS_UINT8(VALUE, BITMASK, BITINDEX) ((BITMASK << BITINDEX) & VALUE)
#define P64_CHECKBIT_UINT8(VALUE, BITINDEX) P64_CHECKBITS_UINT8(VALUE, 1, BITINDEX)
#define P64_CHECKBITS_SHIFT(VALUE, BITMASK, BITINDEX) P64_CHECKBITS_UINT8(VALUE, BITMASK, BITINDEX) >> BITINDEX
#define P64_CHECKBIT_SHIFT(VALUE, BITINDEX) P64_CHECKBITS_UINT8(VALUE, 1, BITINDEX) >> BITINDEX
#define P64_SETBIT_OFF(VALUE, BITINDEX) ~(1 << BITINDEX) & VALUE
#define P64_SETBIT_ON(VALUE, BITINDEX) (1 << BITINDEX) | VALUE
#define P64_SETBIT(VALUE, BITINDEX, SETTING) SETTING ? P64_SETBIT_ON(VALUE, BITINDEX) : P64_SETBIT_OFF(VALUE, BITINDEX)

#define DIRECTION_BITINDEX 5

typedef enum {
    INIT_SUCCESS,
    INIT_PERMISSION_ERROR,
    INIT_DLLLOAD_ERROR
} init_result_t;

typedef enum {
    PORT_DIR_FORWARD = 0,
    PORT_DIR_REVERSE = 1
} port_dir_t;


static inline init_result_t portio_init_ports(uint16_t address, uint16_t num_ports) {

    int res = 0;
    #if !defined(_WIN32)
    res = ioperm(address, num_ports, 1);
    if (res != 0) {
        return INIT_PERMISSION_ERROR;
    }
    #else

    PyObject *mod = PyImport_AddModule("parallel64");
    PyObject *filestring = PyObject_GetAttrString(mod, "__file__");
    const char *constfilechars = PyUnicode_AsUTF8(filestring);
    Py_DECREF(filestring);
    char *filechars = malloc(strlen(constfilechars));
    strncpy(filechars, constfilechars, strlen(constfilechars) + 1);
    filechars[strlen(constfilechars) - 11] = '\0';
    char *dllpath = strcat(filechars, "\\ports");
    free(filechars);
    dllpath = strcat(dllpath, "\\inpoutx64");
    dllpath = strcat(dllpath, "\\inpoutx64");

    HINSTANCE dll = LoadLibrary(dllpath);
    if (dll == NULL) {
        return INIT_DLLLOAD_ERROR;
    }
    writeport = (wport)GetProcAddress(dll, "DlPortWritePortUchar");
    readport = (rport)GetProcAddress(dll, "DlPortReadPortUchar");
    #endif
    return INIT_SUCCESS;

}

static inline PyObject* portio_parse_write(uint16_t address, PyObject *args) {
    const uint8_t value;

    if (!PyArg_ParseTuple(args, "b", &value)) {
        return NULL;
    }

    writeport(address, value);
    Py_RETURN_NONE;
}

static inline PyObject* portio_parse_read(uint16_t address) {
    return PyLong_FromLong(readport(address));
}

static inline const port_dir_t portio_get_port_direction(uint16_t spp_base_addr) {
    const int8_t control_byte = readport(SPP_CONTROL_ADDR(spp_base_addr));
    const uint8_t direction_byte = P64_CHECKBIT_SHIFT(control_byte, DIRECTION_BITINDEX);
    return (port_dir_t)direction_byte;
}

static inline void portio_set_port_direction(uint16_t spp_base_addr, port_dir_t direction) {
    uint8_t new_direction_byte = P64_SETBIT(direction, DIRECTION_BITINDEX, direction);
    writeport(SPP_CONTROL_ADDR(spp_base_addr), new_direction_byte);
}

static inline bool portio_test_bidirectionality(uint16_t spp_base_addr) {
    port_dir_t direction = portio_get_port_direction(spp_base_addr);
    portio_set_port_direction(spp_base_addr, PORT_DIR_REVERSE);
    bool is_bidir = portio_get_port_direction(spp_base_addr) == PORT_DIR_REVERSE;
    if (is_bidir && direction == PORT_DIR_FORWARD) portio_set_port_direction(spp_base_addr, PORT_DIR_FORWARD);
    return is_bidir;
}

static inline void portio_reset_control_pins(uint16_t spp_base_addr, bool is_bidir) {
    uint8_t control_byte = readport(SPP_CONTROL_ADDR(spp_base_addr));
    uint8_t bidir_control_byte = P64_SETBIT(0b11110000, DIRECTION_BITINDEX, is_bidir);
    uint8_t pre_control_byte = bidir_control_byte | control_byte;
    uint8_t new_control_byte = (1 << 2) | pre_control_byte;
    writeport(SPP_CONTROL_ADDR(spp_base_addr), new_control_byte);
}

#endif /* PORTIO_H */
