# Handoff: Flip my flipper (Synnefo Handheld)

Written 2026-11-11 for whoever picks this project up next (a person, or a new Claude Code session). Read this first, then `README.md`, then `01-requirements-and-architecture.md`.

**Status in one paragraph.** The project is a modular, portable electronics and authorised security-research handheld designed in India, with parts sourced from Indian sellers only. It is at the end of Phase 0 (requirements, architecture and feasibility). Nothing has been built, flashed or powered on. What exists is documents, a solved pin map for two candidate MCUs, a module interface standard (SMIS v0.2), a power architecture, a firmware architecture with Zephyr 4.5.0 accepted as the working RTOS, build-level firmware test applications, KiCad skeletons for two NFC modules, pinout tables and diagrams, and a lot of sourcing and regulatory research. All research was done by automated agents from web pages and datasheets and is **unverified** until checked against the primary document. Stock and prices in this repository were captured on **2026-11-01 and 2026-11-02** and are probably out of date.

Repository: https://github.com/A3lxq/Flip-my-flipper (public, GPL-3.0-or-later, marked under development). The owner's local working copy is a folder named `Hand Held PROJECT`.

---

## 1. Ground rules the owner set (do not change silently)

1. **India-only sourcing.** Every part must come from an Indian seller with Indian stock. DigiKey India, Mouser India, element14/Farnell India, Tanotis (its prices include import duties), LCSC and any overseas seller count as imports. A part may be replaced only after it is shown to be import-only; "not found" is not enough.
2. **Status labels.** Decisions are CONFIRMED (the owner decided), PROPOSED (a recommendation) or OPEN. Never turn a proposal into a decision.
3. **No invented data.** No part numbers, prices, stock, pin numbers or datasheet values that were not seen in a source. Mark unverified items.
4. **Lawful use only.** No jamming or blocking function; sub-GHz transmit locked to licence-exempt bands; receive-only by default. The regulatory notes are not legal advice.
5. **Commit and push only when the owner asks.** Scan the staged files for secrets and personal paths first.
6. The owner prefers that plans are not compromised: when asked for two variants, do both.

## 2. Decisions

CONFIRMED by the owner:

