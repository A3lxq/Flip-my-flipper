# Firmware architecture v0.1

Status: PROPOSED draft, written before any firmware exists. The RTOS decision is recorded in §14 and stays OPEN until you accept it. Hardware inputs: `08-smis-v0.2.md`, `09-power-architecture.md`, `02-pin-maps.md`, `06-nfc-modules.md`, `07-india-regulatory.md`. Numbers in memory tables are placeholders to be measured, not facts.

## 1. Goals and constraints

| ID | Requirement | Source |
|---|---|---|
| F1 | One application tree runs on **both** STM32F429ZIT6 (about 256 KB RAM) and STM32H743IIT6 (about 1 MB RAM); the F429 sets the feature floor | R18 |
| F2 | Applications use a documented hardware API, never raw pins | brief §16 |
| F3 | Modules are discovered by descriptor and bound to drivers by `driver ID` (SMIS §4, §5) | R21 |
| F4 | Shared SPI bus with per-transaction mode, bit order and clock | `06-nfc-modules.md` §2 |
| F5 | All radio transmission passes one policy gate: region profile, band, power cap, duty cycle; receive-only by default; no jamming | R20 |
| F6 | Power manager enforces port and total budgets, load shedding, ship mode | `09-` §8 |
| F7 | LVGL UI with buttons only, partial-frame rendering | R13, R13b |
| F8 | FAT on microSD, settings in flash | brief §4 |
| F9 | Secure update with recovery; never brick on a failed flash | brief §21 |
| F10 | Host-testable logic (parsers, state machines, policy) | brief §20 |
| F11 | Licence: GPL-3.0-or-later project; every dependency must be compatible (see §13) | repo licence |

## 2. Layers

```
+--------------------------------------------------------------+
| Applications  (Sub-GHz, NFC, RFID, IR, GPIO, Wi-Fi/BLE tools) |  use only the service APIs below
+--------------------------------------------------------------+
| UI service (LVGL)  | Settings | Launcher | Module dashboard    |
+--------------------------------------------------------------+
| Services: module manager | power manager | radio policy gate  |
|           storage | usb | logging | update | event bus        |
+--------------------------------------------------------------+
| Module drivers: cc1101 | pn532 | st25r3916 | rdm6300 | ir |...|  (registered by driver ID)
+--------------------------------------------------------------+
| Platform services: SPI arbiter | I2C | bit-bang ID I2C | UART |
|                    GPIO/EXTI | PWM | ADC | flash | SD         |
+--------------------------------------------------------------+
| OSAL (threads, queues, mutexes, timers, time)                 |
+--------------------------------------------------------------+
| RTOS + vendor HAL | board support (firmware/board/pins_*.h)   |
+--------------------------------------------------------------+
```

Rule: a layer calls only the layer below. Applications never include module drivers directly; they ask the module manager for a capability (for example `nfc_reader`) and get a driver handle.

## 3. Repository layout (planned)

```
firmware/
  app/          applications
  ui/           LVGL screens, input mapping
  services/     module_manager, power_manager, radio_policy, storage, usb, logging, update, events
  drivers/      module drivers, one directory each (cc1101, pn532, st25r3916, ...)
  platform/     spi_arbiter, i2c, idbus (bit-bang), uart, gpio, pwm, adc, flash
  osal/         thin RTOS wrapper
  board/        generated pin headers (exists), per-MCU clock/peripheral config
  tests/        host unit tests; hardware-in-loop scripts
  third_party/  vendored libraries with licence files
```

## 4. Threads (PROPOSED)

| Thread | Priority | Role |
|---|---|---|
| `evt` / event dispatcher | high | receives ISR-posted events (EXTI, UART, USB), forwards to owners; ISRs only post |
| `power` | high | polls charger/gauge/INA219, enforces budgets, shutdown thresholds |
| `radio_<port>` | medium | one worker per active radio module; talks through the SPI arbiter |
| `modmgr` | medium | port state machines, ID reads, driver start/stop |
| `ui` | medium | LVGL tick, input, rendering |
| `usb`, `storage`, `log` | low | services |
Interrupt rule: no SPI or file I/O in an ISR; an ISR posts an event with the port number and a timestamp.

