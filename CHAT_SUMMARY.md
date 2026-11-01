# Project log: summary of the planning sessions

Summary of the working sessions (31 Oct to 1 Nov 2026) in which this project was planned with Claude. It records what was decided by the project owner, what was proposed, what was researched, and what is still open. Nothing has been built or tested. Status labels follow the documents: CONFIRMED (decided by the owner), PROPOSED (a recommendation), OPEN.

## 1. Starting point
A long brief described "Synnefo Handheld": a modular, portable electronics and authorised security-research device offering Flipper-Zero-style capabilities on an independent platform (own firmware, own module standard), with a future Linux compute module. The first task was a requirements traceability matrix, risk review, MCU comparison, a prototype route without a custom PCB, an SMIS connector draft and a power budget, then a list of decisions needed before a bill of materials.

## 2. Decisions by the project owner (CONFIRMED)
| Decision | Detail |
|---|---|
| Computing | MCU-only V1 with a reserved, unpopulated Linux connector |
| Display | up to 3.5", ST7796-class controller, 320×480, SPI first; buttons only (no touch) |
| Modules | 8 ports: 3 internal (2 SPI, 1 I²C), 3 top external SPI, 2 side external (1 I²C, 1 UART), plus two 2×10 GPIO headers |
| MCU | commit to both STM32H743IIT6 (preferred) and STM32F429ZIT6 (fallback) via a swappable core module |
| Sourcing | every part must come from Indian sellers with Indian stock; DigiKey/Mouser India and Tanotis count as imports; a part may be replaced only after it is shown to be import-only ("not found" is not enough) |
| NFC | design both a PN532 module (buildable now) and an ST25R3916 module (blocked by sourcing) |
| Process | prefer Indian-sourced parts; plan both rather than compromise; keep the licence open source and label the project under development |

## 3. What was produced (see the numbered documents)
- `01` requirements matrix and decision log; `02` pin maps solved and checked by script for both MCUs; `03` core-module architecture; `04`/`05` Indian sourcing and compatibility; `06` NFC modules; `07` regulatory research; `08` SMIS v0.2; `09` power architecture; `firmware/board/` generated pin headers; `tools/` solver and checker; `research/` condensed agent reports.

## 4. Key findings
- **MCU:** the STM32H743 was not found in confirmed Indian stock (boards and chips listed were out of stock; one bare chip listing looked doubtful). The F429ZIT6 is listed by Indian sellers (authenticity unverified). Both pin maps fit the full V1 signal list with the ID lines added (H743 36 spare pins, F429 10).
- **Parts in Indian stock and compatible with caveats:** ESP32-S3 module, CC1101 (868 MHz variant), RDM6300, TSOP1738 (needs 5 V or another variant), ST7796S display, PCA9535 expander, USB-C connector, tact switches.
- **No Indian source found:** ST25R3916, per-port current-limited switches with fault flag (at confirmed stock), 1-wire ID EEPROMs, 0.8 mm board-to-board connectors, genuine JST SH 1.0 mm.
- **Design changes forced by research:** MT3608 and AP2112K rejected; JST SH replaced by a 10-pin 2.54 mm keyed box header for all ports; two-wire module ID with a 24-series EEPROM (per-port data and clock lines); discrete per-port protection; two 3.3 V bucks; USB-C CC-aware charger limit.
- **NFC differences that affect the system:** PN532 uses SPI mode 0, LSB first, active-low IRQ; ST25R3916 uses SPI mode 1, active-high IRQ and has no reset pin; the SPI layer must reconfigure per transaction.
- **Regulatory research (not legal advice):** no official Indian source names the Flipper Zero; jamming equipment is prohibited under the Telecommunications Act 2023; equipment type approval is required to import, sell or use wireless devices; licence-exempt sub-GHz limits (865–868 MHz and 433 MHz) bind the radio design; BIS, MTCTE and e-waste applicability to a modular handheld is unresolved.

## 5. Corrections made along the way
- An early statement that the BQ2407x charger family was import-only was too strong; the BQ24075 is listed at Evelta (stock ambiguous).
- An agent's "GSR 680(E)" for 433 MHz (secondary source) was replaced by G.S.R. 347(E), which another agent read directly.
- The pin-count estimate fell from about 110 to 89 when buttons and port controls moved onto I²C expanders, then rose to 97 when the two-wire ID lines were added.
- The very first ST datasheet downloads failed; pin data came from ST's open GitHub pin database instead.

## 6. Open items
| Item | Needed |
|---|---|
| H743 supply | written quotes and lead times from Indian sellers; ST authenticity proof for the F429 |
| SMIS | decision: accept the 3.3 V-only ID phase (SMIS v0.2 §6) |
| ST25R3916 | an Indian source, and nine ST documents that could not be read (current datasheets, antenna/layout notes, NFC08A1 schematic, X-CUBE-NFC6 licence) |
| PN532 | buy one V3 board and measure voltages, DIP mapping and current |
| Power | confirm Evelta stock; read the non-Q1 TPS61088 and PCA9555/TCA9535 datasheets; cell datasheet, polarity and BIS number |
| Regulatory | lawyer review of the 13 questions; Gazette texts for 13.56 MHz, 5 GHz and the 2026 possession rules |
| Next work | firmware architecture and RTOS decision (Zephyr vs FreeRTOS), prototype plan without a custom PCB, KiCad skeleton and PN532 adapter board, then the first bill of materials |

## 7. Repository
Published as a public repository named "Flip my flipper" under Apache-2.0 and marked under development. The ST pin-data clone and derived pin dumps are not included (third-party BSD-3 data); `tools/README.md` explains how to regenerate them.
