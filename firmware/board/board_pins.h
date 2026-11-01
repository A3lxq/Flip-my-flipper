#ifndef BOARD_PINS_H
#define BOARD_PINS_H
#if defined(SYN_MCU_H743)
#include "pins_stm32h743iit6.h"
#elif defined(SYN_MCU_F429)
#include "pins_stm32f429zit6.h"
#else
#error "Define SYN_MCU_H743 or SYN_MCU_F429"
#endif
#endif