## 5. Module manager

- One state machine per port with the states of SMIS §5: `OFF → ID → VERIFIED → ON`, `FAULT` from any state, `EJECTING` on user request.
- Descriptor parser: magic, version, CRC-16, class match, field range checks; pure C with no hardware calls so it can be unit-tested on the host.
- Driver registry: static table of `{driver_id, class, ops}` built at compile time. A descriptor whose `driver ID` is not registered yields "unsupported", never a guess.
- Driver ops:
  ```c
  struct module_driver_ops {
      int  (*probe)(port_t *p, const smis_desc_t *d);   /* check chip identity */
      int  (*init)(port_t *p);
      void (*irq)(port_t *p, uint32_t ts);              /* called from the module's thread */
      int  (*deinit)(port_t *p);
      const void *api;                                  /* class-specific vtable: nfc, subghz, ... */
      uint32_t (*capabilities)(port_t *p);
  };
  ```
- Class APIs: `nfc_driver_t` as in `06-nfc-modules.md` §6; `subghz_driver_t` (rx, tx through the policy gate, set frequency/modulation); `rfid125_driver_t`; `ir_driver_t`.

## 6. SPI arbiter

- One mutex per physical SPI bus; one transaction at a time.
- Each transaction carries its own configuration:
  ```c
  struct spi_xfer_cfg { uint8_t mode; bool lsb_first; uint32_t hz; gpio_t cs; };
  ```
  taken from the module descriptor (CC1101 mode 0 MSB, PN532 mode 0 LSB, ST25R3916 mode 1 MSB). The arbiter reprograms the SPI peripheral only when the configuration differs from the last one used.
- LSB-first: use the peripheral's LSB-first bit where available, otherwise bit-reverse in software; verified at bring-up.
- CS lines are GPIOs owned by the arbiter. Maximum clock per module is the descriptor's `spi_max_khz`, never above the connector/cable limit.
- DMA for transfers above a threshold; polling below (decision after measurement).
- The display has its own SPI bus (SPI1 in the pin maps) so UI refresh never waits on module traffic.

## 7. Module ID bus

Bit-banged two-wire read of the 24-series EEPROM on each port (per-port `IDD`/`IDC`, open-drain, never driven high into an unpowered module). Runs from `modmgr` under a bus mutex at 100 kHz or slower. Pure bit-bang code with an injectable pin interface so it can be tested on the host.

## 8. Radio policy gate

Every transmit path (sub-GHz, NFC field, Wi-Fi/BLE transmit features, IR) calls:

```c
policy_result_t policy_check_tx(const tx_request_t *r);   /* band, freq, power, duty, user-confirmed */
```

Inputs from the region profile (default **IN**):
- Allowed sub-GHz transmit bands: 865–868 MHz (power cap and duty cycle by class, e.g. 25 mW e.r.p. and 1 % for the non-specific class) and 433.05–434.79 MHz (10 mW e.r.p., 10 % duty cycle); nothing else.
- NFC/LF field strength caps once the Gazette values are confirmed.
- Receive-only by default; transmit/replay requires an explicit user action and is logged (timestamp, band, duration).
- Duty-cycle accounting per band over a sliding window; a request that would exceed it is refused.
- No jamming/blocking function exists in any driver API (no continuous-carrier-over-band sweeps, no wideband noise modes).
- Profile tables are data, versioned, and checked for integrity; the radio drivers refuse to start without a valid profile.

Limits are taken from `07-india-regulatory.md` and are **unverified against the Gazette**; they are software caps, not a compliance claim. Custom firmware can bypass them; liability is a lawyer question.

## 9. Power manager

Implements `09-power-architecture.md` §8: reads MAX17048 (voltage, SOC, ALRT), BQ24075 PGOOD/CHG, INA219 per-port currents (alert wire-OR to one EXTI), and the CC voltages (ADC) to select the input current limit (USB500 default; resistor-set limit when a 1.5 A or 3 A source is advertised). Enforces port and total budgets, refuses new ports that exceed them, sheds loads in order (transmit features, 5V_P ports, then warns), enters ship mode through SYSOFF below the shutdown threshold.

## 10. UI

