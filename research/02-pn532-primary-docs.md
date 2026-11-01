# PN532 and the V3 breakout (from NXP and Elechouse documents)

Condensed from a research-agent report. Documents read: NXP PN532/C1 data sheet Rev 3.6 (28 Nov 2017, doc 115436) https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf ; NXP UM0701-02 PN532 User Manual Rev 02 (2007, firmware V1.6) https://www.nxp.com/docs/en/user-guide/141520.pdf ; Elechouse PN532 module V3 user guide (13 pp) and schematic text layer (the drawing itself could not be rendered); Adafruit PN532 learn guide (secondary).

## Chip facts [primary]
- VBAT 2.7–5.5 V recommended, abs max −0.5 to 6.0 V; below 3.3 V performance (range) is reduced.
- PVDD (host pins) 1.6–3.6 V recommended, abs max 4 V: **host pins are not 5 V tolerant**. Logic thresholds follow PVDD (VIH ≥ 0.7×PVDD, VIL ≤ 0.3×PVDD).
- DVDD internal LDO from VBAT, 3 V typ above 3.4 V; 10 µF low-ESR decoupling.
- Currents (typ, 25 °C, VBAT 3.4 V, PVDD 3 V): hard power-down 2 µA; soft power-down 18–25 µA; transmitter with continuous wave 60 mA typ / 100 mA max; total ≤ 150 mA max, below 100 mA with recommended antenna tuning. Idle and card-emulation currents not given separately.
- Host interface select: I0/I1 pins; selif 00 = HSU, 01 = SPI, 10 = I2C. SPI means I0 = 1, I1 = 0. SPI pins: NSS 27, MOSI 28, MISO 29, SCK 30.
- SPI: **mode 0, LSB first**, max 5 MHz (DS), half-duplex; t(SCK low/high) ≥ 50 ns. First byte after NSS falls selects the operation: 0x02 status read, 0x01 data write, 0x03 data read; ready byte 0x01. IRQ (P70_IRQ) is active-low when a response/ACK is ready; a pulse up to 12 ms occurs when waking the host from power-down. NSS low wakes the chip; hold it for oscillator start-up (typically a few hundred µs up to 2 ms). RSTPD_N low = hard power-down. Post-reset wait time: not found (Adafruit code, secondary: reset low 1 ms, high, 2 ms, then 10 ms).
- Capabilities: ISO14443A/MIFARE, 14443B (reader/writer), FeliCa 212/424 kbit/s, card emulation (A/MIFARE or FeliCa), NFCIP-1 P2P to 424 kbit/s. **ISO15693 not listed.** Official ranges: reader up to 50 mm, card emulation about 100 mm.

## The V3 breakout [vendor, partly inferred]
- Size 42.7×40.4×4 mm, PCB antenna; vendor reading distance 5–7 cm (marketing).
- Vendor says VCC 3.3–5 V; I2C/UART level shifted; SPI 3.3 V TTL with 100 Ω series resistors and "could be connected directly to 5 V" (**unverified and risky**: 100 Ω alone does not meet the chip's 4 V limit).
- Schematic text: rails VCC5V and VCC3.3V; **no regulator part found**; dual MOSFET level shifters on SDA/SCL; R10–R14 100 Ω on SPI; 27.12 MHz crystal; matching components.
- DIP switches (Elechouse): HSU both OFF, I2C SW1 ON/SW2 OFF, **SPI SW1 OFF/SW2 ON** (conflicts with the NXP selector mapping and Adafruit's board, so clones may differ again; verify with a meter).

## Software licences (read from repositories)
libnfc LGPL v3 (Linux-oriented SPI, not an STM32 driver); Adafruit-PN532 BSD (SPI, LSB-first mode 0); Seeed-Studio/PN532 BSD 3-clause (SPI); elechouse/PN532 BSD-style header (first lines only). No Zephyr, ESP-IDF or STM32 PN532 driver found.

## Still to measure on the actual board
Regulator and PVDD source; voltages on all signal lines at 3.3 V and 5 V; DIP mapping; IRQ/RSTPDN pull-ups and polarity; LSB-first SPI on the STM32; supply current in RF bursts (up to about 100–150 mA); post-reset/wake delays; range and detuning in the final enclosure (no official data on metal/battery detuning).
