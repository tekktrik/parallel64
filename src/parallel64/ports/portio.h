// SPDX-FileCopyrightText: 2023 Alec Delaney
//
// SPDX-License-Identifier: MIT

#ifndef PORTIO_H
#define PORTIO_H

#include <stdbool.h>
#include <stdint.h>
#include <time.h>

#if defined(__linux__) || defined(BSD)
#include <sys/io.h>
#define writeport(PORT, VALUE) outb(VALUE, PORT)
#define readport(PORT) inb(PORT)
#endif


#define SPP_DATA_ADDR(ADDRESS) (ADDRESS)
#define SPP_STATUS_ADDR(ADDRESS) (ADDRESS)+1
#define SPP_CONTROL_ADDR(ADDRESS) (ADDRESS)+2
#define EPP_ADDRESS_ADDR(ADDRESS) (ADDRESS)+3
#define EPP_DATA_ADDR(ADDRESS) (ADDRESS)+4
#define ECP_DATA_ADDR(ADDRESS) (ADDRESS)
#define ECP_CONFIG_ADDR(ADDRESS) (ADDRESS)+1
#define ECP_ECR_ADDR(ADDRESS) (ADDRESS)+2

#define P64_CHECKBITS_UINT8(VALUE, BITMASK, BITINDEX) ((BITMASK << BITINDEX) & VALUE)
#define P64_CHECKBIT_UINT8(VALUE, BITINDEX) P64_CHECKBITS_UINT8(VALUE, 1, BITINDEX)
#define P64_CHECKBITS_SHIFT(VALUE, BITMASK, BITINDEX) P64_CHECKBITS_UINT8(VALUE, BITMASK, BITINDEX) >> BITINDEX
#define P64_CHECKBIT_SHIFT(VALUE, BITINDEX) P64_CHECKBITS_UINT8(VALUE, 1, BITINDEX) >> BITINDEX
#define P64_SETBITS_OFF(VALUE, BITMASK, BITINDEX) ~(BITMASK << BITINDEX) & VALUE
#define P64_SETBITS_ON(VALUE, BITMASK, BITINDEX) (BITMASK << BITINDEX) | VALUE
#define P64_SETBITS(VALUE, BITMASK, BITINDEX, SETTING) SETTING ? P64_SETBITS_ON(VALUE, BITMASK, BITINDEX) : P64_SETBITS_OFF(VALUE, BITMASK, BITINDEX)
#define P64_SETBIT_OFF(VALUE, BITINDEX) P64_SETBITS_OFF(VALUE, 1, BITINDEX)
#define P64_SETBIT_ON(VALUE, BITINDEX) P64_SETBITS_ON(VALUE, 1, BITINDEX)
#define P64_SETBIT(VALUE, BITINDEX, SETTING) P64_SETBITS(VALUE, 1, BITINDEX, SETTING)

#define DIRECTION_BITINDEX 5

#define BUSY_BITINDEX 7

typedef enum {
    INIT_SUCCESS,
    INIT_PERMISSION_ERROR,
    INIT_DLLLOAD_ERROR
} init_result_t;

typedef enum {
    PORT_DIR_FORWARD = 0,
    PORT_DIR_REVERSE = 1
} port_dir_t;

typedef enum {
    PUSH_PULL = 0,
    OPEN_DRAIN = 1
} drive_mode_t;

typedef enum {
    PULL_UP = 0,
    PULL_DOWN = 1,
    PULL_NONE = 2
} pull_mode_t;


#if defined(_WIN32)
init_result_t portio_load_dll(const char *dllpath);
uint8_t readport(uint16_t port);
void writeport(uint16_t port, uint8_t value);
#endif


port_dir_t portio_get_port_direction(uint16_t spp_base_addr);
void portio_set_port_direction(uint16_t spp_base_addr, port_dir_t direction);
bool portio_test_bidirectionality(uint16_t spp_base_addr);
void portio_reset_control_pins(uint16_t spp_base_addr, bool is_bidir);
bool portio_delay_us(uint16_t delay_us);

#endif /* PORTIO_H */