| Decision | Detail |
|---|---|
| Computing | MCU-only V1 with a reserved, unpopulated Linux connector (R8) |
| MCU | Commit to both **STM32H743IIT6** (preferred, LQFP176) and **STM32F429ZIT6** (fallback, LQFP144) behind a swappable core module (R18) |
| Display and input | up to 3.5", 320x480, ST7796-class controller, SPI first, buttons only, no touch (R13, R13b) |
| Ports | 8 module ports: 3 internal (2 SM-S SPI, 1 SM-I I2C), 3 top external SM-S, 2 side external (1 SM-I, 1 SM-U UART), plus two 2x(2x10) GPIO headers (R14, R14b) |
| NFC | Design both a PN532 module (buildable from Indian stock) and an ST25R3916 module (blocked on sourcing) (R19) |
| RTOS | **Zephyr 4.5.0 as the working RTOS** (accepted 2026-11-02), hardware verification still open (R23) |
| Licence | GPL-3.0-or-later (changed from Apache-2.0 at the owner's request); changes should come back via pull requests (`CONTRIBUTING.md`) |
| KiCad skeletons | Both NFC modules (R25) |

PROPOSED, awaiting the owner:

| Item | Detail |
|---|---|
| **3.3 V-only ID phase** | **The one decision currently waiting on the owner.** SMIS v0.2 section 6: read a module's ID EEPROM with only its 3V3_P rail on (5 V off, signal pins high-impedance). The alternative is a dedicated always-on ID rail (costs a contact and parts). |
| SMIS v0.2 (R21) | 10-contact keyed box header on every port, two-wire ID (per-port IDD/IDC, 24-series EEPROM), separate 3V3_P/5V_P switches, discrete per-port protection, no hot-plug in V1 |
| Power architecture v1 (R22) | BQ24075 charger, MAX17048 gauge, two TLV62568 3.3 V bucks, 5 V boost (TPS61023 module for the prototype, TPS61088 for a custom board), 1.5 A 5 V budget |
| Linux as a pluggable module (R24) | Hybrid MCU + Linux, Flipper One-style division of labour; not Linux-only |
| Regulatory guardrails (R20) | no jamming, sub-GHz TX limited to 865-868 MHz and 433.05-434.79 MHz within power and duty-cycle limits, India profile by default |
| Port numbering P1-P8 and module assignment | proposed in `hardware/pinouts/module-pinouts.md`, never fixed elsewhere |

Stale rows in `01-requirements-and-architecture.md`: R16 says the regulatory position is "not researched yet" (it was researched, see `07-india-regulatory.md`), and R12 and R15 are still OPEN. Update them when next editing that file.

## 3. Architecture in brief

- **MCU core module** carries the MCU, crystals and debug; one fixed connector (97 signals) goes to the carrier board; two core boards, one carrier. `03-core-module.md`, `02-pin-maps.md`, generated headers in `firmware/board/`.
- **SMIS v0.2** (`08-smis-v0.2.md`): every port uses the same 10-contact 2.54 mm box header; contacts 1, 2, 3, 9, 10 never change (GND, 3V3_P, 5V_P, IDC, IDD); contacts 4-8 depend on the class (SM-S SPI, SM-I I2C, SM-U UART).
- **Power** (`09-power-architecture.md`): single protected Li-ion cell, USB-C sink, charger with power path, two 3.3 V rails (system, IO/ports), switched 5 V rail, per-port P-FET switches with INA219 sensing.
- **Firmware** (`10-firmware-architecture.md`): layers (apps, UI, services, module drivers, platform, OS wrapper), module manager with per-port state machines, SPI arbiter that reconfigures mode, bit order and clock per transaction, radio policy gate, power manager, LVGL UI with partial-frame buffers, signed updates with recovery.
- **NFC** (`06-nfc-modules.md`): Variant A PN532 (SPI mode 0, LSB first, active-low IRQ) via an adapter board; Variant B ST25R3916 (SPI mode 1, active-high IRQ, no reset pin).
- **Linux** (`11-os-options-and-linux-architecture.md`): not recommended as the sole OS; kernel lacks CC1101, ST25R3916 and PN532-over-SPI drivers; recommended as an optional module later.

## 4. What exists (file map)

| Path | Contents |
|---|---|
| `01-requirements-and-architecture.md` | requirements matrix R1-R25 with status, decisions, risks |
| `02-pin-maps.md`, `tools/` | solved and verified pin maps for both MCUs; solver, checker, header generator |
| `03-core-module.md` | core-module architecture and the 97-signal connector table |
| `04-india-sourcing.md`, `05-deep-sourcing-and-compatibility.md` | Indian stock and datasheet compatibility of the parts |
| `06-nfc-modules.md` | both NFC modules, pins, supply, firmware, tests |
| `07-india-regulatory.md` | licence-exempt bands, type approval, BIS, TEC, e-waste, laws; 13 questions for a lawyer |
| `08-smis-v0.2.md`, `09-power-architecture.md`, `10-firmware-architecture.md`, `11-os-options-and-linux-architecture.md` | the standards and architecture documents |
| `firmware/board/` | generated per-MCU pin headers, same names on both chips |
| `firmware/zephyr/` | toolchain setup and three build-level test applications with results (`derisk/RESULTS.md`) |
| `hardware/kicad/` | KiCad projects (PN532 adapter schematic + placement-only PCB, block-level ST25R3916 schematic), shared library, generator, ERC/DRC outputs |
| `hardware/pinouts/` | module pinout tables with knowledge tags, system and SM-S connection diagrams, generator |
| `research/` | condensed research-agent reports 01-15 (not verbatim; limits in its README) |
| `CHAT_SUMMARY.md` | chronological log of decisions, findings and corrections |
| `datasheets/` | local only, git-ignored: clone of ST's open pin data (BSD-3) |

## 5. What was actually verified, and what was not

Verified by running something:
- Pin maps: solver output re-checked by `tools/verify.py` (every signal exists on its pin, no pin used twice, interrupt line numbers unique); both maps fit with 97 pins assigned (H743 36 spare, F429 10 spare).
- Generated firmware headers compile with gcc for both chips and expose identical names.
- Zephyr 4.5.0 builds (SDK 1.0.1, GCC 14.3.0): LVGL with an ST7796S, two USB device controllers in one image, and per-device SPI settings on a shared bus, all on `nucleo_f429zi` and `nucleo_h743zi`. Measured: F429 uses 381,636 B flash and 65,600 B RAM with one 10 % partial display buffer (96,320 B with two); a full 320x480 frame overflows the F429 RAM by 145,472 B and fits the H743.
- KiCad 10.0.8: adapter schematic 0 ERC violations with the intended netlist; adapter PCB no clearance, courtyard or edge violations (23 unrouted nets expected); ST25R3916 skeleton 4 ERC errors, all the intentional open pins.

**Never run on hardware:** dual-USB enumeration, SPI waveforms and LSB-first behaviour, the ST7796S panel's real init values (the gamma tables in the test overlays are placeholders), the real RAM budget with USB/FAT/SD/ESP32/module drivers, every power rail, the charger, the NFC modules.

**Unverified research (read the tag before trusting a number):** all stock and prices (snapshots from 2026-11-01/02; Evelta shows contradictory stock labels; Robu, Robocraze and several other sellers were blocked and not read); most regulatory text (official DoT, India Code and e-Gazette pages were unreadable; many items rest on mirrors and law-firm summaries); module pin orders for vendor breakouts; the older ST25R3916 datasheet revision (Rev 3, 2020).

## 6. Known gaps and traps

1. **USB-C CC1/CC2 ADC pins and BQ24075 control lines (EN2, CE, SYSOFF) are not in the pin maps.** Add two ADC pins and re-solve; the BQ24075 lines can use spare PCA9535 B bits. Re-solving can move other pins, which would change `firmware/board/` headers, `03-core-module.md`, the diagrams and the Zephyr test overlays, so regenerate all of them.
2. **Zephyr SPI pitfall:** the STM32 driver skips reconfiguration when the `struct spi_config` pointer is unchanged. One config struct per device; never edit one in place.
3. **ST licences:** ST's RFAL (SLA0052) and ST's USB library (SLA0044) forbid use that would subject them to open-source terms, so they cannot be in a distributed GPL binary. The ST25R3916 driver has to be written from the datasheet (or separate terms obtained). The SLA0052 text was read from a third-party copy. Not legal advice.
4. **Voltage safety on the PN532 V3 breakout:** its host pins are not 5 V tolerant (4 V absolute max); the board's regulator was not found. Power it from 3V3_P first and measure before connecting.
5. **Parts that do not work for this design:** MT3608 boost (no load disconnect), AP2112K (600 mA), TSOP1738 on 3.3 V (rated 4.5-5.5 V in the sheet that was read), JST SH 1.0 mm (genuine parts not confirmed in India), 1-wire ID EEPROMs (not found in India; 24-series I2C EEPROMs are used instead).
6. **The 144-pin Nucleo boards** do not carry the 176-pin H743's pins (for example PI2), so they can only test part of the final pin map.
7. **Gaps with no Indian-stocked part found:** per-port current-limited load switches with a fault flag at confirmed stock, ST25R3916, a buck-boost converter, genuine JST SH, 0.8 mm board-to-board connectors, 1-wire ID chips.
8. The ERC/DRC and diagram numbers refer to pin-map draft 2.

## 7. How to resume on a machine

Local environment as left on 2026-11-02 (it may have changed; check):
- **Zephyr:** `~/zephyr-work/` holds the venv, the west workspace (`ws/`), Zephyr SDK 1.0.1 and build folders. `source ~/zephyr-work/env.sh` (a copy is `firmware/zephyr/env.sh.example`), then `west build ...` as in `firmware/zephyr/README.md`. About 5 GB.
- **KiCad checks:** they ran in Docker with the official image. **That image was no longer on the machine on 2026-11-11**; re-pull it with `docker pull kicad/kicad:10.0` (about 0.8 GB download, 3.5 GB on disk) before repeating them; commands are in `hardware/kicad/README.md`.
- **Regenerate files:** `tools/pinmap.py`, `verify.py`, `genboard.py` (see `tools/README.md`; needs the ST pin data clone in `datasheets/`); `python3 hardware/kicad/tools/gen_kicad.py hardware/kicad`; `python hardware/pinouts/gen_pinouts.py <repo root>` (needs matplotlib).
- **Disk** was at about 89 % used; avoid large installs.
- **Memory file** for Claude Code: `synnefo-handheld-project.md` in the project's Claude Code memory folder under `~/.claude/projects/` (outside the repo, on the owner's machine).
- Before any commit: scan staged files for secrets and personal paths, e.g. `git ls-files -z | xargs -0 grep -nIiE "gmail|token|password|secret|api[_-]?key|/ho[m]e/|/t[m]p/"`.

