# NFC modules: Variant A (PN532) and Variant B (ST25R3916)

Status: PROPOSED design, version 2. Not built, not tested. Both variants are planned in full (user decision R19). Variant A is buildable now from Indian stock. Variant B depends on an Indian source for the ST25R3916 (none found yet) and on four ST documents that could not be read.

Source labels: **[P]** primary manufacturer document actually read by a research agent; **[V]** vendor page or schematic; **[S]** secondary (forum, snippet, distributor text); **[N]** not found; **[K]** my own engineering judgement. I have not independently re-read any of the documents myself.

## 1. Side-by-side

| | Variant A: PN532 | Variant B: ST25R3916 |
|---|---|---|
| Build route under R17 (India-only) | Plug-in adapter board carrying the in-stock PN532 V3 breakout (DNA Tech ₹317.43, 50 in stock; verified page) | Custom board with the chip. Chip found only at import routes. **Blocked until an Indian source exists** |
| Technologies [P] | ISO14443A/B, MIFARE, FeliCa 212/424, card emulation (A/MIFARE, FeliCa), peer-to-peer. **No ISO15693** | NFC-A/B up to 848 kbit/s, NFC-F, **NFC-V/ISO15693**, all five NFC Forum tag types, EMVCo 3.0, card emulation NFC-A/F, P2P |
| Official range statement [P] | Up to 50 mm reader, about 100 mm card emulation; vendor's 5–7 cm is marketing [V] | No range or output-power figure in the datasheet read [N] |
| SPI mode / order / max clock [P] | Mode 0, **LSB first**, 5 MHz max | **CPOL 0, CPHA 1 (mode 1)**, MSB first, 10 MHz max |
| IRQ polarity [P] | **Active low** (P70_IRQ) | **Active high** |
| Reset pin | RSTPD_N (hard power-down), active low | **None.** Power-on reset or direct command C0 "Set default" |
| Interface select [P] | I0/I1 pins (SPI = I0 high, I1 low) via DIP switches on the board | I2C_EN pin: tie to GND for SPI |
| Chip supply [P] | VBAT 2.7–5.5 V (performance reduced below 3.3 V); host pins PVDD 1.6–3.6 V recommended, 4 V absolute max (not 5 V tolerant) | VDD and VDD_TX 2.4/2.6–5.5 V (must be the same supply, ±0.2 V); VDD_IO 1.65–5.5 V sets logic level |
| Current [P] | TX about 60 mA typ / 100 mA max; total under 100 mA with recommended antenna; hard power-down about 2 µA | Ready 4.5 mA, all active with RF segments off 16 mA at 3.3 V; **full-field current not found** [N]; internal driver regulator limit 350 mA rms |
| Package | Breakout board (42.7×40.4×4 mm) | Leadless 5×5 mm QFN32 (AQWT; AQET reported) or WLCSP36 (not hand-friendly) |
| Host library licences | Adafruit-PN532 BSD, Seeed-Studio/PN532 BSD 3-clause (read); libnfc LGPL v3 but Linux-only | ST RFAL under SLA0052 (read): usable only with ST silicon; X-CUBE-NFC6 licence unread |
| Difficulty | Low: header-based | High: RF design, antenna tuning, reflow QFN |

## 2. Findings that affect the system, not just the module

