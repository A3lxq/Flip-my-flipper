# Operating-system options and the Linux-first question

Status: PROPOSED analysis (2026-11-02), based on three research reports (`research/12-` to `research/14-`). Nothing was built or measured; Linux power, boot-time and latency figures for the candidate boards were not found. Not legal advice.

## 1. Questions answered

1. **Other ways to run the firmware besides Zephyr?** Yes: ten options were assessed (summary in §2).
2. **Can the device be built Flipper-One-style, with ARM Linux as the OS and the tools built around it?** Technically yes for the networking and tooling layer, but not as "Linux alone": Flipper One itself keeps a FreeRTOS microcontroller, and the kernel lacks drivers for this device's radio and NFC chips (§3). The sensible form is a **hybrid** (§4), which is what this project's reserved Linux connector already allows.

## 2. Microcontroller OS options (for the STM32F429 / STM32H743 core)

Ranking from the research agent, with this project's reading:

| Rank | Option | Why | Main drawback |
|---|---|---|---|
| 1 | **Zephyr 4.5.0** (baseline) | Most of the platform in tree: boards for both MCUs, SPI with per-transfer LSB-first config, SD, USB, ST7796S driver, LVGL 9.6.0, MCUboot, power management, host tests | No CC1101, PN532 or ST25R3916 driver; H743 second USB needs a custom node |
| 2 | FreeRTOS + STM32Cube (HAL/LL only) | MIT kernel, Flipper Zero precedent, simplest licensing | Everything above the kernel is assembled by us |
| 3 | **Apache NuttX** | Only option with in-tree **CC1101** and **PN532** drivers, plus ST7796, SPI LSB-first, SD/SDIO, USB CDC/MSC, MCUboot/nxboot, and boards for both Nucleo parts | POSIX-style, heavy configuration, LVGL version unknown, no ST25R3916 |
| 4 | Rust + Embassy | Per-transaction SPI config, embassy-boot, CC1101 and PN532 crates | LVGL 9, ST25R3916 and ESP32 UART missing; UI redone; steep learning curve |
| 5 | Eclipse ThreadX (MIT) | Open USBX, FileX, GUIX | STM32 glue depends on ST HAL; no radios, display, bootloader |
| 6 | RT-Thread | Many STM32 board packages | LVGL package lags, no CC1101, thin English community |
| 7 | ChibiOS | Good low-level drivers | Kernel is **GPL-3.0-only** (no "or later"); little middleware |
| 8 | libopencm3 / bare metal | Smallest | H7 minimal, no SD driver |
| 9 | STM32duino / PlatformIO | Fast to prototype | ST-licensed USB stack and ST25R3916 library (excluded) |
| 10 | Mbed OS | — | End of life (July 2026) |

