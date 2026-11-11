# De-risk results (build level, 2026-11-02)

## 1. LVGL footprint (Zephyr's LVGL sample + ST7796S over SPI, shell and logging on)

`CONFIG_LV_Z_BITS_PER_PIXEL=16`, `CONFIG_LV_Z_VDB_SIZE` as shown (percent of the 320x480 screen per buffer); LVGL memory pool 16 KB (sample default). Numbers are from the linker's memory report.

| Board | Draw buffer | Flash used | RAM used | Result |
|---|---|---|---|---|
| nucleo_f429zi (192 KB RAM region) | 1 x 10 % (30,720 B) | 381,636 B (18.2 % of 2 MB) | 65,600 B (33.4 %) | builds |
| nucleo_f429zi | 2 x 10 % | 381,668 B | 96,320 B (49.0 %) | builds |
| nucleo_f429zi | full frame (307,200 B) | n/a | n/a | **fails: RAM overflowed by 145,472 bytes** |
| nucleo_h743zi (512 KB RAM region) | 1 x 10 % | 386,264 B (18.4 %) | 65,664 B (12.5 %) | builds |
| nucleo_h743zi | full frame | 386,264 B | 342,144 B (65.3 %) | builds |

Meaning: a partial-frame strategy is required on the F429 and confirmed to fit with room; a full frame buffer fits only on the H743. This is the LVGL sample, not the product, so USB, FAT, SD, the ESP32 link and module drivers still have to fit in the remainder (about 126 KB of the F429's 192 KB with one buffer, about 96 KB with two). The F429's 64 KB CCM is not counted (the CPU can use it, DMA cannot).

## 2. Two USB device controllers in one image (`usb2`)

Two independent USB device contexts (`usbd_fs` on OTG FS, `usbd_hs` on OTG HS in full-speed mode on PB14/PB15), each with its own CDC-ACM serial port, using Zephyr's new USB device stack.

| Board | Result | Flash | RAM |
|---|---|---|---|
| nucleo_f429zi | builds (OTG HS node already in the SoC dtsi) | 62,908 B | 22,360 B |
| nucleo_h743zi | builds with a custom `usbotg_hs` node (the H743 dtsi defines only `usbotg_fs`) | 67,756 B | 23,000 B |

Checks done: the node values (base 0x40040000, interrupts 74/75/77, clock bit AHB1ENR 25) match ST's `stm32h743xx.h`; the linked H743 image contains two UDC instances (`udc217_*`, `udc221_*`); Zephyr's `udc_stm32.c` states it supports an OTGHS and an OTGFS controller in one build. **Not verified:** enumeration on real hardware, behaviour of the embedded FS PHY on the OTG HS port, and whether the HAL's shared PCD code coexists at runtime.

## 3. Shared SPI bus with per-device settings (`spi3`)

PN532 (mode 0, LSB first, 1 MHz, IRQ active low), CC1101 (mode 0, MSB, 6.5 MHz, IRQ active high), ST25R3916 (mode 1, MSB, 5 MHz, IRQ active high) on one SPI2 bus with their own chip selects, each with its own `struct spi_config` from the devicetree.

| Board | Result | Flash | RAM |
|---|---|---|---|
| nucleo_f429zi | builds | 31,516 B | 7,040 B |
| nucleo_h743zi | builds | 35,464 B | 7,104 B |

Checks done: compile-time assertions on the devicetree properties (a negative test removing the PN532 LSB-first property fails the build as intended); the compiled `spi_config` structs read from the F429 ELF are PN532 operation `0x0110` / 1,000,000 Hz, CC1101 `0x0100` / 6,500,000 Hz, ST25R3916 `0x0104` / 5,000,000 Hz (0x100 = 8-bit word, 0x10 = LSB first, 0x04 = clock phase 1); `spi_stm32_configure()` (drivers/spi/spi_stm32.c) sets clock polarity, phase, bit order and the baud prescaler for each new config.
**Pitfall found:** the driver skips reconfiguration when the `struct spi_config` pointer equals the last one used (`spi_context_configured()` compares pointers, not contents). Keep one config struct per device and never modify one in place.
**Not verified:** actual waveforms and LSB-first behaviour on the silicon, the real SPI clock (quantised to a prescaler division of the peripheral clock, not measured), the Nucleo uses different pins from our maps for some signals.

## 4. Re-verification and the NUCLEO-H753ZI (2026-11-11)

All builds above were rebuilt from the committed sources (copied to a path without spaces) on 2026-11-11 and gave **identical** flash and RAM numbers, including the F429 full-frame overflow.
The same three test applications also build for **`nucleo_h753zi`** (STM32H753, the H743 line plus crypto, and the H7 Nucleo board that Hubtronics listed in stock on 2026-11-11), using copies of the H743 overlays (`boards/nucleo_h753zi.overlay`):

| App | Flash | RAM |
|---|---|---|
| LVGL + ST7796S, 10 % partial buffer | 385,896 B (18.4 %) | 65,664 B (12.5 % of 512 KB) |
| two USB device controllers | 67,424 B (3.2 %) | 23,000 B (4.4 %) |
| shared SPI, per-device settings | 35,132 B (1.7 %) | 7,104 B (1.4 %) |

Build level only; nothing has run on hardware.

## What this does and does not change
Build-level risk for all three items is retired; the remaining risks need hardware: dual-USB enumeration, SPI waveforms and the display panel's real init values. See `10-firmware-architecture.md` §14.