- LVGL with partial rendering. A full 320×480 RGB565 frame is 307,200 bytes, which does not fit the F429's RAM; use one or two partial buffers of about 1/10 of the screen (about 30 KB each, placeholder) on the F429, larger on the H743.
- Input: 8 buttons on a PCA9535 (INT wakes the MCU); debounce in the input service; long-press and combos mapped in one table.
- Screens: launcher, module dashboard (ports, state, current), per-app screens, settings (region, brightness, sound), diagnostics.
- Display driver: ST7796S over SPI, RGB565; if the chosen RTOS lacks a driver, a small custom one (initialisation sequence from the ST7796S spec).

## 11. Storage and settings

- microSD over 4-bit SDIO/SDMMC with a FAT filesystem; capture files in an open documented format (to be defined; no assumption of compatibility with other devices' formats).
- Settings and calibration in internal flash with wear levelling; schema-versioned.

## 12. Boot, update, recovery

- Two-stage: a small immutable bootloader plus application slots. Images are signed; the bootloader verifies before jumping. Recovery mode (held button on boot) can reflash from SD or USB. A failed image never replaces the last good one (A/B slots or a swap-and-confirm scheme). Candidate bootloaders are in the research report; decision pending.
- USB: CDC console and MSC; DFU/update path through the bootloader. The second USB controller (full-speed on PB14/PB15) is reserved for the Linux link.
- Linux link: a framed, versioned, authenticated protocol over UART/USB, designed later; V1 runs without it.

## 13. Memory and CPU budget (placeholders)

| Item | F429 (about 256 KB RAM) | H743 |
|---|---|---|
| RTOS + stacks | to measure | to measure |
| LVGL buffers and heap | about 60 KB (two partial buffers) | larger |
| USB, FATFS, SD buffers | to measure | to measure |
| Module driver buffers (FIFO, frames) | to measure | to measure |
Rule: the F429 build must link and run within its RAM with all V1 features; an H743 build must not require features the F429 cannot run.

## 14. RTOS decision record

**Status: PROPOSED recommendation, not accepted.** Evidence: `research/11-zephyr-vs-freertos.md` (checked 2026-11-01; nothing was built or measured; ST's site was unreachable so ST licence texts come from ST's GitHub repositories and third-party copies).

**Recommendation: Zephyr 4.5.0** (released 2026-10-28), moving to the next LTS (4.6, planned April 2027) when it ships. FreeRTOS 11.3.x with STM32Cube is the alternative.

| Need | Zephyr 4.5.0 | FreeRTOS + STM32Cube |
|---|---|---|
| Same app on F429 and H743 | boards `nucleo_f429zi`, `nucleo_h743zi` in tree; shared app code with per-board overlays | Cube HAL differs per series; abstraction is ours |
| SPI per-transaction mode, LSB-first, clock | supported in `spi_stm32.c` (reconfigures when the config differs) | possible in HAL/LL; code is ours |
| I²C, bit-banged I²C, UART+DMA, EXTI | in tree | HAL; bit-bang is ours |
| SD (F4 SDIO / H7 SDMMC), FAT | in tree (F4 driver not run on an F4 board in tree) | HAL SD + FatFs |
| USB CDC / MSC | in tree | ST USB library is SLA0044 (blocked, see below); TinyUSB (MIT) unverified on these parts |
| Second USB (HS in FS) | F429 supported; **H743 needs a custom devicetree node**; two controllers in one image unverified | unknown |
| ST7796S display | driver in tree (`display_st7796s.c`) | LVGL driver needs two SPI callbacks |
| LVGL 9, buttons | LVGL 9.6.0 module + `gpio-keys` | LVGL 9.6.0 with `LV_OS_FREERTOS` |
| Settings, bootloader/DFU, power management | NVS/settings, MCUboot, `subsys/pm` | assembled by us; MCUboot lists no FreeRTOS port |
| CC1101 | community module only | RadioLib (MIT) with a HAL port |
| PN532 | none | Adafruit/Seeed libraries (BSD, Arduino-style) to port |
| ST25R3916 | immature community modules | no driver without RFAL |
| ESP32-S3 over UART | in-tree `esp_at` Wi-Fi driver; BLE HCI-UART partial | AT client to write |
| Host tests | ztest, twister, `native_sim` | DIY |
| Footprint | not found for either (LVGL sample floors: about 250 KB flash, 32 KB RAM) | not found |

**Licence findings (not legal advice):**
- Permissive components (Zephyr Apache-2.0, FreeRTOS MIT, Cube HAL BSD-3, CMSIS Apache-2.0, TinyUSB MIT, LVGL MIT, RadioLib MIT, MCUboot Apache-2.0, PN532 libraries BSD) can be combined into a GPL-3.0-or-later work according to the FSF's licence list.
- **ST's SLA0044 (USB Device library) and SLA0052 (RFAL) cannot go into a distributed GPL firmware.** Clause 5 of both forbids use "that would subject this software package to any Open Source Terms", which names GPL; clause 4 also limits use to ST silicon, which conflicts with GPL's no-further-restrictions rule. Use Zephyr's USB stack or TinyUSB, and write an independent ST25R3916 driver from the datasheet (or obtain separate terms from ST). The SLA0052 text was read from a third-party copy; confirm it against ST's own before relying on it.
- Zephyr's tree contains some GPL-2.0-only files (for example a FUSE header and scripts); make sure they stay out of the build.

**Risks of choosing Zephyr:** custom `usbotg_hs` node for the H743 and unverified dual-USB; no driver for CC1101, PN532 or ST25R3916 (community modules small or unvalidated); LTS3 (3.7) is old and LTS4 does not exist yet, so plan an upgrade in about six months; tight RAM on the F429; west/Kconfig/devicetree learning curve.
**Risks of choosing FreeRTOS:** everything above the kernel is ours to assemble (SD/FAT glue, USB, bootloader, settings, power management, logging, console, test harness); ST's USB library is blocked for GPL; Cube HAL trees differ between F4 and H7. Precedent: the Flipper Zero firmware (GPL-3.0) uses FreeRTOS, on a different MCU class.

**Alternatives assessed (2026-11-02):** ten further options were researched (`research/12-rtos-alternatives.md`, `11-os-options-and-linux-architecture.md`). Apache NuttX is the runner-up on driver coverage (in-tree CC1101, PN532, ST7796, MCUboot); FreeRTOS + Cube (HAL/LL only) is the runner-up on licensing simplicity. Zephyr remains the recommendation. ChibiOS's kernel is GPL-3.0-only; STM32duino brings ST-licensed USB code; Mbed OS is end of life. No option has a usable ST25R3916 driver.

**De-risk first (before accepting):**
1. Build the Zephyr LVGL sample for `nucleo_f429zi` and `nucleo_h743zi` and record real RAM/flash.
2. Prove a custom `usbotg_hs` node on the H743 and two USB controllers in one image.
3. Prove PN532 LSB-first SPI through a per-device `spi_config` on a shared bus.
If these fail, fall back to FreeRTOS + Cube with TinyUSB.

**Testing on both MCUs:** host unit tests for the module manager, state machines, descriptor parser, power manager and the radio policy (with fake time and mocked SPI/GPIO); hardware-in-the-loop on one F429 and one H743 board over SWD with a USB-serial pass/fail and a logic analyser for SPI mode/bit order/clock; per-peripheral checks (SPI loopback, SD/FAT stress, USB enumeration, EXTI polarity, bootloader update/rollback/power loss); bench-test the region lock and duty cycle into a dummy load before any air transmission. Run the same list on both MCUs.

## 15. Open items

1. Accept the RTOS recommendation (§14) after the de-risk builds; bootloader choice (MCUboot with Zephyr).
2. **ST25R3916 driver:** ST's RFAL (SLA0052) and ST's USB library (SLA0044) cannot be combined into a distributed GPL-3.0 binary (clause 5, see §14). Write an independent driver from the datasheet or seek separate terms from ST. Needs legal review. Variant A (PN532) drivers are BSD and fine.
3. Capture file format; settings schema; log format.
4. SPI DMA threshold; display refresh strategy.
5. Linux link protocol (later).
6. Region profile data format and update path.
7. Measure RAM/flash on the F429 early (first prototype milestone).
