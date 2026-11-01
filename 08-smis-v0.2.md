# Synnefo Module Interface Standard (SMIS) v0.2

Status: PROPOSED draft. Supersedes the connector and ID sections of v0.1 (`01-requirements-and-architecture.md` §5, §11, §13). Numbers marked TARGET are design goals to confirm by test, not ratings. Sources for part facts are in `05-`, `06-`, `07-` and `09-power-architecture.md`.

## 1. What changed from v0.1 and why

| # | Change | Reason |
|---|---|---|
| 1 | **One connector footprint for every port**: 10-contact (2×5), 2.54 mm shrouded, keyed box header | Verified in Indian stock (Probots 10-pin right-angle, ₹17 incl. GST, in stock). Genuine JST SH 1.0 mm is not confirmed in India; 6- and 8-pin variants of other families were not verified. |
| 2 | **Power and ID pins are identical on every class** (pins 1, 2, 3, 9, 10) | One carrier port design; class is declared by the module descriptor. |
| 3 | **Two-wire module ID** (data `IDD` per port, clock `IDC` per port), replacing the single-wire ID | The 1-wire EEPROMs (DS2431 etc.) were not found in any Indian store. The 24-series I²C EEPROMs are in stock (ElectronicsComp 24C02, M24C04). |
| 4 | **RST contact removed**; reset is by power-cycling the module's 3V3_P or a chip command | ST25R3916 has no reset pin, CC1101 resets by SPI strobe, PN532 can be reset by power cycle. Freed the contact for IDC. |
| 5 | **Separate switched rails per port**: `3V3_P` and `5V_P` | Each port has its own enable lines; 3V3_P can be on while 5V_P is off. |
| 6 | **ID is read with only 3V3_P on**; 5V_P stays off until the descriptor is validated | An EEPROM needs power to be read. See §6 for the safety argument and the decision this needs from you. |
| 7 | **Descriptor extended** with SPI mode, bit order, clock, IRQ polarity, reset method, supply and current fields | Required by the CC1101 / PN532 / ST25R3916 differences (06-nfc-modules.md §2). |
| 8 | **Hot-plug not supported in V1**: modules are changed with the port ejected from the UI | Box headers do not guarantee ground-first mating. |

## 2. Port classes and pinouts

All classes use the same 10 contacts. Pins 1, 2, 3, 9 and 10 never change function.

| Pin | SM-S (SPI) | SM-I (I²C) | SM-U (UART) |
|---|---|---|---|
| 1 | GND | GND | GND |
| 2 | 3V3_P | 3V3_P | 3V3_P |
| 3 | 5V_P | 5V_P | 5V_P |
| 4 | SCK | SDA | TX (module output) |
| 5 | MOSI | SCL | RX (module input) |
| 6 | MISO | IRQ | IRQ |
| 7 | CS | GPIO (optional) | GPIO (optional) |
| 8 | IRQ | not connected | not connected |
| 9 | IDC | IDC | IDC |
| 10 | IDD | IDD | IDD |

Naming: TX and RX are from the host's point of view (host TX drives module RX). Module signal pins are 3.3 V logic and not 5 V tolerant.
Port counts (CONFIRMED): 5 SM-S ports, 2 SM-I ports, 1 SM-U port, as in R14b.

## 3. Electrical rules

TARGET values; confirm by test.

| Item | TARGET |
|---|---|
| Logic level | 3.3 V only. Never 5 V on any signal contact. |
| `3V3_P` per port | 100 mA default, up to 200 mA if the descriptor requests it and the power budget allows |
| `5V_P` per port | 200 mA default, up to 500 mA if the descriptor requests it and the budget allows (SM-S and SM-U only; SM-I modules should not require it) |
| `5V_P` total | 1.5 A across all ports (V1) |
| Contact rating | Box header contacts are rated well above these (per vendor listings; the exact rating of the stocked part is not yet checked) |
| Inrush | Gate-RC soft start on each switch; module bulk capacitance limit TBD |
| Back-power | Carrier never drives a signal high into a powered-off module: `IDD`, `IDC` and all signals are inputs or open-drain until the port is enabled |
| ESD | TVS on signal contacts of external ports (candidates: SRV05-4 at DNA Tech and Sunrom, USBLC6-2SC6 at DNA Tech) |
| Hot-plug | Not supported in V1 |

## 4. Module identification

### 4.1 Hardware

