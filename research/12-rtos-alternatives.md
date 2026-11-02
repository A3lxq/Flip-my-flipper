# RTOS and framework alternatives (condensed)

Condensed from a research-agent report checked 2026-11-02 (GitHub API, raw files, crates.io, FSF licence list). Nothing was built or measured; "open issues" includes open pull requests. Not legal advice. Status: IN = supported in tree, COM = community/external package, MISS = missing, UNK = not verified. FSF quotes (https://www.gnu.org/licenses/license-list.html): Apache-2.0 "compatible with version 3 of the GNU GPL … not compatible with GPL version 2"; Expat (MIT) and modified BSD "compatible with the GNU GPL"; LGPLv3 "compatible with GPLv3".

## Apache NuttX
nuttx-13.1.0 (commit dated 2026-09-26); last commit 2026-11-02; about 728 open issues/PRs; about 4.1k stars. Apache-2.0 (`LICENSE`, `NOTICE`). Make + CMake with Kconfig; apps in apache/nuttx-apps.
Boards: `boards/arm/stm32f4/nucleo-f429zi`, `stm32f429i-disco`; `boards/arm/stm32h7/nucleo-h743zi`, `weact-stm32h743`, `devebox-stm32h743`, `openh743i`.
| Need | Status | Evidence |
|---|---|---|
| SPI LSB-first, per-transaction mode/frequency/lock | IN | `include/nuttx/spi/spi.h` `HWFEAT_LSBFIRST`; H7 `stm32_spi.c` handles it; F4 LSB-first unchecked |
| I2C | IN | `stm32_i2c.c` (H7) |
| SDIO (F4), SDMMC (H7), MMC/SD | IN | `stm32_sdio_m3m4_v1.c`, `stm32h7/stm32_sdmmc.c`, `drivers/mmcsd/mmcsd_sdio.c`; FAT UNK |
| USB device F4 OTG FS/HS | IN | `stm32_otgfsdev_m3m4_v1.c`, `stm32_otghsdev_m3m4_v1.c`; H7 `stm32_otgdev.c`; HS-in-FS on H7 UNK |
| CDC/MSC/composite | IN | `drivers/usbdev/cdcacm.c`, `usbmsc.c`, `composite.c`; `nucleo-h743zi/configs/composite` |
| ST7796 | IN | `drivers/lcd/st7796.c` |
| LVGL | COM | `nuttx-apps/graphics/lvgl`, `examples/lvgldemo`; version UNK |
| Bootloader | IN | `boot/mcuboot`, `boot/nxboot`, `boot/miniboot`; configs `mcuboot-app/loader`, `nxboot-app/loader` |
| CC1101 | IN | `drivers/wireless/cc1101.c` (board file only for nucleo-l476rg) |
| PN532 | IN | `drivers/contactless/pn532.c` (plus `mfrc522.c`) |
| ST25R3916 | MISS | grep found nothing |
| ESP32-S3 over UART | UNK | |
POSIX-style (VFS, /dev, NSH shell), good Sphinx docs, Kconfig-heavy, substantial bring-up; each chip family has its own driver copy; footprint unknown.

## RT-Thread
v5.3.0 (2026-09-10); last commit 2026-10-30; about 545 open; about 12.3k stars. Apache-2.0; SCons + Kconfig. BSPs: `bsp/stm32/stm32f429-st-disco` (+3), `stm32h743-st-nucleo` (+3). Drivers on ST HAL: `drv_spi.c`, `drv_sdio.c`, `drv_usbd.c`. SPI/I2C/UART/GPIO IN; SDIO + DFS FAT IN; USB device IN/COM (CherryUSB, Apache-2.0); LVGL package versions 9.0.0/9.1.0 (default 9.0.0); mcuboot package; CC1101 MISS; PN532 COM (Adafruit shim); ST25R3916 MISS; no STM32 ST7796S driver. Documentation uneven; community mostly Chinese-language.

## Eclipse ThreadX
ThreadX v6.5.2.202603b (2026-11-01), USBX/FileX/GUIX v6.5.2.202603 (2026-10-02), NetX Duo 202603b. MIT (`LICENSE.txt`; source header SPDX MIT, "Eclipse ThreadX contributors"). USBX, FileX, GUIX, NetX Duo, LevelX, TraceX are open (org `eclipse-threadx`). CMake. `ports/cortex_m4`, `cortex_m7`; STM32 glue in `eclipse-threadx/supported-platforms` (USBX DCD over ST HAL PCD, FileX SD/MMC drivers over HAL; Ethernet only for NetX; no Nucleo board directories). USB CDC/MSC classes IN; SD/FAT IN (FileX); LVGL UNK (GUIX is a different GUI library); SPI/I2C/UART/GPIO via ST HAL; ST7796S, CC1101, PN532, ST25R3916, bootloader MISS.

## Rust with Embassy
embassy-stm32 0.6.0 (2026-03-20), embassy-usb 0.6.0, embassy-boot 0.7.0, embassy-boot-stm32 0.8.0, embassy-executor 0.10.0, embassy-embedded-hal 0.6.0; last commit 2026-10-30; about 596 open; about 10k stars. `MIT OR Apache-2.0`; Cargo + probe-rs. Features `stm32f429zi`, `stm32f429ii`, `stm32h743ii`. SPI `Config { bit_order, frequency }`; shared-bus `SpiDeviceWithConfig` calls `set_config` per transaction (`embassy-embedded-hal/src/shared_bus/asynch/spi.rs`); SDMMC (F4 SDIO detail UNK) + `embedded-sdmmc` 0.10.0 for FAT; USB `Driver::new_fs/new_hs/…ulpi` (MSC UNK; HS-in-FS UNK); embassy-boot (DFU UNK). LVGL: `lv_binding_rust` last push 2025-01-22, crate `lvgl` 0.6.2 (2023); no LVGL 9 binding confirmed; `embedded-graphics` 0.8.2 and `mipidsi` 0.10.0 (MIT) as Rust-native options (ST7796 UNK). CC1101 crate `cc1101` 0.1.3 (Apache-2.0); PN532 crate `pn532` 0.5.0 (MIT OR Apache-2.0); ST25R3916: only `techmccat/st25r39`, "WIP", no licence. RTIC 2.4.0 (MIT OR Apache-2.0) is an alternative executor. Steep learning curve; 0.x APIs break between releases.

## ChibiOS
Tag ver21.11.5 (2026-04-04); master kernel 8.0.0 (no tag); GitHub is a read-only mirror of SVN; last commit 2026-05-31; 28 open. **RT kernel header: "GNU General Public License … version 3 of the License" = GPL-3.0-only**; HAL Apache-2.0; commercial licences exist. GNU Make. Boards `ST_NUCLEO144_F429ZI`, `ST_NUCLEO144_H743ZI`, `ST_STM32F429I_DISCOVERY`; own LLDs (OTGv1, SDIOv1, SDMMCv1/v2, SPIv1–v4, I2Cv1–v4, QUADSPI). FatFs binding; USB classes, LVGL, bootloader, radios not in tree.

## Mbed OS
End of life (Arm: Mbed OS and the platform "will reach end of life in July 2026"; announced 2024-07-09 per secondary sources). Repo not archived; last push 2024-10-08; release mbed-os-6.17.0 (2023-02-28). Apache-2.0. Mbed CE fork (mbed-os-7.1.0, 2026-09-29, CMake): F429ZI/H743ZI targets UNK. Do not start new work on the original.

## libopencm3 / bare metal / STM32 LL
libopencm3: LGPL-3.0-or-later (README; GitHub detector says GPL-3.0, a mismatch), only tag v0.8.0 (2020), last commit 2026-10-15. F4 supported; H7 has only fdcan/flash/pwr/rcc; SD host driver absent; FAT, LVGL, display, bootloader, radios missing. ST LL drivers are BSD-3-Clause but bring no USB or FAT.

## Arduino framework (STM32duino)
Core 3.0.0 (2026-07-23). LGPL-2.1 core, BSD-3 HAL, Apache CMSIS, **ST "Ultimate Liberty" (SLA0044) in `system/Middlewares/STM32_USB_*_Library` and `libraries/USBDevice`** (excluded). RadioLib 7.8.1 (MIT, CC1101), Adafruit-PN532 1.3.4 (BSD), LVGL 9.6.0 (MIT), SdFat 2.3.1 (MIT); `stm32duino/ST25R3916` is SLA0052 (excluded). Prototyping only.

## Others
Tock release-2.3.0 (Apache-2.0 or MIT; F429 boards but no STM32H7 chips); Hubris (MPL-2.0; server-focused); Apache Mynewt (Apache-2.0; weact_h743vi and nucleo-h753zi BSPs); Contiki-NG v5.2 (BSD-3; networking-focused). All poor fits.

## Side-by-side (extract)
| | Zephyr | FreeRTOS+Cube | NuttX | RT-Thread | ThreadX | Embassy | ChibiOS |
|---|---|---|---|---|---|---|---|
| Licence | Apache-2.0 | MIT + BSD-3 | Apache-2.0 | Apache-2.0 | MIT | MIT OR Apache-2.0 | GPL-3.0-only kernel, Apache HAL |
| In-tree CC1101 / PN532 | no / no | no / no | **yes / yes** | no / package | no / no | crates | no / no |
| ST7796S | yes | LVGL callbacks | yes | no | no | unknown | no |
| LVGL 9 | 9.6.0 in tree | add | version unknown | 9.0–9.1 | unknown | stale bindings | no |
| Bootloader | MCUboot | assemble | MCUboot, nxboot | mcuboot pkg | none | embassy-boot | none |
| ST25R3916 | no | no | no | no | no | WIP unlicensed | no |

Ranked recommendation (agent): 1 Zephyr; 2 FreeRTOS + Cube (HAL/LL only); 3 NuttX; 4 Rust + Embassy; 5 ThreadX; 6 RT-Thread; 7 ChibiOS; 8 libopencm3/LL; 9 STM32duino; 10 Mbed OS.

## Unknowns
NuttX FAT and LVGL version, F4 SPI LSB-first; OTG HS in FS mode for every option; LSB-first in RT-Thread/ChibiOS; Embassy MSC class and ST7796S via mipidsi; stm32-metapac licence; Mbed CE targets; ESP32-S3 UART in each option; LVGL OS abstraction on ThreadX; RAM/flash footprints; Arm's own Mbed EOL post (not fetched).