Common gap: **no option has a usable ST25R3916 driver under a compatible licence**; the project must write one (ST's RFAL cannot enter a distributed GPL binary, see `10-firmware-architecture.md` §14).

**Decision impact:** Zephyr 4.5.0 was accepted as the working RTOS on 2026-11-02 after the build-level de-risk checks. NuttX is the runner-up if the Zephyr de-risk builds fail and driver coverage matters more than ecosystem size; FreeRTOS + Cube is the runner-up if licensing simplicity and Flipper-Zero-like structure matter more. The firmware's OS wrapper keeps the choice replaceable.

## 3. What Flipper One actually is (public sources)

- Announced 21 May 2026; prototype hardware; price and ship date unconfirmed (about $350 target per press).
- **Linux main processor + FreeRTOS microcontroller**: Rockchip RK3576 (8 cores, 8 GB RAM, 64 GB UFS) running mainline Linux, plus a Raspberry Pi RP2350B co-processor that drives the display, buttons, power states and boot sequencing. Link: UART (console), SPI (framebuffer), I²C (commands/events), an interrupt pin and boot-select lines.
- **No NFC, RFID or sub-GHz** in the published spec: it is a Linux and networking multi-tool (Wi-Fi 6E, Bluetooth 5.2, dual Gigabit Ethernet, USB 3, HDMI, M.2 expansion). Offline radio protocols stay on Flipper Zero's microcontroller class.
- Battery listed 7,000 mAh / 24 Wh (not final); this project's planned cell is 3000–3500 mAh (about 11–13 Wh).

## 4. Architecture options for this project

| | A. MCU only (current V1) | B. Linux only | C. Hybrid: MCU + Linux module |
|---|---|---|---|
| Sub-GHz, NFC, 125 kHz, IR timing | MCU handles in firmware | Kernel has **no CC1101 or ST25R3916 driver and no PN532-over-SPI driver**; `gpio-ir-tx` cannot be built on a PREEMPT_RT kernel and has no hardware carrier; no evidence found that user space meets the timing | MCU keeps all real-time radio/NFC/IR work |
| Networking, Wi-Fi/BT tools, USB gadget (HID, mass storage, serial), network analysers | limited | strong: mature mainline support and tools (BlueZ, Wireshark, bettercap, aircrack-ng…); monitor mode depends on the Wi-Fi chipset | Linux module does this |
| Power / battery life | low | no sourced figures; Pi Zero 2 W third-party idle about 100–130 mA at 5 V (rough: about 0.5–0.65 W, so very roughly 17 h idle on an 11 Wh cell, ignoring conversion loss, radios and load) | Linux can be powered down when not needed (the MCU keeps running); matches Flipper One's pattern |
| Boot time | fast | not found | MCU instant; Linux boots on demand |
| Display / UI | LVGL on ST7796S driver in Zephyr | no ST7796 kernel driver (generic `panel-mipi-dbi` with an init file; or a DSI/RGB panel); LVGL on Linux exists | MCU drives the 3.5" screen; Linux can send framebuffer data (Flipper One pattern) or use its own display later |
| India-only sourcing | STM32 sourcing already studied | Linux modules: Hubtronics lists CM4/CM5 as "Notify when available"; Pi Zero 2 W out of stock at DNA Tech; leads at Robu/Quartz/Robocraze unconfirmed; no Indian listing for Rockchip/i.MX 93/STM32MP2 modules | Same Linux sourcing question, but only as an optional module |
| Licensing | GPL-3.0-or-later project + permissive libraries | Linux kernel is GPL-2.0-only; user space talks to it through system calls and stays a separate work; GPL-2.0-only tools can only be invoked as separate programs; nmap's NPSL is not plain-GPL distributable; Wi-Fi/BT firmware blobs are redistributable but not free | same, plus the inter-processor protocol |
| Board complexity | lowest | high (DDR, PMIC, high-speed layout) unless a ready compute module is used | moderate: a module plugs into the reserved connector |
| Regulatory | per-radio ETA etc. | adds the Linux host's radios to ETA scope | same |
| Tool ecosystem | custom apps | huge | best of both |

**Recommendation (PROPOSED):**
1. Keep **A as V1** (decided: MCU-only with a reserved Linux connector, R8).
2. Treat the Linux side as a **future pluggable module (option C)**, modelled on Flipper One's division of labour: the MCU owns display, buttons, power, boot sequencing and all real-time radio/NFC/IR; Linux owns networking, tools, USB-gadget testing and bigger UIs. This is also what the Proxmark3 (host client + ARM/FPGA hardware) and STM32MP1/MP2 (Linux on Cortex-A + RTOS on Cortex-M, RPMsg/OpenAMP) do.
3. Do **not** choose B (Linux alone): the missing kernel drivers, the timing risk and unsourced power figures make it the riskiest path, and it would still need the MCU.
4. When the Linux module is designed, pick the module from what Indian sellers actually stock (first candidates by evidence: Raspberry Pi Zero 2 W and CM4/CM5, all currently unconfirmed in stock) and define the MCU↔Linux protocol (framed, versioned, UART/USB; Flipper One uses UART console + I²C commands + SPI framebuffer + INT line) in a later SMIS-style document.

**What would change this:** confirmed Indian stock of a suitable Linux module; a measured real-time test of user-space SPI to the CC1101/PN532 at the required timing; a decision to prioritise networking tools over radio/NFC work.

## 5. Open items

1. Choose the OS wrapper API so Zephyr/NuttX/FreeRTOS stay interchangeable (`10-firmware-architecture.md` §2).
2. NuttX evaluation only if the Zephyr de-risk builds fail (FAT, LVGL version, H7 USB HS-in-FS).
3. Reproducible real-time latency test of Linux user-space SPI on a candidate board.
4. Official power tables and boot times (Raspberry Pi datasheets, Rockchip, NXP, ST AN5726/AN5730).
5. Indian stock by hand at Robu, Robocraze, Quartz Components, Thingbits and others.
6. MCU↔Linux protocol design; legal review of GPL-2.0-only/NPSL/firmware-blob handling and GPLv3 "Installation Information" for shipped hardware.