## 8. What to do next, in order

Needs the owner:
1. Decide the 3.3 V-only ID phase (SMIS v0.2 section 6) or ask for the always-on ID rail.
2. Request written quotes and lead times: Hubtronics (NUCLEO-F429ZI, H743ZI, H753ZI), Evelta (F429ZI stock and ship-from; BQ24075, MAX17048, TPS61088 stock), Lion Circuits (H753ZI ship-from and invoice), DNA Tech and others for bare STM32H743 chips; ST authenticity proof for the F429ZIT6 chips.
3. Buy test hardware: a PN532 V3 board (DNA Tech had 50 at ₹317.43), a CC1101 868 MHz board, an RDM6300, a Nucleo-F429ZI, and either an H743-class board or the NUCLEO-H723ZG (DNA Tech had 3 in stock). Measure and photograph the breakout headers.
4. Fetch from a machine that can reach st.com: ST25R3916B datasheet DS13541, current DS12484, AN5276, AN5240, AN5322, AN5592, UM3007 and the X-NUCLEO-NFC08A1 schematic, and the X-CUBE-NFC6 licence file.
5. Send the 13 questions in `07-india-regulatory.md` to a lawyer or test lab before any sale.

Engineering:
6. Add the CC1/CC2 ADC pins and re-solve the pin maps (see section 6, gap 1); regenerate headers, connector table, diagrams.
7. Check Indian stock and pin compatibility of the bare STM32H753, H563 and F439 chips (the substitutes for the H743/F429).
8. Run the hardware checks of the three Zephyr test items on Nucleo boards.
9. Finish the PN532 adapter once a breakout has been measured, then route it; read the ST documents and finish the ST25R3916 module.
10. Remaining SMIS and power items: fuse hold currents, EEPROM datasheets, per-port limits, non-Q1 TPS61088 and PCA9555/TCA9535 datasheets, cell datasheet and BIS number.
11. Write the ST25R3916 driver independently; write the SPI arbiter and module manager (`10-firmware-architecture.md`).
12. Design the carrier and core-module boards once the pin maps and SMIS are stable; then the first bill of materials.

## 9. Open questions for the owner

1. Accept or change the 3.3 V-only ID phase?
2. Is the proposed port numbering and module assignment acceptable (P1 CC1101, P2/P3 NFC, P8 RDM6300)?
3. Should the pin maps be re-solved now to add CC1/CC2, accepting that some pins may move?
4. Is buying an H723ZG (a different MCU) acceptable as a stand-in H7 test board?
5. Who will contact sellers and the lawyer, and by when?
