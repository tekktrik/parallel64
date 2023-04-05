// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#include <stdbool.h>
#include <stdint.h>
#include <time.h>

#include "portio.h"

#if defined(_WIN32)
#include <Windows.h>
typedef void (__stdcall *wport)(USHORT, UINT);
typedef UINT (__stdcall *rport)(USHORT);
wport writeport_cached;
rport readport_cached;
#elif defined(__linux__) || defined(BSD)
#include <sys/io.h>
#endif


#if defined(_WIN32)
static init_result_t portio_load_dll(const char *dllpath) {
    HINSTANCE dll = LoadLibraryA(dllpath);
    if (dll == NULL) {
        return INIT_DLLLOAD_ERROR;
    }
    writeport_cached = (wport)GetProcAddress(dll, "DlPortWritePortUchar");
    readport_cached = (rport)GetProcAddress(dll, "DlPortReadPortUchar");
    if (
        writeport == NULL ||
        readport == NULL
    ) {
        return INIT_DLLLOAD_ERROR;
    }
    return INIT_SUCCESS;
}


uint8_t readport(uint16_t port) {
    return readport_cached(port);
}

void writeport(uint16_t port, uint8_t value) {
    writeport_cached(port, value);
}
#endif


port_dir_t portio_get_port_direction(uint16_t spp_base_addr) {
    const int8_t control_byte = readport(SPP_CONTROL_ADDR(spp_base_addr));
    const uint8_t direction_byte = P64_CHECKBIT_SHIFT(control_byte, DIRECTION_BITINDEX);
    return (port_dir_t)direction_byte;
}

void portio_set_port_direction(uint16_t spp_base_addr, port_dir_t direction) {
    uint8_t current_control = readport(SPP_CONTROL_ADDR(spp_base_addr));
    uint8_t new_direction_byte = P64_SETBIT(current_control, DIRECTION_BITINDEX, direction);
    writeport(SPP_CONTROL_ADDR(spp_base_addr), new_direction_byte);
}

bool portio_test_bidirectionality(uint16_t spp_base_addr) {
    port_dir_t direction = portio_get_port_direction(spp_base_addr);
    portio_set_port_direction(spp_base_addr, PORT_DIR_REVERSE);
    bool is_bidir = portio_get_port_direction(spp_base_addr) == PORT_DIR_REVERSE;
    if (is_bidir && direction == PORT_DIR_FORWARD) portio_set_port_direction(spp_base_addr, PORT_DIR_FORWARD);
    return is_bidir;
}

void portio_reset_control_pins(uint16_t spp_base_addr, bool is_bidir) {
    uint8_t control_byte = readport(SPP_CONTROL_ADDR(spp_base_addr));
    uint8_t mask_control_byte = 0b11110000 & control_byte;
    uint8_t new_control_byte = P64_SETBIT_ON(mask_control_byte, 2);
    writeport(SPP_CONTROL_ADDR(spp_base_addr), new_control_byte);
}

bool portio_delay_us(uint16_t delay_us) {
    #if defined(_WIN32)
    // Windows code
    LARGE_INTEGER frequency, start_time, current_time;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start_time);
    LARGE_INTEGER ticks_needed;
    ticks_needed.QuadPart = delay_us * frequency.QuadPart;
    ticks_needed.QuadPart = delay_us / 1000000;
    while (true) {
        QueryPerformanceCounter(&current_time);
        if (current_time.QuadPart - start_time.QuadPart >= ticks_needed.QuadPart) break;
    }
    #elif defined(__linux__) || defined(BSD)
    // Linux
    struct timespec delay_set = {0, delay_us * 1000};
    struct timespec delay_remaining = {0, 0};
    if (nanosleep(&delay_set, &delay_remaining)) {
        return false;
    }
    #else
    // Other system
    uint16_t delay_ms = delay_us / 1000;
    clock_t start_time = clock();
    while (clock() < start_time + delay_ms);
    #endif
    return true;
}
