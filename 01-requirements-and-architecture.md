# Synnefo Handheld: Phase 0 Architecture Review

Status labels: CONFIRMED (user decided), PROPOSED (my recommendation), OPEN (needs decision/research), VALIDATED (tested), BLOCKED.
Nothing here is VALIDATED. All figures are planning assumptions and must be checked against datasheets and measured on hardware. No part numbers, prices or stock levels are asserted; none were looked up.

## 1. Requirements traceability matrix

| ID | Requirement | Source | Status | Verification |
|---|---|---|---|---|
| R1 | Modular base device with detachable expansion units | Brief §6 | CONFIRMED | Module swaps without mainboard changes |
| R2 | Both 2.54 mm GPIO headers and dedicated plug-in connectors | §6 | CONFIRMED | Inspection; pinout doc published |
| R3 | Both 3.3 V and 5 V expansion power, regulated and protected | §6, §12 | CONFIRMED | Rail accuracy, ripple, current-limit trip tests |
| R4 | Automatic module detection where supported | §6, §13 | CONFIRMED | Official module enumerates, correct driver bound |
| R5 | Manual configuration of generic modules, validated before power-up | §13 | CONFIRMED | Invalid config is rejected, rail stays off |
| R6 | Users can solder custom circuits or plug in modules | §1, §11 | CONFIRMED | Prototype pads/headers exist, limits documented |
| R7 | Own firmware, driver framework, module manager | §2, §16 | CONFIRMED (direction) | Module added by driver only, no app change |
| R8 | V1 is MCU-only; Linux compute interface reserved (connector footprint and signals, unpopulated) | §15; user decision 2026-10-31 | CONFIRMED | Connector and protocol spec exist; V1 boots and works with it unpopulated |
| R9 | Lawful use only; no jamming; region-aware radio limits, receive-only/TX-off defaults | §3, §20 | CONFIRMED | Firmware region lock tests |
| R10 | Documented electrical limits on every port | §20 | CONFIRMED | SMIS document complete |
| R11 | Firmware update and recovery path | §21 | CONFIRMED (V1 goal) | Recover from a bad flash |
| R12 | V1 feature scope (which radios) | §18-19 | OPEN | See §3 |
| R13 | Display: 3.5" max, 320×480, ST7796-class controller, no touch; SPI for prototype, parallel/FMC kept as later option (exact panel part TBD) | user decision 2026-10-31 | CONFIRMED (size limit, controller class, no touch) / OPEN (exact module, SPI vs parallel final) | Datasheet check; refresh and tearing test |
| R13b | Input is buttons only (d-pad plus keys), no touch | user decision 2026-10-31 | CONFIRMED | Button debounce and wake tests |
| R14 | Both internal and external modules (external detachable bays plus internal module slots) | user decision 2026-10-31 | CONFIRMED | Internal and external module both enumerate; mechanical fit check |
| R14b | 8 module ports in total (internal and external, split OPEN), plus the 2×10 GPIO headers; per-port ID line and switched power | user decision 2026-10-31 | CONFIRMED (count and split: 3 internal [2 SM-S, 1 SM-I], 3 top external SM-S, 2 side external [1 SM-I, 1 SM-U]) | Port count on board; per-port enable and ID test; power manager enforces budget |
| R18 | Commit to both STM32H743IIT6 (preferred) and STM32F429ZIT6 (fallback); same carrier, swappable MCU core module (architecture PROPOSED, see 03-core-module.md) | user decision 2026-11-01 | CONFIRMED (both chips) / PROPOSED (core-module approach) | Both cores boot the same firmware tree and pass the same module tests |
| R19 | Design both NFC modules: Variant A (PN532, buildable from Indian stock) and Variant B (ST25R3916, blocked by India-only sourcing until a source is found); draft in 06-nfc-modules.md | user decision 2026-11-01 | CONFIRMED (design both) / OPEN (Variant B sourcing) | Both enumerate as nfc_reader and pass the same bring-up tests |
| R20 | Regulatory guardrails: no jamming; sub-GHz transmit locked to 865-868 MHz and 433.05-434.79 MHz within power and duty-cycle limits; receive-only default; India profile default; ETA/BIS/e-waste checked before any sale (details and open questions in 07-india-regulatory.md) | brief §3, §20; research 2026-11-01 | PROPOSED | Firmware region-lock and duty-cycle tests; lawyer review |
| R21 | SMIS v0.2: one 10-contact keyed box header on all ports; two-wire module ID (per-port IDD/IDC, 24-series EEPROM); separate 3V3_P/5V_P per port; discrete per-port protection; no hot-plug in V1 (08-smis-v0.2.md) | research 2026-11-01 | PROPOSED | Descriptor read on 8 ports; port-off and fault tests |
| R22 | Power architecture v1: BQ24075 charger, MAX17048 gauge, two 3.3 V bucks, 5 V boost (1.5 A budget), USB-C sink (09-power-architecture.md) | research 2026-11-01 | PROPOSED | Rail, charger and brown-out tests |
| R23 | Firmware architecture v0.1 (layers, module manager, SPI arbiter, radio policy gate, power manager) and **Zephyr 4.5.0 as the working RTOS**; build-level de-risk done 2026-11-02, hardware tests pending (10-firmware-architecture.md, firmware/zephyr/) | user acceptance 2026-11-02 | CONFIRMED (Zephyr 4.5.0 as working RTOS) / OPEN (hardware verification) | Dual-USB enumeration, SPI waveforms, panel init values, real RAM budget on hardware |
| R24 | Linux module stays optional and pluggable (hybrid MCU + Linux, Flipper One-style division of labour); not Linux-only (11-os-options-and-linux-architecture.md) | research 2026-11-02 | PROPOSED | Real-time and sourcing checks before choosing a module |
| R25 | KiCad skeletons for both NFC modules: PN532 adapter (schematic + placement-only PCB) and ST25R3916 module (block-level schematic), checked with KiCad 10.0.8 (hardware/kicad/) | user request 2026-11-02 | CONFIRMED (skeletons made) / OPEN (breakout pinout, ST documents, routing) | ERC/DRC reports in hardware/kicad/checks/; real-board measurements |
| R15 | MCU, RTOS, connectors, charger IC, regulators | §8-12 | OPEN | Decision log |
| R16 | Indian regulatory position (WPC/DoT/TEC/BIS, import) | §3 | OPEN: not researched yet | Primary-source review |

