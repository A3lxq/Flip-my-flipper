#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate the module pinout tables and the connection diagrams.

MCU pins are read from tools/out_F429.md and tools/out_H743.md (the solved, verified pin maps), so no MCU pin is
typed by hand. Module-side pin knowledge is written here with a status tag:
  P = read by a research agent from a manufacturer datasheet/user manual
  V = vendor page or guide, secondary
  K = my recollection of the standard pinout, NOT checked in this project (verify)
  ? = not known

usage: gen_pinouts.py <repo root>      (needs matplotlib)
"""
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = sys.argv[1]
OUT = f"{ROOT}/hardware/pinouts"


def load(chip):
    pins, reserved = {}, []
    for line in open(f"{ROOT}/tools/out_{chip}.md"):
        m = re.match(r"\| (\d+) \| (\S+) \| (\S+) \| (.+) \|$", line)
        if not m or m.group(3) == "Function":
            continue
        pos, port, fn, sig = m.groups()
        if fn == "RESERVED":
            reserved.append((port, sig))
        else:
            pins[fn] = port
    return pins, reserved


F, FRES = load("F429")
H, HRES = load("H743")


def pin(chip_map, name):
    return chip_map.get(name, "n/a")


# ------------------------------------------------------------------ block data for the system diagram
# each row: (label, key) where key is a pin-map name (or None for a note)
LEFT = [
    ("3.5in display, ST7796S", "SPI1 + 3 GPIO + PWM", [
        ("SCK", "DISP_SPI_SCK"), ("MOSI", "DISP_SPI_MOSI"), ("MISO", "DISP_SPI_MISO"), ("CS", "DISP_CS"),
        ("DC", "DISP_DC"), ("RESET", "DISP_RST"), ("BL (PWM)", "DISP_BL")]),
    ("microSD socket", "SDIO / SDMMC 4-bit", [
        ("CLK", "SD_CK"), ("CMD", "SD_CMD"), ("D0", "SD_D0"), ("D1", "SD_D1"), ("D2", "SD_D2"), ("D3", "SD_D3"),
        ("Card detect", "SD_CD")]),
    ("ESP32-S3-WROOM-1", "UART1 + 3 GPIO", [
        ("MCU TX>ESP RX", "UART_ESP_TX"), ("ESP TX>MCU RX", "UART_ESP_RX"), ("EN", "ESP_EN"),
        ("IO0 (boot)", "ESP_BOOT"), ("Handshake", "ESP_HS")]),
    ("USB-C receptacle (OTG FS)", "USB FS", [
        ("D-  (DM)", "USB_FS_DM"), ("D+  (DP)", "USB_FS_DP"), ("VBUS sense", "USB_VBUS"),
        ("CC1 / CC2 ADC", None)]),
    ("Linux link (reserved, unpopulated)", "UART4 + USB HS(FS) + 4 GPIO", [
        ("UART TX", "UART_LINUX_TX"), ("UART RX", "UART_LINUX_RX"), ("USB DM", "LINUX_USB_DM"),
        ("USB DP", "LINUX_USB_DP"), ("Power enable", "LINUX_EN"), ("Reset", "LINUX_RST"),
        ("Present", "LINUX_PRSNT"), ("Wake", "LINUX_WAKE")]),
    ("Console UART (USART2)", "serial console", [("TX", "UART_CON_TX"), ("RX", "UART_CON_RX")]),
]
RIGHT_TOP = [
    ("Shared expansion buses (to ports)", "SPI2 + I2C2 + USART3", [
        ("SPI SCK", "EXP_SPI_SCK"), ("SPI MOSI", "EXP_SPI_MOSI"), ("SPI MISO", "EXP_SPI_MISO"),
        ("I2C SCL", "I2C_EXP_SCL"), ("I2C SDA", "I2C_EXP_SDA"), ("UART TX", "UART_EXP_TX"),
        ("UART RX", "UART_EXP_RX")]),
]
RIGHT_BOTTOM = [
    ("System I2C (I2C1)", "SCL/SDA", [
        ("SCL", "I2C_SYS_SCL"), ("SDA", "I2C_SYS_SDA"),
        ("on bus", "MAX17048 0x36"), ("on bus", "PCA9535 A, B 0x20.."), ("on bus", "INA219 x8 0x40..0x47")]),
    ("Power control", "GPIO / EXTI", [
        ("Power INT (EXTI)", "PWR_INT"), ("5V boost enable", "BOOST_EN"), ("Power good", "PWR_PG"),
        ("Expander B INT", "INT_B"), ("BQ24075 EN2/CE/SYSOFF", None)]),
    ("IR, buzzer, vibration, LEDs", "timers / GPIO", [
        ("IR TX (PWM)", "IR_TX"), ("IR RX (capture)", "IR_RX"), ("Buzzer (PWM)", "BUZZER"),
        ("Vibration", "VIBRATION"), ("LED R", "LED_R"), ("LED G", "LED_G"), ("LED B", "LED_B")]),
]
PORTS = [  # (port, class, proposed module)
    ("P1", "SM-S", "CC1101 sub-GHz"), ("P2", "SM-S", "NFC (PN532 or ST25R3916)"), ("P3", "SM-S", "NFC / spare"),
    ("P4", "SM-S", "internal, spare"), ("P5", "SM-S", "internal, spare"), ("P6", "SM-I", "internal I2C module"),
    ("P7", "SM-I", "side I2C module"), ("P8", "SM-U", "RDM6300 125 kHz")]


def port_pins(chip_map, n):
    s = f"IDD {pin(chip_map, f'IDD_P{n}')} IDC {pin(chip_map, f'IDC_P{n}')} IRQ {pin(chip_map, f'IRQ_P{n}')}"
    if n <= 5:
        s += f" CS {pin(chip_map, f'CS_P{n}')}"
    return s


# ------------------------------------------------------------------ drawing helpers
MONO = {"family": "DejaVu Sans Mono"}
HDR = "#1f3a5f"
COLORS = {"left": "#e8f0fb", "right": "#eaf6ea", "port": "#fff4dc", "gap": "#fde2e2"}


def block(ax, x, y_top, w, title, subtitle, rows, color, ncol=True, row_h=0.27):
    """Draw a block; returns (center_y, height). rows: (label, key|None)."""
    hdr_h = 0.62
    h = hdr_h + row_h * len(rows) + 0.1
    ax.add_patch(Rectangle((x, y_top - h), w, h, fc=color, ec=HDR, lw=1.4, zorder=2))
    ax.add_patch(Rectangle((x, y_top - hdr_h), w, hdr_h, fc=HDR, ec=HDR, zorder=3))
    ax.text(x + 0.12, y_top - 0.2, title, color="white", fontsize=9.5, fontweight="bold", va="center", zorder=4)
    ax.text(x + 0.12, y_top - 0.46, subtitle, color="#cfe0f7", fontsize=7.5, va="center", zorder=4, style="italic")
    if ncol:
        ax.text(x + w - 1.78, y_top - 0.2, "F429", color="#9ad", fontsize=7.5, fontweight="bold", va="center", zorder=4, **MONO)
        ax.text(x + w - 0.95, y_top - 0.2, "H743", color="#9ad", fontsize=7.5, fontweight="bold", va="center", zorder=4, **MONO)
    for i, (label, key) in enumerate(rows):
        yy = y_top - hdr_h - row_h * (i + 0.6)
        if key is None:
            ax.text(x + 0.12, yy, f"{label}", fontsize=7.8, va="center", zorder=4, color="#a40000", **MONO)
            ax.text(x + w - 1.78, yy, "not in pin map", fontsize=6.8, va="center", zorder=4, color="#a40000", **MONO)
            continue
        ax.text(x + 0.12, yy, label, fontsize=7.8, va="center", zorder=4, **MONO)
        if key in F or key in H:
            ax.text(x + w - 1.78, yy, pin(F, key), fontsize=7.8, va="center", zorder=4, **MONO)
            ax.text(x + w - 0.95, yy, pin(H, key), fontsize=7.8, va="center", zorder=4, **MONO)
        else:
            ax.text(x + w - 1.78, yy, key, fontsize=7.3, va="center", zorder=4, color="#444", **MONO)
    return y_top - h / 2, h


def system_diagram():
    fig, ax = plt.subplots(figsize=(21, 19.5), dpi=100)
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 19.5)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.text(10.5, 19.15, "Synnefo Handheld: how each module connects to the MCU core (pin-map draft 2, 97 pins assigned)",
            ha="center", fontsize=14, fontweight="bold")
    ax.text(10.5, 18.8, "Pins are read from tools/out_F429.md and out_H743.md. Port numbering/assignment is a PROPOSAL. "
            "Red rows are signals not yet in the pin map.", ha="center", fontsize=9, color="#444")
    lw_, mx_, mw_, rx_, rw_ = 5.5, 7.1, 3.4, 11.9, 8.4
    ax.add_patch(Rectangle((lw_ + 1.0, 0.5), 0.0, 0.0, fc="none"))
    # left column
    y = 18.3
    anchors = []
    for title, sub, rows in LEFT:
        cy, h = block(ax, 0.3, y, lw_, title, sub, rows, COLORS["gap"] if any(r[1] is None for r in rows) else COLORS["left"])
        anchors.append(("L", cy, sub))
        y -= h + 0.32
    left_bottom = y
    # right column: shared buses
    y = 18.3
    for title, sub, rows in RIGHT_TOP:
        cy, h = block(ax, rx_, y, rw_, title, sub, rows, COLORS["right"])
        anchors.append(("R", cy, sub))
        y -= h + 0.32
    # ports block
    row_h = 0.27
    hdr = 0.62
    n_rows = len(PORTS) * 2
    h = hdr + row_h * n_rows + 0.1
    ax.add_patch(Rectangle((rx_, y - h), rw_, h, fc=COLORS["port"], ec=HDR, lw=1.4, zorder=2))
    ax.add_patch(Rectangle((rx_, y - hdr), rw_, hdr, fc=HDR, ec=HDR, zorder=3))
    ax.text(rx_ + 0.12, y - 0.2, "Module ports P1-P8 (SMIS v0.2, 10-contact each)", color="white", fontsize=9.5, fontweight="bold", va="center", zorder=4)
    ax.text(rx_ + 0.12, y - 0.46, "per-port: ID data, ID clock, IRQ, chip select (SM-S only)", color="#cfe0f7", fontsize=7.5, va="center", style="italic", zorder=4)
    for i, (p, cls, mod) in enumerate(PORTS):
        n = i + 1
        y0 = y - hdr - row_h * (2 * i + 0.6)
        ax.text(rx_ + 0.12, y0, f"{p} {cls} {mod}", fontsize=7.6, va="center", fontweight="bold", zorder=4, **MONO)
        ax.text(rx_ + 0.12, y0 - row_h, f"   F429 {port_pins(F, n)}", fontsize=7.0, va="center", zorder=4, **MONO)
        # H743 pins on the right half of the second row would be too long: print on the same row with offset
        ax.text(rx_ + 4.55, y0 - row_h, f"H743 {port_pins(H, n)}", fontsize=7.0, va="center", zorder=4, **MONO)
    anchors.append(("R", y - h / 2, "ports"))
    y -= h + 0.32
    for title, sub, rows in RIGHT_BOTTOM:
        cy, h2 = block(ax, rx_, y, rw_, title, sub, rows, COLORS["gap"] if any(r[1] is None for r in rows) else COLORS["right"])
        anchors.append(("R", cy, sub))
        y -= h2 + 0.32
    # GPIO header summary
    ax.add_patch(Rectangle((rx_, y - 1.0), rw_, 1.0, fc=COLORS["right"], ec=HDR, lw=1.4, zorder=2))
    ax.text(rx_ + 0.12, y - 0.25, "GPIO headers (2 x 2x10, 2.54 mm)", fontsize=9.5, fontweight="bold", va="center", zorder=4)
    gp = ", ".join(f"H{i}" for i in range(1, 13))
    ax.text(rx_ + 0.12, y - 0.55, f"12 GPIO (GPIO_H1..H12) + 4 ADC (ADC_H1..H4) + shared SPI/I2C/UART", fontsize=7.6, va="center", zorder=4, **MONO)
    ax.text(rx_ + 0.12, y - 0.8, "pins: see module-pinouts.md", fontsize=7.6, va="center", zorder=4, **MONO)
    anchors.append(("R", y - 0.5, "headers"))
    right_bottom = y - 1.0
    # MCU box
    top, bot = 18.3, min(left_bottom, right_bottom) + 0.2
    ax.add_patch(Rectangle((mx_, bot), mw_, top - bot, fc="#fff0b8", ec="#7a5b00", lw=2.2, zorder=2))
    ax.text(mx_ + mw_ / 2, top - 0.5, "MCU CORE", ha="center", fontsize=14, fontweight="bold", zorder=4)
    ax.text(mx_ + mw_ / 2, top - 0.95, "STM32F429ZIT6 (LQFP144)\nSTM32H743IIT6 (LQFP176)", ha="center", fontsize=9.5, zorder=4)
    ax.text(mx_ + mw_ / 2, top - 1.7, "one connector, same logical\nsignals; chip-specific\nrouting on each core module\n(03-core-module.md)", ha="center", fontsize=8.2, zorder=4, color="#444")
    # reserved pins list inside MCU box
    yy = top - 3.2
    ax.text(mx_ + 0.15, yy, "Reserved (kept free of signals):", fontsize=8, fontweight="bold", zorder=4)
    for port, sig in FRES:
        yy -= 0.26
        ax.text(mx_ + 0.15, yy, f"{port:<14s} {sig[:22]}", fontsize=7.4, zorder=4, **MONO)
    yy -= 0.8
    ax.text(mx_ + 0.15, yy, "Not drawn: crystals, USB CC\nresistors, decoupling, boot/reset\nnetworks (core module)", fontsize=7.4, zorder=4, color="#444")
    # connection lines
    SHORT = {"SPI1 + 3 GPIO + PWM": "SPI1", "SDIO / SDMMC 4-bit": "SDIO", "UART1 + 3 GPIO": "UART1",
             "USB FS": "USB FS", "UART4 + USB HS(FS) + 4 GPIO": "UART4 / USB", "serial console": "USART2",
             "SPI2 + I2C2 + USART3": "SPI2 I2C2 USART3", "ports": "8 ports", "SCL/SDA": "I2C1",
             "GPIO / EXTI": "GPIO", "timers / GPIO": "timers", "headers": "GPIO"}
    for side, cy, label in anchors:
        label = SHORT.get(label, label)
        if side == "L":
            ax.plot([0.3 + lw_, mx_], [cy, cy], color="#2a5bd7", lw=1.8, zorder=1)
            ax.plot([mx_], [cy], "o", color="#2a5bd7", zorder=1)
            ax.text((0.3 + lw_ + mx_) / 2, cy + 0.08, label, ha="center", fontsize=7.2, color="#2a5bd7", zorder=4)
        else:
            ax.plot([mx_ + mw_, rx_], [cy, cy], color="#1b8a1b", lw=1.8, zorder=1)
            ax.plot([mx_ + mw_], [cy], "o", color="#1b8a1b", zorder=1)
            ax.text((mx_ + mw_ + rx_) / 2, cy + 0.08, label, ha="center", fontsize=7.2, color="#1b8a1b", zorder=4)
    ax.text(0.3, 0.25, "Module-side pins (what is connected to what on each module) are in sm-s-port-matrix.png and module-pinouts.md. "
            "BQ24075 EN2/CE/SYSOFF are planned for a spare PCA9535 B bit; USB CC1/CC2 need two ADC pins.",
            fontsize=7.8, color="#444")
    fig.savefig(f"{OUT}/system-connections.png", bbox_inches="tight")
    fig.savefig(f"{OUT}/system-connections.svg", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ SM-S / SM-U / SM-I matrix diagram
SMS_NETS = ["GND", "3V3_P", "5V_P", "SCK", "MOSI", "MISO", "CS", "IRQ", "IDC", "IDD"]
SMS_MCU = {  # contact -> function name in the pin map (P1 shown)
    "SCK": "EXP_SPI_SCK", "MOSI": "EXP_SPI_MOSI", "MISO": "EXP_SPI_MISO", "CS": "CS_P1", "IRQ": "IRQ_P1",
    "IDC": "IDC_P1", "IDD": "IDD_P1"}
# module-side pin names per SM-S contact; tag in [] = knowledge level
MOD_SMS = {
    "CC1101 module (chip pins)": ["GND 16,19 [K]", "VDD 4,9.. [K]", "n/c", "SCLK 1 [K]", "SI 20 [K]", "SO/GDO1 2 [K]",
                                    "CSn 7 [K]", "GDO0 6 [P]", "ID EEPROM SCL", "ID EEPROM SDA"],
    "PN532 V3 breakout (signals)": ["GND", "VCC (JP1 1-2)", "JP1 3 (unused)", "SCK", "MOSI", "MISO",
                                      "SSEL", "IRQ (low)", "ID EEPROM SCL", "ID EEPROM SDA"],
    "ST25R3916 module (chip pins)": ["GND/EP 33 [P]", "VDD_IO 1 [P]", "VDD 8, VDD_TX 10 [P]", "SCLK ? ", "MOSI ?",
                                       "MISO ?", "BSS ?", "IRQ ? (high)", "ID EEPROM SCL", "ID EEPROM SDA"],
}
MOD_NOTE = {
    "CC1101 module (chip pins)": "GDO2 (pin 3 [P]) has no contact; vendor breakout headers differ (8 and 10 pin boards)",
    "PN532 V3 breakout (signals)": "header ORDER unverified [V]; RSTPDN pulled up on the adapter; chip pins [P]: NSS 27, MOSI 28, MISO 29, SCK 30, IRQ 25, RSTPD_N 38",
    "ST25R3916 module (chip pins)": "I2C_EN tied to GND; no reset pin; other pin numbers unknown until DS12484 Table 2 is read",
}


def matrix_diagram():
    fig, ax = plt.subplots(figsize=(24, 17), dpi=100)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 17)
    ax.axis("off")
    ax.text(12, 16.65, "SM-S port: contact-by-contact connection of the SPI modules (port P1 shown)", ha="center", fontsize=15, fontweight="bold")
    ax.text(12, 16.3, "Left: MCU pins (F429 | H743). Centre: SMIS v0.2 contacts (2x5 header, IDC numbering). Right: module pins. "
            "Tags: [P] datasheet read, [V] vendor guide, [K] my recollection, unverified, ? unknown.", ha="center", fontsize=9, color="#444")
    row_h = 0.62
    top = 15.2
    cols = {"mcu": 0.4, "net": 5.2, "contact": 7.5}
    mod_x = [10.0, 14.6, 19.2]
    mod_w = 4.3
    ax.text(cols["mcu"], top + 0.55, "MCU pin  F429 | H743", fontsize=9.5, fontweight="bold")
    ax.text(cols["net"], top + 0.55, "SMIS net", fontsize=9.5, fontweight="bold")
    ax.text(cols["contact"], top + 0.55, "Contact", fontsize=9.5, fontweight="bold")
    ax.plot([cols["contact"] + 1.5, mod_x[-1] - 0.1], [top + 0.25, top + 0.25], color="#2a5bd7", lw=1.0, ls="--")
    ax.text(mod_x[0], top + 0.78, "each column is an ALTERNATIVE module on the same port (not in series)", fontsize=8.4, color="#2a5bd7")
    for (name, pins_), x in zip(MOD_SMS.items(), mod_x):
        ax.add_patch(Rectangle((x - 0.1, top - row_h * 10 - 0.15), mod_w, row_h * 10 + 0.85, fc="#f4f8ff", ec=HDR, lw=1.2, zorder=1))
        ax.text(x, top + 0.55, name, fontsize=9.5, fontweight="bold", color=HDR)
    for i, net in enumerate(SMS_NETS):
        y = top - row_h * (i + 0.5)
        # MCU side
        if net in SMS_MCU:
            key = SMS_MCU[net]
            txt = f"{pin(F, key):>5} | {pin(H, key):<5}  {key}"
        elif net in ("3V3_P", "5V_P"):
            txt = "via port switch (PCA9535 A)"
        else:
            txt = "ground"
        ax.text(cols["mcu"], y, txt, fontsize=8.6, va="center", **MONO)
        ax.text(cols["net"], y, net, fontsize=9.5, va="center", fontweight="bold", **MONO)
        # contact box (IDC numbering: contact n is odd/even column, row (n-1)//2) - shown as a numbered chip
        ax.add_patch(Rectangle((cols["contact"], y - 0.22), 1.5, 0.44, fc="#fff0b8", ec="#7a5b00", lw=1.2, zorder=3))
        ax.text(cols["contact"] + 0.75, y, f"{i + 1}", ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
        ax.plot([cols["net"] + 1.6, cols["contact"]], [y, y], color="#7a5b00", lw=1.4, zorder=2)
        ax.plot([cols["mcu"] + 4.7, cols["net"] - 0.1], [y, y], color="#999", lw=0.8, ls=":", zorder=1)
        for (name, pins_), x in zip(MOD_SMS.items(), mod_x):
            txt = pins_[i]
            unver = "?" in txt or "[K]" in txt
            ax.plot([x - 0.1, x + 0.0], [y, y], color="#2a5bd7" if "n/c" not in txt else "#bbb", lw=1.6, zorder=2)
            ax.plot([x - 0.1], [y], "o", ms=3, color="#2a5bd7" if "n/c" not in txt else "#bbb", zorder=2)
            ax.text(x + 0.05, y, txt, fontsize=8.2, va="center", zorder=4, style="italic" if unver else "normal",
                    color="#7a3b00" if unver else "black", **MONO)
    ybot = top - row_h * 10 - 0.3
    for (name, note), x in zip(MOD_NOTE.items(), mod_x):
        wrap = []
        words, line = note.split(), ""
        for wd in words:
            if len(line) + len(wd) > 44:
                wrap.append(line)
                line = ""
            line += wd + " "
        wrap.append(line)
        for k, ln in enumerate(wrap):
            ax.text(x, ybot - 0.3 - 0.3 * k, ln, fontsize=7.8, color="#444")
    # SM-U and SM-I panels
    py = 6.9
    ax.text(0.4, py, "SM-U port (P8, UART) with RDM6300 125 kHz reader", fontsize=11.5, fontweight="bold")
    ax.text(0.4, py - 0.35, "contacts 4-8 change meaning per class; 1, 2, 3, 9, 10 never change", fontsize=8.6, color="#444")
    SMU = ["GND", "3V3_P", "5V_P", "TX (module out)", "RX (module in)", "IRQ", "GPIO", "n/c", "IDC", "IDD"]
    SMU_MCU = {"TX (module out)": "UART_EXP_RX", "RX (module in)": "UART_EXP_TX", "IRQ": "IRQ_P8", "IDC": "IDC_P8", "IDD": "IDD_P8"}
    RDM = ["GND", "(not used)", "5V supply", "TX (UART out, level unverified) [V]", "(RX, if present) ?", "-", "-", "-", "ID EEPROM SCL", "ID EEPROM SDA"]
    rh = 0.4
    top2 = py - 1.0
    for i, net in enumerate(SMU):
        y = top2 - rh * i
        if net in SMU_MCU:
            key = SMU_MCU[net]
            txt = f"{pin(F, key):>5} | {pin(H, key):<5}  {key}"
        elif net in ("3V3_P", "5V_P"):
            txt = "via port switch"
        else:
            txt = "ground" if net == "GND" else "-"
        ax.text(0.4, y, txt, fontsize=8, va="center", **MONO)
        ax.text(5.2, y, net, fontsize=8.8, va="center", fontweight="bold", **MONO)
        ax.add_patch(Rectangle((8.0, y - 0.16), 1.0, 0.32, fc="#fff0b8", ec="#7a5b00", zorder=3))
        ax.text(8.5, y, str(i + 1), ha="center", va="center", fontsize=8.8, fontweight="bold", zorder=4)
        ax.plot([7.2, 8.0], [y, y], color="#7a5b00", lw=1.2)
        ax.plot([9.0, 10.0], [y, y], color="#2a5bd7", lw=1.1)
        ax.text(10.1, y, RDM[i], fontsize=8, va="center", style="italic" if "?" in RDM[i] or "[V]" in RDM[i] else "normal", **MONO)
    ax.text(10.0, top2 + 0.45, "RDM6300 (vendor header, order unverified)", fontsize=9, fontweight="bold", color=HDR)
    # SM-I panel
    ax.text(14.2, py, "SM-I port (P6, P7, I2C): generic sensor/module", fontsize=11.5, fontweight="bold")
    ax.text(14.2, py - 0.35, "I2C bus is shared by both SM-I ports (I2C2)", fontsize=8.6, color="#444")
    SMI = ["GND", "3V3_P", "5V_P", "SDA", "SCL", "IRQ", "GPIO (opt)", "n/c", "IDC", "IDD"]
    SMI_MCU = {"SDA": "I2C_EXP_SDA", "SCL": "I2C_EXP_SCL", "IRQ": "IRQ_P6", "IDC": "IDC_P6", "IDD": "IDD_P6"}
    for i, net in enumerate(SMI):
        y = top2 - rh * i
        if net in SMI_MCU:
            key = SMI_MCU[net]
            txt = f"{pin(F, key):>5} | {pin(H, key):<5} {key}"
        elif net in ("3V3_P", "5V_P"):
            txt = "via port switch"
        else:
            txt = "ground" if net == "GND" else "-"
        ax.text(14.2, y, txt, fontsize=8, va="center", **MONO)
        ax.add_patch(Rectangle((19.4, y - 0.16), 1.0, 0.32, fc="#fff0b8", ec="#7a5b00", zorder=3))
        ax.text(19.9, y, str(i + 1), ha="center", va="center", fontsize=8.8, fontweight="bold", zorder=4)
        ax.text(20.6, y, net, fontsize=8.8, va="center", fontweight="bold", **MONO)
    ax.text(14.2, 1.4, "P7 uses IRQ_P7 / IDC_P7 / IDD_P7 (see module-pinouts.md).", fontsize=8.2, color="#444")
    ax.text(0.4, 0.75, "Power for each port: 3V3_P and 5V_P are separate P-FET switches enabled from PCA9535 A (not MCU pins). "
            "During ID only 3V3_P is on (SMIS v0.2 section 6).", fontsize=8.6, color="#444")
    ax.text(0.4, 0.4, "Contact numbering follows a 2x5 header: odd contacts on one row (1,3,5,7,9), even on the other (2,4,6,8,10).",
            fontsize=8.6, color="#444")
    fig.savefig(f"{OUT}/sm-s-port-matrix.png", bbox_inches="tight")
    fig.savefig(f"{OUT}/sm-s-port-matrix.svg", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ markdown
def md_pins(keys):
    return "<br>".join(f"{k}: {pin(F, k)} / {pin(H, k)}" for k in keys)


def markdown():
    L = []
    a = L.append
    a("# Module pinouts and connections")
    a("")
    a("Generated by `gen_pinouts.py` from the solved pin maps (`tools/out_F429.md`, `tools/out_H743.md`). Status: PROPOSED draft. "
      "MCU pins are exact for the pin-map draft 2 (97 pins assigned). Module-side pins are only as good as their tag.")
    a("")
    a("Tags: **[P]** read by a research agent from a manufacturer datasheet or user manual; **[V]** vendor page or guide (secondary); "
      "**[K]** my recollection of the standard pinout, *not checked in this project*; **?** unknown. "
      "Port numbers P1 to P8 and the module-to-port assignment are a proposal for this document, not a decision.")
    a("")
    a("![System connections](system-connections.png)")
    a("")
    a("![SM-S port matrix](sm-s-port-matrix.png)")
    a("")
    a("## 1. What I know about each module's own pins")
    a("")
    a("| Module | Role / where it connects | Interface | Supply | Pins known | Pins not known |")
    a("|---|---|---|---|---|---|")
    a("| **CC1101** sub-GHz module (868 / 433 MHz, Indian breakouts) | SM-S port, proposed P1 | SPI mode 0, MSB, 6.5 to 10 MHz | 1.8-3.6 V, not 5 V tolerant | chip pins [P]: GDO2 = 3, GDO0 = 6. Chip [K]: SCLK 1, SO/GDO1 2, CSn 7, SI 20 | vendor breakout header order: 8-pin boards put GDO0 on pin 3 and GDO2 on 8, 10-pin boards GDO0 on 7 and GDO2 on 8 [V, partial]; check the silkscreen of the board you buy |")
    a("| **PN532 V3** NFC breakout (Variant A) | SM-S port via the adapter, proposed P2 | SPI mode 0, LSB first, 5 MHz max, IRQ active low | breakout VCC 3.3-5 V claimed [V]; chip VBAT 2.7-5.5 V, PVDD <= 3.6 V [P] | chip pins [P]: I0 16, I1 17, NSS 27, MOSI 28, MISO 29, SCK 30, P70_IRQ 25, P32_INT0 32, RSTPD_N 38. Header signal names [V]: VCC, GND, SCK, MISO, MOSI, SSEL, IRQ, RSTPDN, plus I2C/UART shares | **header order and position**, regulator, DIP switch mapping (conflicting sources) |")
    a("| **ST25R3916** NFC module (Variant B) | SM-S port, proposed P2 or P3 | SPI mode 1, MSB, 10 MHz max, IRQ active high; no reset pin | VDD/VDD_TX 2.4-5.5 V, VDD_IO 1.65-5.5 V [P] | chip pins [P]: VDD_IO 1, VDD_D 3, VDD_A 7, VDD 8, VDD_RF 9, VDD_TX 10, VDD_AM 11, VDD_DR 14, exposed pad 33 | SCLK, MOSI, MISO, BSS, IRQ, I2C_EN, XTI, XTO and antenna pin numbers (DS12484 Table 2 not read); chip not sourceable in India yet |")
    a("| **RDM6300** 125 kHz reader | SM-U port, proposed P8 | UART 9600 baud, EM4100 only | 5 V | functions only (5 V, GND, TX; antenna coil connector) [V] | header order, TX voltage level, whether an RX pin exists |")
    a("| **Generic I2C module** | SM-I ports, proposed P6, P7 | I2C 400 kHz | 3.3 V (5 V pin available) | SMIS contacts only | per module |")
    a("| **ST7796S 3.5in display** (Waveshare module, touch unused) | on-board, SPI1 | SPI, RGB565 | 3.3 V / 5 V with on-board translator [V] | signal names [V]: VCC, GND, MISO, MOSI, SCLK, LCD_CS, LCD_DC, LCD_RST, LCD_BL, TP_SDA, TP_SCL, TP_INT, TP_RST (15-pin GH1.25 cable) | physical pin order; the cable lists 13 names for 15 pins |")
    a("| **microSD socket** | on-board, SDIO / SDMMC 4-bit | SD mode | 3.3 V | standard microSD contacts [K]: 1 DAT2, 2 CD/DAT3, 3 CMD, 4 VDD, 5 CLK, 6 VSS, 7 DAT0, 8 DAT1, plus a card-detect switch | the chosen socket's own numbering (DNA Tech TF-07F 9-pin) |")
    a("| **ESP32-S3-WROOM-1** | on-board, UART1 | UART, 3.3 V | 3.0-3.6 V, own rail >= 500 mA [P] | [P]: TXD0 = GPIO43 = pin 37, RXD0 = GPIO44 = pin 36; strapping pins GPIO0, GPIO3, GPIO45, GPIO46; EN; octal-PSRAM variants lose IO35-37 | other module pad numbers not recorded; handshake GPIO not chosen |")
    a("| **USB-C receptacle** | on-board, USB FS | USB 2.0 FS | VBUS 5 V | D+ -> PA12, D- -> PA11, VBUS sense -> PA9 (MCU side, both chips); CC1, CC2 with 5.1 kohm each | CC1/CC2 ADC pins **not in the pin map** (gap) |")
    a("| **TSOP1738** IR receiver + IR LED | on-board, timer pins | 38 kHz, active-low output | **4.5-5.5 V** [P, 2001 sheet] | [K]: pin 1 OUT, 2 GND, 3 VS (verify) | newer datasheet, 3.3 V behaviour |")
    a("| Buzzer, vibration motor, 3 LEDs, 8 buttons | on-board | GPIO / PWM / PCA9535 B | 3.3 V | MCU side only | driver parts not chosen |")
    a("| **BQ24075** charger | on-board, control by GPIO/expander | none (pin-strapped) | USB 5 V | functions [P]: ISET, ILIM, EN1, EN2, CE, TS, TMR, SYSOFF, PGOOD, CHG | VQFN-16 pin numbers not recorded; EN2/CE/SYSOFF are **not in the pin map** (planned for PCA9535 B spare bits) |")
    a("| **MAX17048** fuel gauge | I2C_SYS | I2C 0x36 | VDD = cell | functions [P]: SDA, SCL, ALRT, QSTRT, CTG | TDFN-8 numbers not recorded |")
    a("| **PCA9535** x2 | I2C_SYS | I2C 0x20-0x27 | 2.3-5.5 V | functions [P]: A0-A2, SDA, SCL, INT, P0.0-P1.7 | SOIC-24 numbers not recorded |")
    a("| **INA219** x8 | I2C_SYS, one per 5V_P port | I2C 0x40-0x4F | 3.3 V | functions only | package numbers per board |")
    a("| Linux module (future) | reserved connector | UART + USB + 4 GPIO | TBD | MCU side only | module not chosen |")
    a("")
    a("## 2. MCU pins for each module (F429 / H743)")
    a("")
    a("| Module / bus | Signals (F429 / H743) |")
    a("|---|---|")
    for title, sub, rows in LEFT + RIGHT_TOP + RIGHT_BOTTOM:
        keys = [k for _, k in rows if k and (k in F or k in H)]
        if keys:
            a(f"| {title} ({sub}) | {md_pins(keys)} |")
    a("")
    a("### Ports P1 to P8")
    a("")
    a("| Port | Class | Proposed module | F429 pins | H743 pins |")
    a("|---|---|---|---|---|")
    for i, (p, cls, mod) in enumerate(PORTS):
        a(f"| {p} | {cls} | {mod} | {port_pins(F, i + 1)} | {port_pins(H, i + 1)} |")
    a("")
    a("### GPIO headers")
    a("")
    a("| Signal | F429 | H743 |")
    a("|---|---|---|")
    for n in range(1, 13):
        a(f"| GPIO_H{n} | {pin(F, f'GPIO_H{n}')} | {pin(H, f'GPIO_H{n}')} |")
    for n in range(1, 5):
        a(f"| ADC_H{n} | {pin(F, f'ADC_H{n}')} | {pin(H, f'ADC_H{n}')} |")
    a("")
    a("### Reserved pins")
    a("")
    a("| F429 | H743 |")
    a("|---|---|")
    for (fp_, fs), (hp, hs) in zip(FRES, HRES):
        a(f"| {fp_} ({fs}) | {hp} ({hs}) |")
    a("")
    a("## 3. SM-S port contact-by-contact")
    a("")
    a("| Contact | SMIS net | CC1101 module | PN532 breakout | ST25R3916 module |")
    a("|---|---|---|---|---|")
    names = list(MOD_SMS)
    for i, net in enumerate(SMS_NETS):
        a(f"| {i + 1} | {net} | " + " | ".join(MOD_SMS[n][i] for n in names) + " |")
    a("")
    a("## 4. Gaps found while building these diagrams")
    a("")
    a("1. **USB-C CC1 / CC2 ADC inputs** (needed to read the source's advertised current, `09-power-architecture.md` §2) are not in the pin maps. Two ADC pins must be added and the maps re-solved.")
    a("2. **BQ24075 control lines (EN2, CE, SYSOFF)** have no MCU pins; the plan is spare bits on PCA9535 B (8 of its 16 bits are unused).")
    a("3. **Port numbering and module assignment** (P1 to P8) were never fixed in the SMIS documents; this table proposes one.")
    a("4. **ESP32 handshake GPIO**, **vibration/buzzer drivers** and **IR LED driver** are MCU-side only; the module-side parts are not chosen.")
    a("5. Vendor breakout headers (PN532 V3, CC1101 boards, RDM6300) must be measured on the actual boards before any adapter is routed.")
    open(f"{OUT}/module-pinouts.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    system_diagram()
    matrix_diagram()
    markdown()
    print("done")
