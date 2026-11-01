"""Assign Synnefo Handheld logical signals to MCU pins.

Reads a pin dump made by dumppins.py (position, name, type, signals...) and
searches for a conflict-free assignment. Every peripheral signal is checked
against ST's published signal list for that pin. Alternate-function (AF)
numbers are not in this data; take them from the datasheet or CubeMX.

usage: pinmap.py pins.txt {H743|F429} extra_gpio out.md
"""
import re
import sys

dump, mcu, extra, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]

pins = {}  # name -> (position, signals)
for line in open(dump):
    parts = line.split()
    pos, name, typ = parts[0], parts[1], parts[2]
    if typ == 'I/O':
        pins[name] = (int(pos), set(parts[3:]))

# ---- pins that must not be used for general signals -----------------------
reserved = {}
for n, (pos, sigs) in pins.items():
    for s in sigs:
        if 'SWDIO' in s or 'SWCLK' in s:
            reserved[n] = 'SWD'
        elif s.endswith('SWO'):
            reserved[n] = 'SWO (JTDO), kept free for trace'
        elif s in ('RCC_OSC_IN', 'RCC_OSC_OUT'):
            reserved[n] = 'HSE crystal'
        elif s in ('RCC_OSC32_IN', 'RCC_OSC32_OUT'):
            reserved[n] = 'LSE crystal'
avoid = {'PC13': 'RTC/tamper pin, weak drive'}
for n in list(pins):
    if n.endswith('_C'):
        avoid[n] = 'analog-switch pad, kept free'
if mcu == 'F429':
    avoid['PB2'] = 'BOOT1 strap'

SPI = ['SPI1', 'SPI2', 'SPI3', 'SPI4', 'SPI5', 'SPI6']
I2C = ['I2C1', 'I2C2', 'I2C3', 'I2C4']
UART = ['USART1', 'USART2', 'USART3', 'UART4', 'UART5', 'USART6', 'UART7', 'UART8']
SDI = ['SDMMC1', 'SDMMC2'] if mcu == 'H743' else ['SDIO']

# ---- requirements ----------------------------------------------------------
# task kinds: group(name, insts, roles) | sig(name, signal) | tim(name)
# | adc(name) | gpio(name, exti)
tasks = []


def group(name, insts, roles):
    tasks.append(('group', name, insts, roles))


def sig(name, s, exti=False):
    tasks.append(('sig', name, s, exti))


group('SD', SDI, ['D0', 'D1', 'D2', 'D3', 'CK', 'CMD'])
group('USB_FS', ['USB_OTG_FS'], ['DM', 'DP'])
group('LINUX_USB', ['USB_OTG_HS'], ['DM', 'DP'])
group('DISP_SPI', SPI, ['SCK', 'MOSI', 'MISO'])
group('EXP_SPI', SPI, ['SCK', 'MOSI', 'MISO'])
group('I2C_SYS', I2C, ['SCL', 'SDA'])
group('I2C_EXP', I2C, ['SCL', 'SDA'])
for u in ('UART_ESP', 'UART_CON', 'UART_EXP', 'UART_LINUX'):
    group(u, UART, ['TX', 'RX'])
sig('USB_VBUS', 'USB_OTG_FS_VBUS')
for n in ('IR_TX', 'IR_RX', 'BUZZER', 'DISP_BL'):
    tasks.append(('tim', n))
for i in range(1, 5):
    tasks.append(('adc', f'ADC_H{i}'))
exti = ['INT_B', 'PWR_INT', 'ESP_HS', 'SD_CD', 'LINUX_WAKE', 'LINUX_PRSNT'] + [f'IRQ_P{i}' for i in range(1, 9)]
for n in exti:
    tasks.append(('gpio', n, True))
plain = (['DISP_CS', 'DISP_DC', 'DISP_RST', 'ESP_EN', 'ESP_BOOT', 'LINUX_EN', 'LINUX_RST',
          'VIBRATION', 'LED_R', 'LED_G', 'LED_B', 'BOOST_EN', 'PWR_PG']
         + [f'IDD_P{i}' for i in range(1, 9)] + [f'IDC_P{i}' for i in range(1, 9)]
         + ['CS_P1', 'CS_P2', 'CS_P3', 'CS_P4', 'CS_P5']  # five SM-S ports
         + [f'GPIO_H{i}' for i in range(1, extra + 1)])
for n in plain:
    tasks.append(('gpio', n, False))


