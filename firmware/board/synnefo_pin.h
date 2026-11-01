#ifndef SYNNEFO_PIN_H
#define SYNNEFO_PIN_H
/* A pin is (port letter, number). Use SYN_PIN_PORT / SYN_PIN_NUM to unpack. */
#define SYN_PIN(port, num) (((#port[0] - 'A') << 4) | (num))
#define SYN_PIN_PORT(p) ((p) >> 4)
#define SYN_PIN_NUM(p) ((p) & 0xF)
#endif