## 2. Conflicts, gaps and risks found in the brief

1. **Module ID bus does not scale (design flaw).** I²C ID EEPROMs have a few fixed addresses. Several identical connectors would collide, and a faulty module could hold a shared bus low. PROPOSED: one dedicated ID line per connector, single-wire EEPROM-class device, which also gives presence detect and keeps module power off until the descriptor is read.
2. **Two different "6-pin" connectors** (I²C+IRQ/RST and UART) share a name. Keying must prevent mis-mating or they need distinct footprints. PROPOSED: name them by class (SM-I, SM-U, SM-S), see §5.
3. **5 V is not available on the small I²C/UART connectors in the brief's pin counts.** The confirmed 5 V requirement is met on the GPIO headers and the SPI-class connector in my draft. Needs your confirmation.
4. **USB-C does too much.** Charging, device, host and possible PD role swap need CC-line handling and a power-path IC that tolerates OTG and VBUS back-feed. This is an early architecture risk, not a footnote.
5. **Display size drives MCU choice.** A 3.5" 320×480 panel over SPI is slow for full-frame updates (roughly 5 Mbit per frame at 16 bpp). A parallel/FMC or LTDC-capable path is better. STM32H563 has no LTDC, to be verified in its datasheet.
6. **The SPI allocation is a sketch.** SD card (SDMMC is preferable to SPI), display, CC1101, ST25R3916 and the expansion bus compete for pins and alternate functions. It cannot be finalized without the chosen package's pin table.
7. **LF RFID and IR need timer/comparator/ADC resources** that the allocation table doesn't reserve.
8. **Hot-plug on keyed connectors** needs load switches with controlled slew rate, and signal pins that stay high-impedance until the rail is up. This is hardware, not firmware.
9. **RF layout vs the modular bay.** RF modules on a connector have unknown antenna placement and ground return; keep-out and shielding rules belong in SMIS.
10. **Scope.** The roadmap is realistic only if V1 is limited; see §3.
11. **Regulatory.** I have not researched Indian rules yet; nothing in this file is a legal conclusion.