def pin_index(p):
    return int(re.sub(r'\D', '', p[2:]) or 0)


def candidates(t, state):
    kind = t[0]
    if kind == 'sig':
        return [(p, t[2], ()) for p, (_, s) in pins.items() if t[2] in s]
    if kind == 'tim':
        res = []
        for p, (_, s) in pins.items():
            for x in s:
                m = re.fullmatch(r'TIM(\d+)_CH(\d)', x)
                if m:
                    res.append((p, x, (('tim', m.group(1)),)))
        return res
    if kind == 'adc':
        return [(p, sorted(x for x in s if re.fullmatch(r'ADC\d_INP?\d+', x))[0], ())
                for p, (_, s) in pins.items() if any(re.fullmatch(r'ADC\d_INP?\d+', x) for x in s)]
    if kind == 'gpio':
        res = [(p, 'GPIO', (('exti', pin_index(p)),) if t[2] else ()) for p in pins]
        res.sort(key=lambda c: (len(pins[c[0]][1]), c[0]))
        return res
    raise ValueError(kind)


assign = {}  # pin -> (req, signal)
used_res = set()
nodes = 0
LIMIT = 3_000_000
chosen = {}


_cc = {}


def avail(t):
    k = t[:3] if t[0] != 'gpio' else ('gpio', t[2])
    if k not in _cc:
        _cc[k] = candidates(t, None)
    return [c for c in _cc[k]
            if c[0] not in assign and c[0] not in reserved and c[0] not in avoid
            and not any(r in used_res for r in c[2])]


def solve(queue):
    global nodes
    nodes += 1
    if nodes > LIMIT:
        raise RuntimeError('node limit')
    if not queue:
        return True
    groups = [t for t in queue if t[0] == 'group']
    if groups:
        g = groups[0]
        rest = [t for t in queue if t is not g]
        _, name, insts, roles = g
        for inst in insts:
            if ('inst', inst) in used_res:
                continue
            if not all(any(f'{inst}_{r}' in s for _, s in pins.values()) for r in roles):
                continue
            used_res.add(('inst', inst))
            chosen[name] = inst
            sub = [('sig', f'{name}_{r}', f'{inst}_{r}', False) for r in roles]
            if solve(rest + sub):
                return True
            used_res.discard(('inst', inst))
            chosen.pop(name, None)
        return False
    best, best_c = None, None
    for t in queue:
        c = avail(t)
        if not c:
            return False
        if best is None or len(c) < len(best_c):
            best, best_c = t, c
    rest = [t for t in queue if t is not best]
    for p, s, res in best_c:
        assign[p] = (best[1], s)
        used_res.update(res)
        if solve(rest):
            return True
        del assign[p]
        used_res.difference_update(res)
    return False


def order(t):
    if t[0] == 'group':
        return (0, len(t[2]))
    if t[0] == 'sig':
        return (1, 0)
    if t[0] == 'tim':
        return (2, 0)
    if t[0] == 'adc':
        return (3, 0)
    return (4, 0 if t[2] else 1)


tasks.sort(key=order)
ok = solve(tasks)
print(mcu, 'extra GPIO', extra, 'solved' if ok else 'FAILED', 'nodes', nodes)
if not ok:
    sys.exit(1)

free = sorted((p for p in pins if p not in assign and p not in reserved), key=lambda p: pins[p][0])
with open(out, 'w') as f:
    f.write(f'## {mcu}: {len(pins)} I/O pins, {len(assign)} assigned, {len(reserved)} reserved, {len(free)} spare\n\n')
    f.write('Instance choices: ' + ', '.join(f'{k}={v}' for k, v in sorted(chosen.items())) + '\n\n')
    f.write('| Pkg pin | Port | Function | Signal |\n|---|---|---|---|\n')
    for p in sorted(list(assign) + list(reserved), key=lambda p: pins[p][0]):
        if p in assign:
            f.write(f'| {pins[p][0]} | {p} | {assign[p][0]} | {assign[p][1]} |\n')
        else:
            f.write(f'| {pins[p][0]} | {p} | RESERVED | {reserved[p]} |\n')
    f.write('\nSpare I/O: ' + ', '.join(f'{p} ({pins[p][0]})' for p in free) + '\n')
    if avoid:
        f.write('\nDeliberately avoided: ' + ', '.join(f'{p} ({r})' for p, r in avoid.items()) + '\n')