1. **SPI mode differs between modules on the shared expansion SPI bus.** CC1101: mode 0, up to 6.5–10 MHz. PN532: mode 0, LSB-first, 5 MHz. ST25R3916: mode 1, MSB first, 10 MHz. The firmware SPI layer must reconfigure phase, bit order and clock per transaction (or per port) and serialize access.
2. **IRQ polarity differs.** The module descriptor needs an `irq_polarity` field (active_low / active_high), and the driver sets the EXTI edge accordingly. Alternative: an inverter on the module. Proposed: descriptor field, no hardware inverter.
3. **The SM-S RST pin cannot be a plain reset on Variant B.** Use RST as a module-level enable: it switches power through a small load switch on the module, or is left unconnected and the driver uses command C0. PROPOSED: RST is optional, descriptor field `reset_method: [pin_power|command|none]`.
4. **Supply choice.** SM-S offers 3V3 and 5V_SW. Variant B's chip works from 5 V (VDD/VDD_TX from 5V_SW) with VDD_IO at 3.3 V [P, my reading]. Variant A's breakout takes 3.3 V on VCC.
5. **Rev caveat for Variant B.** All Variant B chip facts come from DS12484 Rev 3 (2020, a mirror copy). The current DS12484 Rev 8 and the ST25R3916B datasheet DS13541 Rev 11 were not readable and may differ.

## 3. SM-S connector mapping (both variants, 3.3 V logic)

SM-S: 1 GND, 2 3V3, 3 5V_SW, 4 SCK, 5 MOSI, 6 MISO, 7 CS, 8 IRQ, 9 RST, 10 ID.

| SM-S | Variant A | Variant B |
|---|---|---|
| 2 3V3 | Breakout VCC (first spin, see §4.2) | VDD_IO (logic level) and optional low-voltage supplies |
| 3 5V_SW | Not used in first spin (jumper option) | VDD and VDD_TX (5 V mode) |
| 4 SCK | SCK (30), mode 0, LSB first | SCLK, mode 1 |
| 5 MOSI | MOSI (28) | MOSI |
| 6 MISO | MISO (29) | MISO |
| 7 CS | NSS (27), also wakes the chip when low | BSS (active low) |
| 8 IRQ | P70_IRQ, active low | IRQ, active high |
| 9 RST | RSTPD_N, active low | Optional power switch on module, else unused |
| 10 ID | 1-wire ID device | 1-wire ID device |

Pin numbers in the Variant A column are PN532 chip pins [P]; on the breakout use the header labels (IRQ, RSTPDN, SCK, MISO, MOSI, SSEL) and confirm on the board.

## 4. Variant A: PN532 adapter

### 4.1 Architecture

```
SM-S connector  ->  adapter PCB  ->  PN532 V3 breakout (plugged or soldered onto headers)
 3V3, SPI, IRQ, RST, ID           ID chip, jumpers, optional protection
```

### 4.2 Design rules (from the documents read)