## 3. Proposed V1 scope (PROPOSED, not confirmed)

MCU-only mainboard; GPIO headers; SM-I and SM-S connectors; ID system with manual fallback; one official module (CC1101, receive-first, region-locked); IR; USB-C power/data; SD card; ESP32-class coprocessor optional. NFC (ST25R3916-family) and LF RFID follow as separate module boards once the interface is proven. Linux interface is reserved on the board but unpopulated.

## 4. MCU candidates (verify every row against datasheets)

| Candidate | Why | Concerns |
|---|---|---|
| STM32H743 | Cortex-M7, large RAM, many SPI/UART, SDMMC, LTDC, USB HS (per my recollection) | Larger/fine-pitch packages, higher power, harder to hand-solder; needs external radios |
| STM32H563 | Cortex-M33, TrustZone, lower power, SDMMC, USB FS | No LTDC (verify), less RAM, so display buffering is tighter |
| ESP32-S3 | Wi-Fi/BLE, cheap, good dev boards | Not a main controller for this design; suited as coprocessor only |
| STM32WB55 | Integrated BLE, the Flipper Zero's family | Small RAM/clock for a modular UI; brief says do not assume it |

PROPOSED prototype route with no custom PCB: an STM32H7 or H5 Nucleo/dev board, an SPI or parallel display breakout, a CC1101 breakout (match the frequency variant to your region), IR LED/receiver on protoboard, an SD breakout, and an ESP32-S3 dev board on UART. Build the ID line and a load-switched 5 V rail on a small protoboard before any custom PCB. Final MCU choice is OPEN until the display and pin budget are decided.

## 5. SMIS v0.1 draft (PROPOSED; all part numbers TBD)

Rules for all connectors: logic is 3.3 V only; 5 V pins are power, never signal; ID pin is always present; keyed, with a retention screw or latch; no hot-plug unless the port is marked HP and tested.

| Class | Pins | Pinout (1…n) | Role |
|---|---|---|---|
| SM-I | 6 | GND, 3V3, SDA, SCL, IRQ, ID | I²C sensors/modules |
| SM-U | 6 | GND, 3V3, TX, RX, GPIO, ID | UART modules |
| SM-S | 10 | GND, 3V3, 5V_SW, SCK, MOSI, MISO, CS, IRQ, RST, ID | SPI radios and peripherals |

The 2×10 GPIO headers carry GPIO, SPI/I²C/UART, ADC, 3V3, 5V_SW, GND, RST and IRQ; pin-level assignment is blocked on MCU selection. Exposed headers are not hot-pluggable.

Connector family (JST-SH or other): OPEN. Choose from rated current per contact, pitch, insertion life and retention, then fill in part numbers.

Descriptor: a versioned record containing the fields listed in the brief §13, plus a CRC. Unknown version or bad CRC means the module is shown as unsupported and stays unpowered.

Discovery sequence: as in the brief §13, with ID read performed while the module rail is still off.

## 6. Preliminary power budget (assumptions, all to be measured)

