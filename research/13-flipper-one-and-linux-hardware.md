# Flipper One architecture and Linux compute options (condensed)

Condensed from a research-agent report checked 2026-11-02. Nothing built or measured. Tags: P primary, S secondary. Blocked or unread: flipper.net product page (429), ST and Radxa pages, Pi power datasheets, robu.in/robocraze.com/thinkrobotics.com/quartzcomponents.com/robodo.in/zbotic.in product pages (403/429), FSF GPL FAQ (429).

## Flipper One (public information)
- Announced 21 May 2026 (P: https://blog.flipper.net/flipper-one-we-need-your-help/). Flipper OS still prototyping; FlipCTL at concept/architecture stage. S: The Register (2026-05-21): first prototype exists; Kickstarter expected "at the end of the summer" (not checked); target about $350; no NFC or RFID.
- Tech specs (P, branch `public-release`, specs may change): https://raw.githubusercontent.com/flipperdevices/flipperone-docs/public-release/docs/general/Tech-Specs.md
| Item | Value |
|---|---|
| SoC | Rockchip RK3576: 4× Cortex-A72 + 4× Cortex-A53 up to 2.2 GHz; Mali-G52 MC3; 6 TOPS NPU |
| RAM / storage | 8 GB LPDDR5; 64 GB UFS 2.2 + microSD (blog says no onboard storage; spec file is newer) |
| Co-processor | Raspberry Pi RP2350B (dual M33 + dual Hazard3, 150 MHz, 520 KB SRAM, 16 MB flash) |
| Display | 256×144 monochrome LCD driven by the RP2350 over QSPI |
| Power | battery listed 7,000 mAh / 24,000 mWh (not final); TI BQ25792 charger (3.32 A); BQ28Z620 fuel gauge (blog/CNX say BQ28Z610); GPIO rails 3.3 V and 5 V, 2 A each via eFuse |
| Radios | MediaTek MT7921AUN over USB: Wi-Fi 6E 2×2, Bluetooth 5.2; cellular/NTN via M.2 (planned) |
| Wired / USB / video | 2× Gigabit Ethernet; USB-C1 USB 3.1 + DP Alt + PD; USB-C2 and USB-A host only; HDMI 2.1; DP 1.4 |
| Expansion / size | M.2 Key-B (PCIe 2.1 x1, USB, SATA3, UART, I2C, SIM), GPIO header, debug; 155×67×40 mm |
- Software: mainline Linux for RK3576 with Collabora (one binary blob remains, the DDR trainer; NPU not yet mainline); Flipper OS Debian-based; FlipCTL menu UI. **MCU side runs FreeRTOS** (flipperone-docs `mcu-firmware/Architecture.md`): LCD and backlight, buttons/touchpad/haptics, headphone detection, battery/power subsystems and power states, power-on/boot sequencing of the main CPU, USB-C CC pins, LEDs. **MCU-to-CPU link** (`MCU-CPU-interconnect.md`): UART (Linux console), SPI (framebuffer Linux → RP2350), I2C (Linux master for commands, MCU returns input events), INT pin for pending events, BOOT0 to put the CPU into MaskROM mode, BOOT1 as a PWM-derived voltage the CPU reads to choose the boot source.
- Repos under github.com/flipperdevices: flipperone-docs, flipperone-hardware, flipperone-mcu-firmware, flipperone-linux-build-scripts, flipper-linux-kernel, rockchip-linux, rkbin, u-boot, flipperone-debug-probe, flipctl-slint, flipctl-apps. Licence of the docs repo and openness of the hardware repo not checked.
- Not public: final price, ship date, final battery capacity, measured battery life, idle power, boot time, schematic licence. **No sub-GHz, NFC or RFID in the published spec.**
Takeaway: Flipper One is Linux-primary with a small RTOS MCU for display, input, power and boot sequencing.

## Linux compute candidates (official facts only)
| Candidate | Facts | Source |
|---|---|---|
| Pi Zero 2 W | quad A53 1 GHz, 512 MB, 65×30 mm, $15, 2.4 GHz Wi-Fi, BLE 4.2, micro-USB OTG, microSD, CSI-2; no DSI listed | https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/ |
| CM4 | BCM2711 quad A72 1.5 GHz; 1/2/4/8 GB; Lite or 8/16/32 GB eMMC; from $41.25 | https://www.raspberrypi.com/products/compute-module-4/ |
| CM5 | BCM2712 quad A76 2.4 GHz; 2/4/8/16 GB; 55×40×4.7 mm; 2× 4-lane DSI/CSI; PCIe Gen2 x1; 1× USB 2.0 + 2× USB 3.0; 1× SDIO; up to 30 GPIO; from $67.50 | https://www.raspberrypi.com/products/compute-module-5/ |
| Radxa CM5 | RK3588S, LPDDR4x, 55×40 mm | S: CNX Software |
| Luckfox Pico Ultra | RV1106G3 single A7 1.2 GHz, 256 MB, 100 Mb Ethernet | S |
| Milk-V Duo S | SG2000, 512 MB, 43×43 mm, from $9.9, 5 V/1 A, 4-lane MIPI DSI via header | https://milkv.io/duo-s |
| NXP i.MX 93 | 1–2× A55 1.7 GHz + M33 250 MHz; MIPI-DSI, LVDS, RGB; 2× USB 2.0; 8× SPI | NXP page |
| STM32MP1/MP2 | ST pages timed out; ST publishes AN5730 (power) and AN5726 (low-power modes), not opened | S |
Power: no official idle/typical/max tables found. Third-party Pi Zero 2 W idle about 100–130 mA at 5 V and up to about 500 mA loaded (Tom's Hardware reported 280 mA idle; conditions differ). Boot time, mainline status per SoM and open schematics: not found.

## Indian availability (2026-11-02)
Nothing confirmed in stock by an opened page. Hubtronics (https://hubtronics.in/raspberry-pi-boards?page=2): CM5 4 GB/16 GB eMMC ₹7,280, CM5 2 GB ₹7,969, 4 GB no eMMC ₹7,139, 8 GB/32 GB ₹9,989, 16 GB no eMMC ₹13,570, CM4 variants ₹6,075–10,707, all "Notify When Available" (prices look GST-inclusive; not stated); Pi 4 1 GB ₹4,720 "Buy Now". DNA Tech: Pi Zero 2 W ₹2,035.50 incl. GST, out of stock. Snippet-only leads: Robu CM5 4 GB/16 GB ₹7,149 "in stock"; Quartz Components Pi Zero 2 W ₹1,420 ex GST "234 in stock"; Robocraze Pi Zero 2 W ₹1,909 (both "Sold out" and "6 left"). No Indian listing found for RK3576/RK3588S modules, i.MX 93 or STM32MP2 SoMs. Pi's official reseller page lists Aryabot, e2u, Robu, Silverline (domains only; stock not confirmed). Not checked: Evelta, Probots, Thingbits, Sunrom, Tanna TechBiz, Amazon.in.

## Linux feasibility (kernel tree at commit 6628e7d4c6b2, 2026-11-01, v7.4-rc1)
| Topic | Finding |
|---|---|
| CC1101 | no driver anywhere in the tree (only `cc2520.c` in ieee802154); use spidev |
| PN532 | `drivers/nfc/pn533/` supports USB, I2C, UART (serdev); **no SPI**; DT binding `nxp,pn532.yaml` |
| ST25R3916 | no driver |
| Other NFC | st95hf (SPI), st21nfca, st-nci, trf7970a (SPI) |
| ST7796S | no driver in fbtft, drm/tiny or drm/panel; generic `panel-mipi-dbi.c` loads an init sequence from a firmware file |
| IR | `gpio-ir-tx.c` (`IR_GPIO_TX`) depends on `!PREEMPT_RT`, bit-banged, no hardware carrier; `pwm-ir-tx.c` needs PWM + HIGH_RES_TIMERS; `gpio-ir-recv.c` |
| USB gadget | f_hid, f_mass_storage, f_acm, f_ecm, f_ncm, f_rndis, f_midi, f_uvc; configfs doc |
| Power | `max17040_battery.c` covers MAX17048/49/58; `bq27xxx_battery`; chargers bq24257, bq24735, bq2415x, bq25890, bq256xx, bq2515x, bq25980; **no bq24075 driver**; generic `CHARGER_GPIO` |
| Co-processor | remoteproc `stm32_rproc.c`, `imx_rproc.c`; `rpmsg_char.c` |
| LF RFID | nothing found |
Latency (S, thin): PREEMPT_RT merged in Linux 6.12; a university tutorial rule of thumb is 50–500 µs worst case on stock and under 50 µs with RT (no Pi data); no reproducible cyclictest result for any candidate board; no evidence found that user-space Linux meets sub-GHz or bit-banged IR timing.

## Hybrid options
(a) Linux alone: Luckfox and Milk-V run Linux alone; kernel gaps above mean user space or new drivers. (b) MCU alone: the current plan; Proxmark3 uses an ARM MCU + FPGA with a host client. (c) Linux + MCU: Flipper One (UART, SPI, I2C, INT, BOOT lines); STM32MP1/MP2 and i.MX use remoteproc + RPMsg. No source with formal pros and cons.

## Licensing (not legal advice)
`COPYING` in torvalds/linux: "GPL-2.0 WITH Linux-syscall-note … the GNU General Public License version 2 only"; the note says user programs using kernel services by normal system calls are not derived works; "the only valid version of the GPL as far as the kernel is concerned is _this_ particular version (ie v2, not v2.2 or v3.x)". Kernel docs (https://docs.kernel.org/process/license-rules.html): the syscall boundary "does not extend the GPL requirements to any software which uses it to communicate with the kernel". Agent's reading: user-space programs are separate works; code linked into the kernel is GPL-2.0-only, which the FSF treats as incompatible with GPLv3 for a combined work (FSF FAQ not fetched; verify). Blobs: Flipper's DDR trainer and Wi-Fi/cellular firmware are closed (S); Raspberry Pi, Rockchip and Broadcom firmware licences not checked.

## Unknowns
Hardware repo contents and licence; official power tables; Indian stock by hand on blocked sites; boot times; mainline status per SoM; schematics; reproducible RT latency; FSF FAQ quote.
