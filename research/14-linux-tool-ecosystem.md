# Linux user-space ecosystem and hybrid designs (condensed)

Condensed from a research-agent report checked 2026-11-02. A software-architecture and licensing survey of lawful tooling; no attack details. Licences from the GitHub API SPDX field or first lines of LICENSE/COPYING; kernel facts from `torvalds/linux` master. The GitHub API rate limit ran out partway; unmarked items are unverified. Not legal advice.

## Sub-GHz
CC1101 has no mainline kernel driver (`drivers/net/ieee802154/Kconfig` lists only CC2520; MAINTAINERS has no cc1101 hits), so it is driven through spidev. RadioLib (MIT, pushed 2026-11-01) lists the CC1101; a Linux HAL was not confirmed. python-cc1101 (fphammerle): licence not found. Universal Radio Hacker GPL-3.0, rtl_433 GPL-2.0 (receive-only SDR decoding), GNU Radio GPL-3.0, gqrx GPL-3.0 all need SDR hardware, not a CC1101.

## NFC and RFID
Kernel `drivers/nfc` (GPL-2.0-only): fdp, microread, nfcmrvl, nxp-nci, pn533, pn544, port100, s3fwrn5, st-nci, st21nfca, st95hf, trf7970a. Buses: pn533 USB/I2C/UART(serdev); nxp-nci I2C; st21nfca I2C; st-nci I2C+SPI; st95hf SPI; trf7970a SPI; pn544 I2C+MEI; s3fwrn5 I2C/UART; nfcmrvl USB/UART/I2C/SPI. libnfc LGPL-3.0 (PN532 over UART works through libnfc drivers; list not verified); neard GPL-2.0; nfc-tools mfoc GPL-2.0 (run separately or avoid). Proxmark3 (RRG/Iceman) GPL-3.0: host client on a PC/SBC talking over USB/UART to ARM + FPGA hardware. No LF RFID kernel driver or standalone Linux library found.

## Infrared
`gpio-ir-recv.c` (`IR_GPIO_CIR`, GPL-2.0-only), `gpio-ir-tx.c` (`IR_GPIO_TX`, depends on LIRC, GPL-2.0-or-later, bit-banged so timing depends on scheduling), `pwm-ir-tx.c`, `ir-spi.c` (GPL-2.0). LIRC 0.10.2 (2022-10-04); licence not found on its page.

## Wi-Fi, Bluetooth, network tools, distributions
BlueZ GPL-2.0; aircrack-ng GPL-2.0 (LICENSE file; headers unchecked); Kismet GPL2 with some less restrictive subcomponents; bettercap GPL-3.0; Wireshark GPL-2.0; iw/nl80211 (monitor mode depends on the chipset driver); wpa_supplicant licence not checked. **nmap: NPSL v0.95** — §2: "You may not distribute Covered Software or Derivative Works under plain GPL terms without special permission from Licensor"; the licence defines GPL as version 2; not on the FSF list. Distributions: Kali ARM supports Raspberry Pi 1–5/Zero, BeagleBone Black, ODROID, Pinebook Pro, Radxa Zero, USB Armory, Chromebooks (not a 3.5-inch handheld distribution); Kali NetHunter is Android-based (its page calls its app store outdated); Buildroot GPL-2.0-or-later; Yocto/OpenEmbedded metadata MIT; Armbian build framework GPL-2.0; Parrot, Alpine, postmarketOS not checked.

## USB gadget and host
Kernel configfs gadget framework (`Documentation/usb/gadget_configfs.rst`, GPL-2.0) with `f_hid.c` (GPL-2.0-only), `f_mass_storage.c`, `f_ecm.c`, `f_acm.c`. libusb and usbutils not checked.

## UI stacks and handheld Linux projects
LVGL MIT (a Linux fbdev/DRM/evdev page upstream; raw path 404 so unverified); SDL Zlib (FSF compatibility not confirmed); Qt, GTK, terminal UIs not checked. Pwnagotchi GPL-3.0 (Pi + e-paper); RetroPie-Setup GPL-3.0; ClockworkPi uConsole (CM3/CM4-class, 5 inch 1280×720 per secondary sources; case model GPL v3); ClockworkPi PicoCalc (MCU device, GPL v3). No boot-time or power numbers found for any of them.

## Hybrid designs
Flipper One (see report 13); STM32MP1/MP2 with Linux RemoteProc + RPMsg and OpenAMP on the Cortex-M (ST wiki, snippets only); Zephyr sample `samples/subsys/ipc/openamp_rsc_table/README.rst` "compatible with platforms that embed a Linux kernel OS on the main processor and a Zephyr application on the co-processor"; Collabora 2021 article on Zephyr on STM32MP1; Proxmark3. Common pattern: the MCU owns real-time and low-power peripherals, Linux owns networking, UI and tooling, linked by USB/UART or RPMsg.

## Licence compatibility with GPL-3.0-or-later
FSF quotes (license list and GPL FAQ, fetched 2026-11-02): GPLv2 "is, by itself, not compatible with GPLv3. However, most software released under GPLv2 allows you to use the terms of later versions"; code under "version 2 or later" is compatible; aggregation of "separate programs, distributed together" is permitted; "pipes, sockets and command-line arguments are communication mechanisms normally used between two separate programs"; Apache-2.0, Expat, modified BSD, LGPLv3 compatible.
| Component | Licence | Combine into the work? |
|---|---|---|
| RadioLib, LVGL | MIT | yes |
| SDL | Zlib | likely; verify |
| libnfc | LGPL-3.0 | yes |
| Proxmark3, URH, GNU Radio, gqrx, bettercap, Pwnagotchi, RetroPie-Setup | GPL-3.0 | yes |
| rtl_433, aircrack-ng, BlueZ, Wireshark, neard, mfoc | GPL-2.0 (per-file "or later" unchecked) | separate programs unless "or later" |
| Kismet | GPL-2.0 + mixed | separate program |
| Linux kernel | GPL-2.0 WITH Linux-syscall-note | do not link; use syscalls, configfs, netlink |
| nmap | NPSL v0.95 | no, without permission |
| linux-firmware blobs | per-file redistributable licences (`WHENCE`) | ship as separate non-free files |
GPLv3-specific point: the FAQ says GPLv3 requires "Installation Information" for user products (passage not read in full); consider this if shipping hardware with locked firmware.

## Regulatory
No official statement about Linux-based radio devices needing ETA was found; India's WPC/ETA rules were not researched in this pass (see `07-india-regulatory.md`).

## Risks
CC1101 on Linux has no kernel driver and Linux jitter affects timing-sensitive protocols; SDR-only tools; monitor mode depends on the Wi-Fi chipset driver; GPL-2.0-only tools cannot be merged; NPSL; firmware blobs; GPLv3 installation information; power and boot time not sourced.
