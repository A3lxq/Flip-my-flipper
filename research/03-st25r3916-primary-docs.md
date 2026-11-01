# ST25R3916 / 3916B (from DS12484 Rev 3)

Condensed from a research-agent report. Primary document read: DS12484 Rev 3 (June 2020), 156 pages, from the mirror https://download.mikroe.com/documents/datasheets/ST25R3916%20Datasheet.pdf (old revision, mirror copy). **Not readable** (st.com and mouser.com timed out or returned 403): current DS12484 Rev 8 (2023), ST25R3916B datasheet DS13541 Rev 11 (2026), AN5276 (antenna), AN5240 (layout), AN5322 (AAT), AN5592 (single-ended matching), AN5584 (thermal), UM3007, X-NUCLEO-NFC08A1 schematic, X-CUBE-NFC6 package and licence.

## Supply [primary, §4.2.11, Tables 118–119]
- VDD (pin 8) and VDD_TX (pin 10) must be the same supply (±0.2 V); 2.6–5.5 V (−40 to +105 °C) or 2.4–5.5 V (−20 to +105 °C); abs max 6.0 V (5 V with sup3V set).
- VDD_IO (pin 1) 1.65–5.5 V sets the logic level of BSS, MISO, MOSI, SCLK, IRQ, MCU_CLK; VIH 0.8×VDD_IO, VIL 0.2×VDD_IO. 3.3 V logic with 5 V power is a supported combination (agent's reading).
- Default is 5 V mode; set `sup3V` (IO configuration register 2, address 01h) for a 3.3 V supply. In 5 V mode VDD_A/VDD_D are fixed at 3.4 V and VDD_RF adjusts 3.6–5.1 V in 120 mV steps; in 3.3 V mode VDD_RF adjusts 2.4–3.6 V in 100 mV steps.
- VDD_RF regulator limit 350 mA rms (above that, tie VDD_RF and VDD_DR to VDD_TX); power dissipation limit 300 mW.
- Decoupling: 2.2 µF ∥ 10 nF on the regulator pins; 1 µF ∥ 10 nF on AGDC; 2.2 µF + 1 nF on VDD_AM.
- Secondary (ST staff forum): a 3.3 V supply reduces achievable output power; do not supply VDD_A externally.

## Interface [primary, §4.3]
- SPI: CPOL 0, CPHA 1 (mode 1), MSB first, max 10 MHz; period ≥ 200 ns (≤ 5 MHz) or ≥ 100 ns (5–10 MHz); BSS high ≥ 100 ns; setup/hold ≥ 10 ns. MISO tri-state with optional pull-downs.
- Opcodes: register write 00AAAAAA, read 01AAAAAA, FIFO load 10000000, FIFO read 10011111, direct command 11CCCCCC (C0 Set default, C2 Stop all, C8 NFC initial field on, D6 Adjust regulators, DB Clear FIFO). Space-B registers via prefix FBh. FIFO 512 bytes.
- IRQ is active-high; interrupt registers 1Ah–1Dh are read-only and cleared on read; masks at 16h–19h.
- I2C selected by the I2C_EN pin (GND = SPI); I2C address 50h.
- **No reset or enable pin**: power-on reset or command C0; `en` bit in register 02h controls oscillator/regulators. Start-up sequence in §4.1 (C0, configure, D6, AAT if used); oscillator start-up time in ms not given.
- Crystal 27.12 MHz, about 1 Vpp; load capacitance and ESR not found.

## Packages [primary]
VFQFPN32 5×5 mm, 0.5 mm pitch, exposed pad 3.4–3.6 mm that must be soldered; WLCSP36 3.2×3.2 mm (ST25R3916 only, not hand-friendly). Ordering code scheme `ST25R3916-AQWT` (QFN, −40..+105 °C) and `-BWLT` (WLCSP, −40..+85 °C), 4000/5000 per reel. AQET reported by distributors (secondary); AQWT reported NRND (unverified).

## Capabilities and current [primary]
NFC-A/B up to 848 kbit/s, NFC-F up to 424 kbit/s, NFC-V up to 53 kbit/s, all five NFC Forum tag types, EMVCo 3.0, card emulation NFC-A/F, active/passive P2P, AAT (ST25R3916 only), capacitive wake-up. RF output power and read range: no figures. Currents (typ, 25 °C): power-down 0.8 µA (3.3 V); ready 4.5 mA; all active with RF segments disabled 16 mA at 3.3 V (not full-field). Full-field current: not found.

## Antenna and layout [mostly not found]
No primary content. Secondary (ST forum, older boards): an EMC filter of 270 nH / 680 pF (UM2358, older board) and a 47×34 mm four-turn coil on the NFC08A1 are quoted; **do not use as design values**. Documented flow: measure coil inductance at 1 MHz, DC and parallel resistance; compute with ST's matching tool; tune with a VNA with the driver off; verify range. Layout (secondary): four or more layers, EMC filter close to the IC, short matching traces need no controlled impedance. Keep-out rules and measured Q: not found.

## Software and licence
SLA0052 Rev 3 (read via stm32duino repositories): redistribution allowed; condition 4 limits use to products with an ST NFC/RFID IC; GitHub shows NOASSERTION. X-CUBE-NFC6 licence unread (reported mix of Apache-2.0 / BSD-3 / ST agreement). RFAL support on STM32F4/H7 not verified. No regulatory approval statement in the datasheet.
