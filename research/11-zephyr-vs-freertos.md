# Zephyr vs FreeRTOS + STM32Cube (condensed)

Condensed from a research-agent report checked 2026-11-01. Not legal advice. Nothing was built: no Arm toolchain, west or Zephyr SDK was available, so all footprint figures are "not found". st.com was unreachable; ST licence texts come from ST's GitHub repositories or third-party copies. See `research/README.md` for general limits.

## Zephyr (tag v4.5.0, commit 41d10b59…)
- Releases: 4.5.0 on 2026-10-28 (supported to 2027-10-28); 4.4.0 on 2026-04-14; LTS 3.7.0 (supported to 2029-07-27); next LTS 4.6 planned April 2027; six-monthly cadence (`doc/releases/index.rst`).
- Boards in tree: `boards/st/nucleo_f429zi`, `nucleo_h743zi`, `stm32f429i_disc1`. SoCs `soc/st/stm32/stm32f4x`, `stm32h7x`. F429: `sram0` 192 KB, `ccm0` 64 KB memory region, 2 MB flash. Custom board = directory with board.yml, dts, defconfig, Kconfig.board, yaml, pinctrl.
- SPI: `SPI_MODE_CPOL`, `SPI_MODE_CPHA`, `SPI_TRANSFER_LSB`; `spi_stm32_configure()` reprograms CPOL, CPHA, bit order and baud prescaler when the `spi_config` differs (`drivers/spi/spi_stm32.c`); DT property `spi-lsb-first`.
- I²C STM32 and bit-bang (`i2c_gpio.c`); UART async/DMA; GPIO/EXTI; PWM; ADC.
- SD: F4 legacy `SDMMC_STM32` disk driver (no F4 board in tree enables it); H7 `SDHC_STM32_SDMMC` (excludes F1/F2/F4/F7/L1). FatFs R0.16p2 (ChaN, 2025).
- USB: legacy and new (`udc_stm32.c`, DWC2) stacks; samples cdc_acm, mass, dfu. F429 `usbotg_hs` (FS PHY) defined in `stm32f405.dtsi`; **H743 defines only `usbotg_fs`** (`usbotg_hs` exists for H723/H745/H7A3), so a custom node is needed. Two controllers in one image: not found.
- Display: `drivers/display/display_st7796s.c` with binding `sitronix,st7796s` (MIPI-DBI SPI), also ILI9488 and ST7789V drivers. LVGL module 9.6.0 (zephyrproject-rtos/lvgl commit dated 2026-10-02); gpio-keys input; NVS/settings; MCUboot (module pinned) and DFU; `subsys/pm`.
- Radio/coprocessor: ESP32 Wi-Fi via `drivers/wifi/esp_at` (Apache-2.0 firmware esp-at); BLE via `hci_uart` (ESP32 firmware side unverified). **No in-tree CC1101, PN532 or ST25R3916 driver.** Community: studiofuga/cc1101 (Apache-2.0, last push 2025-02-22), Bwooce/zephyr-st25r3916 ("IN DEVELOPMENT, not yet working: compiles, never validated on hardware"), vouch-opensource/zephyr-st25r (Apache-2.0, last push 2023-05-04), kenthauser/st-nfc (no licence).
- Footprint: only the LVGL sample's twister floors (`min_flash: 250`, `min_ram: 32` KB). Tooling: west, twister, ztest, native_sim, BabbleSim.

## FreeRTOS + STM32Cube
- FreeRTOS kernel V11.3.3 (2026-10-29), MIT; LTS 202604-LTS (tag 202604.01-LTS, LTS to 2028-04-30); previous LTS 202406 lapsed 2026-06-30.
- STM32CubeF4 v1.28.3, STM32CubeH7 v1.13.0: HAL BSD-3-Clause, CMSIS Apache-2.0, FreeRTOS MIT (bundled via stm32-mw-freertos), FatFs BSD-3-Clause, **STM32_USB_Device_Library under SLA0044**.
- LVGL 9.6.0 (MIT) with `LV_OS_FREERTOS`; `lv_st7796` driver needs two user callbacks. RadioLib 7.8.1 (MIT, CC1101 module, C++ HAL subclass). PN532: Adafruit (BSD) and Seeed (BSD-3-Clause) libraries, Arduino-style. MCUboot v2.4.0 (Apache-2.0) lists no FreeRTOS/bare-metal port.
- Flipper Zero firmware: GPL-3.0, FreeRTOS kernel as a submodule, wrapped by its Furi layer; MCU STM32WB.

## Licence findings (interpretation, not legal advice)
- FSF licence list (fetched 2026-11-01): Apache-2.0 compatible with GPLv3; Expat (MIT) and modified BSD GPL-compatible. So the permissive set can be combined into a GPL-3.0-or-later work with notices retained.
- **SLA0052 Rev3 (third-party copy)** clause 4: use "solely and exclusively in combination with" an ST NFC/UHF IC. Clause 5: "No use, reproduction or redistribution of this software package may be done in any manner that would subject this software package to any Open Source Terms" (definition names GPL, EPL, Apache, BSD, MIT). Clause 10: other use voids the licence. **SLA0044 Rev6** (ST USB Device library, from ST's GitHub) has the same pattern. Interpretation: neither can be combined into a distributed GPL-3.0 binary; clause 4 also conflicts with GPLv3 §10 no-further-restrictions. Options: independent driver from the datasheet, separate terms from ST, or a user-supplied download. A search snippet claims X-CUBE-NFC6's additional terms also bar open source (unverified).
- Zephyr's tree includes some GPL-2.0-only files (FUSE header, scripts); keep them out of the build.

## Recommendation (agent)
Zephyr 4.5.0 (to 4.6 LTS later) because most platform pieces are in tree; FreeRTOS + Cube only if footprint or an existing Cube codebase demands it. De-risk: build the LVGL sample on both boards; prove a custom H743 `usbotg_hs` node and dual USB; prove PN532 LSB-first SPI through per-device `spi_config`.

## Unknowns
Measured RAM/flash on F429/H743; dual-UDC support; TinyUSB on these parts; PB14/PB15 as OTG_HS-in-FS in a Zephyr node; one ESP32-S3 image doing AT Wi-Fi and HCI-UART BLE; F4 SD 4-bit on a custom board; verbatim SLA0052 from st.com; STSW-ST25R-ZEP licence; X-CUBE-NFC6 current licence; MCUboot on FreeRTOS; other open-source STM32 handhelds; Zephyr CI details; a legal opinion.