| Block | Typical | Peak |
|---|---|---|
| MCU + memory | 100–200 mA | 300 mA |
| Display + backlight (3.5") | 60–150 mA | 200 mA |
| ESP32-class radio | 80–120 mA | 300+ mA |
| Sub-GHz module | 15–35 mA | 40 mA |
| NFC field on | 50–150 mA | 250 mA |
| LF RFID | 50–100 mA | 150 mA |
| IR TX pulse | negligible avg | 100+ mA |

Reading: about 0.3–0.6 A typical and about 1 A peak at the battery before converter losses. A 2,500–3,500 mAh cell gives roughly 5–10 h typical, which is only an estimate. Do not publish an expansion current rating until converter limits, copper, connector rating and thermal tests are done.

## 7. Decisions needed before the first BOM

1. ~~V1 scope~~ CONFIRMED 2026-10-31: MCU-only, Linux connector reserved.
2. ~~Display size~~ CONFIRMED 2026-10-31: ≤3.5", ST7796-class, buttons only. Still open: exact panel module and SPI vs parallel.
3. ~~Internal vs external modules~~ CONFIRMED 2026-10-31: both.
4. Primary MCU part and package.
5. Charger/power-path IC, supporting USB-C role handling.
6. Connector families and part numbers.
7. Region(s) for radio variants, after the regulatory review.
8. RTOS (Zephyr vs FreeRTOS), after MCU choice.

## 8. Next actions

- Answer the question below.
- I research the Indian regulatory sources (DoT/WPC/TEC/BIS, import) and cite them, if you want.
- Then: MCU comparison with datasheet-checked pin budget, then SMIS v0.2.

## 9. MCU pin and peripheral budget (first pass)

**Source:** ST's `STM32_open_pin_data` repository (`github.com/STMicroelectronics/STM32_open_pin_data`, commit 7d1f151, dated 2026-06-29), parsed with `tools/summ.py`. Local copy in `datasheets/open_pin_data/`. This is ST's own pin database, not the datasheet PDF. The PDFs could not be downloaded (st.com connections hung). Cross-check I/O counts and alternate functions against DS12110 (H743) and DS14258 (H563) before layout. Per-pin alternate-function conflicts are NOT yet checked.

### 9.1 What each family provides

| Part (package) | I/O | RAM (KB) | Flash (KB) | SPI | I2C | USART+UART | SDMMC | USB | LTDC | ADC |
|---|---|---|---|---|---|---|---|---|---|---|
| H743VITx (LQFP100) | 82 | 864 | 2048 | 5 | 4 | 4+4 | 2 | OTG FS + HS | yes | 3 |
| H743ZITx (LQFP144) | 114 | 864 | 2048 | 6 | 4 | 4+4 | 2 | OTG FS + HS | yes | 3 |
| H743IITx (LQFP176) | 140 | 864 | 2048 | 6 | 4 | 4+4 | 2 | OTG FS + HS | yes | 3 |
| H563VITx (LQFP100) | 80 | 640 | 2048 | 5 | 4 | 6+6 | 1 | FS only | no | 2 |
| H563ZITx (LQFP144) | 112 | 640 | 2048 | 6 | 4 | 6+6 | 2 | FS only | no | 2 |
| H563IITx (LQFP176) | 140 | 640 | 2048 | 6 | 4 | 6+6 | 2 | FS only | no | 2 |

Plus LPUART (1 each), FDCAN (2), FMC (1). H743 adds QUADSPI, COMP and OPAMP; H563 adds OCTOSPI.
A full 320×480 16-bit frame is 307,200 bytes. One buffer fits both parts; two buffers (614 KB) fit only the H743's RAM.

### 9.2 Estimated pin demand (V1, SPI display, 8 ports, GPIO headers, Linux link)

| Subsystem | Pins | Notes |
|---|---|---|
| SWD (+SWO) | 3 | |
| HSE and LSE crystals | 4 | |
| USB-C (data, VBUS sense, PD/CC interrupt) | 5 | |
| Display SPI (SCK, MOSI, CS, DC, RST, backlight PWM) + MISO | 7 | |
| Buttons (d-pad 4, OK, Back, 2 keys) | 8 | wake-capable |
| SD card (SDMMC 4-bit + detect) | 7 | |
| Buzzer, vibration | 2 | |
| ESP32 link (UART, EN, BOOT, handshake) | 6 | |
| Module ports, direct: 8 ID + 8 IRQ + 5 SPI chip-selects | 21 | EN, RST, fault via expanders |
| Port expander interrupts | 2 | 2 expanders carry ~21 slow signals |
| Power (charger, gauge, boost enable, PG) | 5 | |
| Shared buses (SPI 3, I²C 4, UART 2) | 9 | |
| IR onboard (TX PWM, RX capture) | 2 | |
| GPIO headers (unique pins) | 20 | buses shared with ports |
| Linux link (UART 2, power enable, reset, present, wake) | 6 | |
| Status LEDs | 3 | |
| **Total** | **about 110** | estimate, assumptions above |

### 9.3 Result (PROPOSED)

- **100-pin parts (80 to 82 I/O): do not fit.**
- **144-pin parts (112 to 114 I/O): essentially zero headroom.** Fine for a scoped-down prototype (skip the Linux link and trim the GPIO header), not for the final board.
- **176-pin parts (140 I/O): fit with about 30 pins (roughly 25%) spare.** This is the target for the custom PCB. LQFP176 (0.5 mm pitch) needs hot-air or drag soldering; this is also where you need a custom PCB.
- **Prototype without a custom PCB:** a 144-pin Nucleo board of the chosen family (as I recall, the Nucleo-H743ZI2 and Nucleo-H563ZI use the ZI 144-pin parts: verify) plus protoboard and breakouts. Some Nucleo pins are used by the on-board debugger/Ethernet; check the board schematic first.
- **H743 vs H563:** both have enough SPI, I²C and UART instances. H743 has more RAM (double-buffered display), USB high-speed for the Linux link, and 3 ADCs. H563 has no LTDC (not needed with an SPI display), TrustZone, and probably lower power. Battery life is unmeasured and unresearched. **OPEN.** My current lean is H743 for headroom, to be re-checked after power figures are read from the datasheets.

### 9.4 Next for this section

1. Cross-check the I/O counts and power figures against the two datasheet PDFs once available.
2. Assign specific pins from the alternate-function data, flagging boot, debug and reserved-pin conflicts.
3. Fix the pin-demand estimate (the 110 is only an estimate).

## 10. Sourcing constraint: India only (user decision 2026-11-01)

**R17 (CONFIRMED):** every part must be buyable from Indian sellers with Indian stock. No imports. Mouser India and DigiKey India ship from overseas, so I treat them as imports, not as Indian sources.
**Rule for changing parts:** a part is replaced only after it has been shown that it can only be imported. Until then it stays in the design, flagged "sourcing unconfirmed".

### 10.1 STM32H7 findings (checked 2026-11-01; snapshots, not live stock)

| Item | Seller | Price (INR) | Stock |
|---|---|---|---|
| WeAct STM32H743VIT6 core board | Probots | 3,999 incl. GST | Out of stock |
| STM32H743VIT6 "DevEBox" board | Probots | 11,999 incl. GST | Out of stock |
| WeAct STM32H750VBT6 board | Electropi | 1,679 + 18% GST | Out of stock |
| NUCLEO-H563ZI | DNA Tech | 5,251 incl. GST | Out of stock |
| NUCLEO-H743ZI (older board) | Hubtronics, CompoIndia | n/a | Out of stock (CompoIndia result may be stale) |
| NUCLEO-H743ZI | IndiaMART seller | 2,900 | Listed in stock, unverified |
| Bare STM32H743ZIT6 | Prozone Engineers (IndiaMART) | 475, MOQ 500 | "In stock", but the listing names no brand and says "Made in India", so its authenticity is doubtful |

Robu and Robocraze could not be checked (HTTP 403 and 429 blocked me); Hubtronics and Tanna not checked.

### 10.2 Conclusion (PROPOSED)

- I found **no confirmed, in-stock, genuine STM32H743 chip or board from an Indian seller.** That is "not found", **not** "only importable". Sellers may be able to supply on lead time. Not enough evidence to change the MCU yet.
- **Next:** ask Indian sellers for a written quote and lead time (Probots, Hubtronics, DNA Tech, Tanna TechBiz, Robu, Robocraze), and check which STM32 parts Indian stores really stock. Only if they all say no do I propose an alternative.
- Other parts (CC1101, ST25R3916, ESP32-S3, charger and power ICs, connectors, display) are **not yet checked** for Indian sourcing.

## 11. Indian-stocked MCU candidates (checked 2026-11-01; snapshots from seller pages, not live stock)

Peripheral data below is from ST's pin database (see §9). RAM figures there may exclude the F4 CCM block, so confirm against the datasheet.

| Candidate | Package / I/O | Flash | SPI / I2C / UART+USART | Notable | Indian source found | Verdict |
|---|---|---|---|---|---|---|
| **STM32F429ZIT6** | LQFP144 / 114 | 2 MB | 6 / 3 / 4+4 | Cortex-M4F 180 MHz, LTDC, FMC, USB FS + HS (ULPI), 3 ADC | DNA Tech: ₹649 incl. GST (₹550 + GST), listed "Stock: 50", price valid to 2026-11-29, page says origin China, importer ElectroSource Pvt Ltd, manufacturer not stated. IndiaMART (Indus Technologies, Bengaluru): ₹560 excl. taxes, brand STMicroelectronics, "In Stock", 2 to 3 weeks | **Best Indian-stocked candidate.** Authenticity of grey-market stock unverified |
| STM32F429ZGT6 | LQFP144 / 114 | 1 MB | same | same family | DNA Tech: ₹1,321.60 incl. GST, out of stock | Backup only |
| STM32F407VET6 | LQFP100 / 82 | 512 KB | 3 / 3 / 4+2 | no LTDC, no FMC to speak of at 100 pins | DNA Tech: ₹1,298 incl. GST, "Stock: 2" | Too few pins for full V1 (needs about 110) |
| STM32F407VGT6 | LQFP100 / 82 | 1 MB | same | | Sunrom: ₹748, no stock | No |
| STM32F446VET6 | LQFP100 | n/a | n/a | | DNA Tech: ₹414.57, out of stock | No |
| STM32H743 (all) | 100/144/176 | 2 MB | see §9 | preferred | None with confirmed stock; bare ZIT6 on IndiaMART (MOQ 500, no brand, "Made in India") is doubtful | Keep as preferred, sourcing unconfirmed |
| STM32H563 (all) | | | | | Only NUCLEO-H563ZI, out of stock | Sourcing unconfirmed |
| 176-pin parts, any family | 140 | | | | None found | |

Boards for a no-PCB prototype: NUCLEO-F429ZI on Tanotis at ₹2,989.65 incl. GST and import duties (stock not checked; the "import duties" wording needs a question to the seller: is it held in India?) and Hubtronics (page exists, price and stock not seen). STM32F429I-DISC1 on Robozar was out of stock at ₹4,311. Robu, Robocraze, Tanna, Rhydolabz: blocked or not checked.

### 11.1 Is F429 a valid substitute for H743? (PROPOSED, not committed)

- **Not pin- or footprint-compatible.** The pin map must be redone for any change of family. Software (HAL, Zephyr, FreeRTOS) supports both.
- **Gives up:** clock (180 vs 480 MHz), RAM (about 256 KB vs 864 KB, to be confirmed), one I²C (3 vs 4), the second SDMMC (F429 has SDIO), and the flexibility of the 176-pin package.
- **Adequate for V1:** 180 MHz Cortex-M4F is well above the 64 MHz Cortex-M4 in the Flipper Zero's STM32WB55 (from memory). A partial-frame buffer is enough for the 320×480 SPI display, but a full 307 KB frame does not fit.
- **Pin budget:** 114 I/O against the roughly 110-pin demand leaves no headroom. Would need to trim the GPIO headers and Linux link, or save pins with more expanders.
- **Rule R17:** the H743 has **not** been shown to be import-only, so it is **not replaced**. The F429ZIT6 is the fallback candidate if Indian sellers cannot supply H743.

### 11.2 Next
1. Ask DNA Tech (they list an H745ZIT3 at zero stock) and other sellers for a written quote and lead time on STM32H743ZIT6 and IIT6.
2. Ask the F429ZIT6 sellers for ST authenticity proof (invoice from an authorised distributor).
3. Check Robu, Robocraze, Tanna, Hubtronics and Rhydolabz manually.

## 12. Pin maps

Draft pin maps for STM32H743IIT6 and STM32F429ZIT6 are in `02-pin-maps.md`. Both fit the full V1 signal list; the earlier estimate of about 110 pins (§9.2) was too high because buttons and port control lines move onto I²C expanders (89 MCU pins assigned in the maps).

## 13. Build on both chips

Both chips are committed (R18). The core-module architecture and generated board headers are in `03-core-module.md` and `firmware/board/`.

## 14. Remaining-part sourcing

See `04-india-sourcing.md` for the Indian-sourcing check of the CC1101, NFC, ESP32-S3, display, power and connector parts. No part has been replaced yet.

## 15. Deeper sourcing and compatibility

See `05-deep-sourcing-and-compatibility.md`. Corrections to §10/`04-india-sourcing.md`: the BQ24075 charger is listed at Evelta (stock ambiguous), so the charger is no longer 'import-only'; MT3608 and AP2112K are unsuitable for the 5 V and 3.3 V rails; the per-port load switch, buck-boost and ST25R3916 remain without an Indian source.

## 16. NFC modules

Both variants planned in full in `06-nfc-modules.md` (version 2, from primary PN532 and ST25R3916 documents). New system-level constraints found: different SPI modes per module (shared bus must reconfigure per transaction), differing IRQ polarity, and no reset pin on the ST25R3916 (descriptor fields `spi_mode`, `spi_bit_order`, `irq_polarity`, `reset_method`).

## 17. Indian regulatory research

See `07-india-regulatory.md`. Sources were partly unreadable; the document lists what is unconfirmed and 13 questions for a lawyer or lab. It is not legal advice.

## 18. SMIS v0.2 and power architecture

See `08-smis-v0.2.md` and `09-power-architecture.md`. Pin maps re-solved with the 16 extra ID lines (97 pins assigned): H743 36 spare, F429 10 spare. Decision needed: accept the 3V3-only ID phase (SMIS §6).

## 19. Firmware architecture

See `10-firmware-architecture.md`. RTOS: Zephyr 4.5.0 accepted as the working RTOS on 2026-11-02 (CONFIRMED); the three build-level de-risk checks passed (firmware/zephyr/derisk/RESULTS.md); hardware verification is still open. ST's RFAL (SLA0052) and USB library (SLA0044) cannot be used in a distributed GPL binary.

## 20. OS options and the Linux-first question

See `11-os-options-and-linux-architecture.md` and `research/12-` to `14-`. Zephyr remains the recommendation, with NuttX and FreeRTOS + Cube as runners-up. A Linux-only design is not recommended; a pluggable Linux module in a hybrid design is.

## 21. KiCad skeletons

See `hardware/kicad/README.md`: PN532 adapter (ERC 0 violations, netlist verified, placement-only PCB with no clearance violations) and a block-level ST25R3916 schematic (4 intentional ERC open items). Both are skeletons: the PN532 V3 header order and the ST25R3916 pin table/antenna design are still unverified.