- **Voltage safety [P+V]:** PVDD (the chip's host-pin supply) is 4 V absolute max, so the chip's host pins are not 5 V tolerant. The Elechouse guide claims the SPI lines "could be connected directly" to a 5 V host through 100 Ω; that does not follow from the chip rating and is treated as unverified and risky. The regulator on the breakout was **not found** in the schematic text [N]. Rule: first spin powers the breakout from **3V3**, so lines are at 3.3 V; verify by measuring SCK, MOSI, MISO, SSEL, IRQ, RSTPDN before connecting to the host. Do not apply 5 V to the board until its regulator and PVDD source are confirmed.
- **Supply jumper (optional):** JP1 selects 3V3 (default) or 5V_SW. Left open on the first spin until measured.
- **Interface switches [V, conflicting]:** Elechouse table gives SPI = switch 1 OFF, switch 2 ON; the NXP data sheet gives SPI = I0 = 1, I1 = 0; Adafruit's own board differs. Clones may differ again. Verify with a meter before power-up and mark the correct positions on the adapter silkscreen.
- **Reset / wake [P]:** RSTPD_N low = hard power-down; NSS low wakes the chip, hold NSS low for the oscillator start-up (typically a few hundred µs, up to 2 ms). Post-reset delay not in the documents; start from 1 ms low, 2 ms, 10 ms (Adafruit code, [S]) and measure.
- **IRQ [P]:** active low when a response or ACK is ready; the host can wait on it instead of polling the SPI status byte (0x01 ready). A pulse up to 12 ms occurs when waking the host from power-down.
- **SPI framing [P]:** first byte after NSS falls: 0x02 status read, 0x01 data write, 0x03 data read; each transfer framed by NSS. The STM32 SPI has an LSB-first option; otherwise bit-reverse in software.
- **Current [P]:** RF on, up to about 100 mA, 150 mA max from the supply: budget the 3V3 rail accordingly and add local bulk decoupling on the adapter.
- **Antenna [P+V]:** keep wires crossing the antenna at 90°; keep the coil clear of metal and the battery. No official detuning data [N]: measure range with the final enclosure.
- **ID device:** 1-wire EEPROM-class chip on SM-S pin 10 (family and part TBD; not yet sourced in India).

### 4.3 Assembly and BOM (nothing ordered)

| Item | Source status |
|---|---|
| PN532 V3 breakout | DNA Tech, ₹317.43 incl. GST, stock 50 (page opened by an agent). Robu and Robocraze listings unverified (blocked) |
| SM-S connector | Family OPEN (see 05-): SH-style generic, GH 1.25 mm, XH or 2.54 mm box header |
| 1-wire ID chip | Not yet searched in India |
| Header pins, jumper, decoupling capacitors | Standard parts; not yet checked |
| Adapter PCB | Custom, hand-solderable, all through-hole or header-based |

### 4.4 Firmware (Variant A)

- Port Adafruit-PN532 or Seeed-Studio/PN532 (both BSD); no existing STM32 PN532 driver was found, so a small HAL-based port is needed: SPI mode 0, LSB-first, ≤ 1 MHz to start, IRQ-driven ready, power-down/wake sequence.
- Does not support ISO15693; the driver reports this in `capabilities()`.

## 5. Variant B: ST25R3916 module

### 5.1 Architecture

```
SM-S  ->  [ 5V_SW ] -> VDD, VDD_TX (same supply)      [ ID chip ]
          [ 3V3 ]   -> VDD_IO (logic level)
          SPI + IRQ +-> ST25R3916 (QFN32)  -> EMC filter -> matching network (AAT optional) -> PCB antenna
                                  |                          27.12 MHz crystal
```

### 5.2 Design rules from DS12484 Rev 3 [P]

- **Supplies:** VDD (pin 8) and VDD_TX (pin 10) from one supply, within ±0.2 V; range 2.6–5.5 V (-40 to +105 °C) or 2.4–5.5 V (-20 to +105 °C); absolute max 6.0 V. VDD_IO (pin 1) sets the logic level of the digital pins; 3.3 V VDD_IO with 5 V VDD is a supported combination (my reading).
- **Mode bit:** the default is 5 V mode. If the chip is supplied from 3.3 V, set `sup3V` (IO configuration register 2, address 01h). In 5 V mode VDD_A and VDD_D are fixed at 3.4 V and VDD_RF is adjustable 3.6–5.1 V in 120 mV steps; in 3.3 V mode VDD_RF is adjustable 2.4–3.6 V in 100 mV steps.
- **Do not supply VDD_A externally** (ST staff, secondary [S]).
- **Reduced RF power at 3.3 V supply** (ST staff [S]): "putting VDD = VDD_TX = 3V3 will reduce the achievable output power". Plan for 5 V on VDD/VDD_TX.
- **Regulator limits:** the VDD_RF regulator limits current to 350 mA rms. Above that, VDD_RF and VDD_DR must be tied to VDD_TX externally. Power dissipation limit 300 mW (Table 118).
- **Decoupling [P]:** 2.2 µF in parallel with 10 nF on the regulator pins; 1 µF + 10 nF on AGDC; 2.2 µF + 1 nF on VDD_AM.
- **Interface:** I2C_EN to GND selects SPI. SPI CPOL 0, CPHA 1, MSB first, max 10 MHz; at ≤ 5 MHz the clock period ≥ 200 ns, at 5–10 MHz ≥ 100 ns; BSS high (SPI reset) ≥ 100 ns; setup/hold ≥ 10 ns. MISO is tri-state (optional pull-downs via `miso_pd1/2`). IRQ is active high; the four interrupt registers (1Ah–1Dh) are read-only and cleared on read.
- **Start-up sequence [P, §4.1]:** after power-on send Set default (C0), configure IO configuration registers 1 and 2 (including `sup3V` if applicable), run Adjust regulators (D6), then run the AAT procedure if AAT is used. Wait for I_osc/osc_ok; the start-up time in ms is not given in Rev 3 [N].
- **Crystal:** 27.12 MHz, amplitude regulated to about 1 Vpp. Load capacitance and ESR **not found** [N]; take them from the chosen crystal's own datasheet and ST's reference design.
- **MCU_CLK:** optional output (3.39, 6.78 or 13.56 MHz) usable as host clock; not needed here.
- **Reset:** no hardware reset pin. See §2 item 3.
- **Package:** VFQFPN32 5×5 mm, 0.5 mm pitch, exposed pad 3.4–3.6 mm square that must be soldered (hot air with paste). Ordering: ST25R3916-AQWT; ST25R3916B and AQET variants reported by distributors [S] (AQWT reported NRND, unverified). The WLCSP (BWLT) is not hand-friendly. Choose the QFN.
- **Layout [S, ST staff]:** 4 or more layers recommended; EMC filter close to the IC; the connection from the driver output (RFO) to the EMC filter carries a rectangular broadband signal; short matching traces (< about 1 cm) need no controlled impedance; about 4 pF parasitic per 1.6 mm stack-up. **Keep-out rules not found** [N]. Reference documents named by ST staff: AN5240 (layout), AN5276 (antenna), AN5584 (thermal).
- **Antenna and matching: not designed.** AN5276, AN5322 (AAT), AN5592 and the NFC08A1 design files were unreadable. Do **not** use the forum values (270 nH / 680 pF filter, 47×34 mm 4-turn coil): they come from older boards and snippets. The documented flow (secondary) is: measure the coil's inductance at 1 MHz, DC resistance and parallel resistance at self-resonance; compute components with ST's antenna matching tool; fine-tune with a VNA with the driver off; verify read range. A 0.5–1.5 µH loop is described as a safe range [S].
- **AAT / capacitive sensor [P]:** automatic antenna tuning (ST25R3916 only) uses external variable capacitors set through registers 26h/27h with tuning voltages on AAT_A/B; the capacitive sensor (CSO/CSI) supports low-power wake-up (calibrates over 0.1–3.1 pF). Optional in the first spin; decide after reading AN5322.

### 5.3 BOM (nothing ordered; not sourceable under R17 yet)

| Item | Status |
|---|---|
| ST25R3916 / ST25R3916B QFN32 | Import routes only (DigiKey India about ₹455–₹596, Mouser India, Tanotis); no Indian seller found |
| 27.12 MHz crystal | Not searched; part and load capacitors TBD from the datasheet |
| Matching network, EMC filter, coil | Values TBD after AN5276; fixed capacitors on the first spin, variable (AAT) later |
| 1-wire ID chip | Not searched |
| SM-S connector | Family OPEN |
| Load switch for optional RST power | Not found in India (same gap as the port switches) |

### 5.4 Firmware (Variant B)

- Use ST's RFAL. Licence SLA0052 (read from the stm32duino repositories): redistribution allowed, but condition 4 restricts use to products with an ST NFC/RFID IC (fine here, but ties the code to ST silicon); GitHub reports it as non-recognised, so check it before distributing firmware. X-CUBE-NFC6 licence not read; reported to mix Apache-2.0/BSD-3 for CMSIS/HAL/BSP with ST's agreement for NDEF/RFAL. RFAL's platform layer is plain C (SPI, GPIO, IRQ), but support for STM32F4 and STM32H7 is **not verified**. Third-party ports: stm32duino/ST25R3916 and NFC-RFAL (SLA0052), Elechouse port (licence unread).

## 6. Common driver interface

`nfc_driver_t`: `probe()`, `init()`, `field_on()/field_off()`, `poll(tech_mask, timeout)`, `read(tag)`, `write(tag)`, `emulate(profile)`, `capabilities()`, `deinit()`.
Descriptor additions needed by this analysis (illustrative names):

```yaml
spi_mode: 0            # 0 or 1
spi_bit_order: lsb     # lsb | msb
spi_max_hz: 5000000
irq_polarity: active_low   # active_low | active_high
reset_method: pin          # pin | pin_power | command | none
supply: 3v3                # 3v3 | 5v_sw
capabilities: [iso14443a, iso14443b, mifare, felica, card_emulation, p2p]   # + iso15693, nfc_forum on Variant B
```

Per-transaction SPI reconfiguration and bus arbitration are the SPI layer's job (see §2 item 1).

## 7. Bring-up and acceptance tests (both variants)

1. **ID:** descriptor read; unknown version stays unpowered and is shown as unsupported.
2. **Voltage check before first power on host:** Variant A: measure all breakout signal lines at 3V3 and (if used) 5V_SW; confirm DIP settings with a meter. Variant B: check VDD, VDD_TX, VDD_IO, VDD_A, VDD_D, VDD_RF against §5.2.
3. **Power:** idle and RF-on current at the connector, recorded for each rail (no figure asserted).
4. **SPI link:** Variant A: read firmware version via GetFirmwareVersion; Variant B: read identification registers after C0.
5. **Interrupts:** IRQ polarity and timing; wake from sleep on tag arrival.
6. **Tags:** detect each tag type you own (ISO14443A MIFARE card, ISO14443B if available; ISO15693 tag on Variant B only).
7. **Range and detuning:** measure range with and without the enclosure, battery and metal nearby.
8. **Variant B only:** crystal start-up and frequency; antenna resonance and Q with a VNA (driver off); VDD_RF ripple; thermal rise at full field; EMC pre-scan of 13.56 MHz harmonics.
9. **Faults:** card removed mid-read, no antenna, wrong supply, SPI bus shared with a CC1101 at the same time.

## 8. Risks

- Variant A: breakout I/O level and DIP mapping unverified on clone boards; LSB-first SPI bug; no ISO15693.
- Variant B: antenna tuning and EMC are the dominant risk; the 350 mA regulator limit; reduced output power at 3.3 V; QFN32 exposed-pad soldering; no reset pin; documents read are an old revision.
- Both: shared SPI bus with different modes; IRQ polarity mismatch; 13.56 MHz transmit rules in India **not researched**; library licences (SLA0052 restricts to ST silicon; X-CUBE-NFC6 unread).
- Do not claim Flipper-level NFC parity for Variant A.

## 9. Open items and actions

1. **Fetch by hand (a machine that can reach st.com):** current ST25R3916B datasheet DS13541, current DS12484, AN5276 (antenna), AN5240 (layout), AN5322 (AAT), AN5592, AN5584, UM3007 and the X-NUCLEO-NFC08A1 schematic, and the X-CUBE-NFC6 LICENSE file. Without them, Variant B cannot be taken past this plan.
2. Buy one PN532 V3 board and measure it (regulator, PVDD source, signal voltages, DIP mapping, current).
3. Ask Indian distributors for ST25R3916 / ST25R3916B QFN (Evelta, DNA Tech, Hubtronics, Tanna TechBiz) and for a 27.12 MHz crystal.
4. Decide the SM-S connector family and the 1-wire ID chip.
5. Indian regulatory research for 13.56 MHz equipment.
6. Verify RFAL on STM32F4/H7 and read the X-CUBE-NFC6 licence.

## 10. KiCad skeletons

Generated projects for both variants are in `hardware/kicad/` (see its README for what was checked and what is unverified).