- Each module carries a 24-series I²C EEPROM at address 0x50, SDA on contact 10 (`IDD`), SCL on contact 9 (`IDC`), VCC from `3V3_P`.
- The carrier gives every port its **own** `IDD` and its **own** `IDC` (open-drain to the MCU, pulled up to that port's `3V3_P`). Because both lines are per port, eight identical EEPROMs at 0x50 cannot collide, and no signal is ever driven into an unpowered module.
- The firmware bit-bangs the I²C EEPROM read at 100 kHz or slower, one port at a time. This costs 16 MCU pins (8 IDD + 8 IDC); the pin maps in `02-pin-maps.md` were re-solved with them and still fit both chips (H743 36 spare pins, F429 10 spare).
- Candidate parts, in Indian stock (opened pages): ElectronicsComp 24C02 (DIP-8, ₹11 ex GST, 1,036 available) and M24C04-WMN6P (SOIC-8, ₹17 ex GST, 154). Their datasheets were not read here.

### 4.2 Descriptor (PROPOSED binary layout, little-endian)

| Offset | Size | Field | Notes |
|---|---|---|---|
| 0 | 4 | magic `SMIS` | |
| 4 | 1 | descriptor version | v0.2 = 2; unknown version means unsupported |
| 5 | 1 | class | 1 SM-S, 2 SM-I, 3 SM-U |
| 6 | 2 | vendor ID | assigned by the project |
| 8 | 2 | module ID | |
| 10 | 1 | hardware revision | |
| 11 | 1 | flags | bit 0 needs 5V_P, bit 1 radiates (transmits), bit 2 has reset pin behaviour as in `reset_method` |
| 12 | 2 | 3V3_P max current (mA) | |
| 14 | 2 | 5V_P max current (mA) | 0 if unused |
| 16 | 1 | SPI mode | 0 to 3 (SM-S only) |
| 17 | 1 | SPI bit order | 0 MSB, 1 LSB |
| 18 | 2 | SPI max clock (kHz) | |
| 20 | 1 | IRQ polarity | 0 active low, 1 active high |
| 21 | 1 | reset method | 0 none, 1 power cycle, 2 command |
| 22 | 16 | driver ID (ASCII) | e.g. `pn532` |
| 38 | 24 | name (ASCII) | |
| 62 | 4 | capability bitmask | tech and feature flags |
| 66 | 2 | CRC-16 over bytes 0 to 65 | algorithm TBD (CCITT proposed) |

Total 68 bytes, well inside a 24C02 (256 bytes). The layout is a draft; it is validated against a schema in firmware before any use.

### 4.3 Manual configuration

A module without a valid descriptor is listed as unsupported. The user may define a manual profile (class, driver, voltage, pin use, current) that is checked against the port's limits before 5V_P is enabled. Manual profiles never raise a port beyond its default limits without an explicit confirmation.

## 5. Discovery and power-up sequence

Port state names: OFF, ID, VERIFIED, ON, FAULT.

1. **OFF.** `3V3_P`, `5V_P` off; `IDD`, `IDC` and all signal pins high-impedance. Enable gate nets pulled to the off state by resistors (so expander power-on states cannot enable a port).
2. **Request.** User or firmware requests the port.
3. **ID (3V3_P only).** Enable `3V3_P` through the soft-start switch. Wait for the rail to settle. Read the descriptor over `IDD`/`IDC`. If there is no ACK within the timeout, power the port off and report "no module".
4. **Verify.** Check magic, version, CRC, class equals the port's class, and driver available. If any check fails: OFF, report why.
5. **Budget check.** The power manager checks `3V3_P` and `5V_P` requests against the port and total budgets and the battery state. If not allowed: OFF.
6. **Configure signals.** Set the SPI mode / bit order / clock, UART, or I²C parameters and the IRQ edge from the descriptor. Signal pins stay inputs until this step.
7. **Enable 5V_P** if the descriptor requests it, through the soft-start switch, while monitoring current.
8. **Initialise** the driver and register the module's applications. State ON.
9. **Runtime.** Monitor current; a trip or a persistent over-limit moves the port to FAULT (5V_P off, then 3V3_P off) and reports the cause.
10. **Eject.** UI request: stop the driver, 5V_P off, 3V3_P off, signals high-impedance. Only then may the module be unplugged.

## 6. Safety argument for the ID phase, and the decision it needs

v0.1 said module power must stay off until the descriptor is validated. An EEPROM cannot be read unpowered, so v0.2 powers **3V3_P only**, current-limited, with all signal pins high-impedance and the 5 V rail off. The risks this leaves:
- **A wrong module in the port** (same connector, different class): only 3V3_P and the two ID lines are active, so no signal contention occurs, and the class mismatch is caught in step 4.
- **A faulty module that shorts 3V3_P to ground:** the per-port protection (§7) trips; the other ports are unaffected.
- **A reversed or damaged connector:** the keyed shrouded header prevents reversal; a shorted pin pair is a hardware fault outside this standard.

**Decision needed from you (OPEN):** accept this 3V3-only ID phase, or require a dedicated always-on ID rail (which would cost a contact, a diode-OR network and a per-port current limit, and would still power the EEPROM before validation).

## 7. Per-port protection (Indian-stocked parts only)

No current-limited USB-style switch with a fault flag was found in confirmed Indian stock (05-, 09-). The V1 design is therefore discrete:

| Block | Per port | Parts (all found in Indian stock; see 09-power-architecture.md) |
|---|---|---|
| 5V_P switch | P-channel MOSFET high-side switch with an N-FET/NPN level shifter from the expander (3.3 V cannot drive the gate of a 5 V-source P-FET) | Si2333CDS-T1-GE3 (Hubtronics, 2,887 in stock), BSS138 (Hubtronics) |
| 5V_P sense | INA219 current monitor with a 0.1 Ω shunt; alert lines wire-OR'd to one MCU fault input | INA219 modules/ICs at ElectronicsComp, DNA Tech, Evelta, Hubtronics; 0.1 Ω 2512 shunt at DNA Tech |
| 5V_P backup | Series resettable fuse | WT1206-050 (Hubtronics, 743 in stock; hold current to be checked) |
| 3V3_P switch | P-FET + level shifter, soft start | same MOSFET family |
| 3V3_P backup | Resettable fuse or current limiter | OPEN (hold current for the 200 mA TARGET not yet matched to a stocked part) |
| ESD | TVS on external-port signal pins | SRV05-4, USBLC6-2SC6 |

Optional upgrade after the 5 V behaviour is verified: Hubtronics TPS1HC100 (49 in stock, ₹83) integrates limit, fault flag and current sense but is a 12 V automotive part in a hard-to-solder package; its datasheet was not read for 5 V use.

Enable lines: 16 bits (8 × 3V3_P enable, 8 × 5V_P enable) on one PCA9535 16-bit I²C expander. The PCA9535's outputs are **inputs at power-on**, so every enable gate net needs a pull-down so a port cannot energise before the firmware writes its registers (datasheet fact reported by the research agent: outputs default to inputs, no internal pull-ups). A second expander carries the 8 buttons.

## 8. Software requirements (module manager)

- One state machine per port (§5); descriptor parser with version check and CRC; driver registry keyed by `driver ID`.
- **SPI arbitration:** one transaction at a time on the shared SPI bus; mode, bit order and clock set per transaction from the descriptor (CC1101 mode 0 MSB, PN532 mode 0 LSB, ST25R3916 mode 1 MSB).
- **IRQ:** edge polarity from the descriptor.
- **Power manager:** enforce per-port and total limits, refuse to enable ports when the battery or USB budget cannot support them, shed loads in a defined order.
- **Radio rules (R20):** modules flagged as transmitting obey the region profile, power cap and duty-cycle limits.

## 9. Test plan (acceptance)

1. Descriptor read from each of 8 ports with identical EEPROMs; no collisions.
2. Port off: no voltage on module contacts; no back-power into an unpowered module from any MCU pin.
3. Power-on of the expander and MCU reset: no port energises.
4. 3V3_P and 5V_P short to ground: only that port trips; fault reported; others unaffected.
5. Wrong-class module: rejected without contention.
6. Current accuracy of the INA219 measurement; trip response time.
7. SPI at the module's clock across the box header and cable for each module type.
8. Eject sequence leaves the connector safe to unplug.

## 10. Open items

1. **Decision:** accept the 3V3-only ID phase (§6).
2. Connector part and mating cable/header: the 10-pin right-angle box header is in stock; confirm the mating IDC receptacle and straight/vertical variants, and the SPI signal quality at the target clock.
3. 3V3_P protection part (fuse or limiter) matching the 200 mA TARGET.
4. Read the 24-series EEPROM datasheets and choose the package.
5. Hold currents of the stocked resettable fuses (datasheets not read).
6. Module bulk-capacitance and inrush limit.
7. Confirm the INA219 gain setting for the 0.1 Ω shunt at 0.5 A (my understanding is that ±40 mV full scale is exceeded at 0.5 A, so ±80 mV is needed; verify in the datasheet).
8. Hot-plug (a later revision with a ground-first connector).
