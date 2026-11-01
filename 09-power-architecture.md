# Power architecture v1

Status: PROPOSED design, not built or tested. Datasheet values come from a research agent that downloaded and read the documents (document, revision and page given); I have not re-read them. Values marked **[calc]** are derived by the agent from datasheet formulas under stated assumptions, **[K]** is my engineering judgement, **[N]** not found. Indian-stock status is from `05-deep-sourcing-and-compatibility.md` and the 2026-11-01 port-protection check; stock figures are snapshots and Evelta labels are often contradictory ("in stock" next to "Sold Out").

## 1. Block diagram and rails

```
USB-C (5.1 kΩ on CC1, CC2)
   |
 VBUS ── ESD ──> BQ24075 (charger + power path) ──┬── BAT ── protected 1S cell (3000–3500 mAh)
                                                   │            └── MAX17048 fuel gauge (VDD on BAT node)
                                                   └── OUT (bus: ≈4.3–4.8 V on USB; ≈Vbat on battery)
                                                         ├── buck ── 3V3_SYS  (MCU, display, SD, expanders, gauge)
                                                         ├── buck ── 3V3_IO   (ESP32-S3, port 3V3_P switches)
                                                         └── boost ─ 5V       (port 5V_P switches)
```

| Rail | Source | Feeds | V1 current cap |
|---|---|---|---|
| BAT | cell | charger, fuel gauge | 4.5 A recommended limit on the charger BAT pin |
| OUT (system bus) | BQ24075 | the three converters | 1.5 A from USB (ILIM), battery supplement above |
| 3V3_SYS | buck #1 | MCU, display, SD, I²C expanders, fuel gauge, buttons | 1 A |
| 3V3_IO | buck #2 | ESP32-S3 (355 mA peak per its datasheet), 8 × 3V3_P | 1 A |
| 5V | boost | 8 × 5V_P | 1.5 A (V1) |

Two 3.3 V bucks keep the Wi-Fi bursts and the module ports off the MCU rail. [K]

## 2. Charger and power path: BQ24075

Part: BQ24075RGTR, VQFN-16 3×3 mm; Evelta ₹72.24 ex GST (₹85.24 incl.), stock ambiguous. BQ24070 (217 pcs at Evelta) is an older part with no ILIM resistor or SYSOFF pin in its pin list; not chosen. (TI SLUS810N, Oct 2021; the agent only skimmed the BQ24070 sheet.)

Design facts [P]:
- **OUT is not a clean 5.5 V on USB.** 5.4–5.6 V applies only when VIN > VOUT + dropout. On a 5 V USB input the input FET is in dropout (VDO(IN-OUT) 300 mV typ, 475 mV max at 4.3 V, 1 A), so OUT ≈ VBUS − 0.3 to 0.5 V under load, roughly 4.3–4.8 V [estimate]. On battery, OUT ≈ VBAT − 50 mV typ (100 mV max) at 1 A.
- The charger is linear: input current = charge current + system load.
- Input range 4.35–6.4 V, OVP 6.6 V, survives 26–28 V; VBAT(REG) 4.20 V; precharge below 3.0 V; recharge at VBAT(REG) − 100 mV; battery-supplement mode keeps the system running above the input limit; thermal regulation at 125 °C junction; the device runs the system with an absent battery.
- **No CC pin**: it cannot read the USB-C source's current advertisement.

Settings:

| Item | V1 value | Basis |
|---|---|---|
| RISET (charge current) | **1.27 kΩ, 1 % → about 0.70 A** (0.63–0.77 A over the KISET range). A 887 Ω resistor would give about 1.0 A (0.90–1.10 A) | ICHG = KISET / RISET, KISET 797/890/975 AΩ [P]. Thermal [calc]: at 1 A charge with 5 V in, 4.7 V OUT and a 3.4 V battery the charger dissipates about 1.6 W (about +71 °C at the JEDEC θJA of 44.5 °C/W), so 0.7 A is the starting value |
| Precharge | about 70 mA (88/1.27k) | KPRECHG 70/88/106 |
| Termination | fixed at 0.1 × ICHG in USB500/ISET modes | BQ24075 has no ITERM pin |
| EN1 / EN2 | **EN1 pulled high, EN2 low by default = USB500 (500 mA)**. After the MCU reads CC and sees an advertised 1.5 A or 3 A source, it drives EN2 high to use the resistor-set limit | EN pins have ≈285 kΩ internal pull-downs; never float |
| RILIM (when EN2 high) | **1.2 kΩ → 1.34 A typ (1.25–1.43 A)** for a 1.5 A source | IIN-MAX = KILIM / RILIM, KILIM 1500/1610/1720 AΩ; note the datasheet's design example uses 1550 |
| RTMR | **60.4 kΩ** → fast-charge timer about 8 h typ (6 h min), precharge about 48 min | tMAXCHG = 10 × KTMR × RTMR; the 5 h default could expire during a charge slowed by system load |
| TS | no NTC on the cell assumed: **10 kΩ fixed resistor from TS to VSS** | datasheet's no-NTC option; confirm the cell pack really has no thermistor |
| CE | pulled low (enabled) with MCU override | internal ≈285 kΩ pull-down; do not float |
| SYSOFF | pull-up as supplied (≈5 MΩ to VBAT), MCU can release; used for **ship mode** | disconnects the battery from OUT; waking needs a button or a USB plug [K] |
| PGOOD, CHG | open-drain, pulled up to 3V3_SYS (1–100 kΩ) | MCU reads them; CHG flashes at 2 Hz on a timer fault |
| Capacitors | IN 1 µF, OUT 4.7 µF, BAT 4.7 µF (typical application); IN ≤ 10 µF | Fig. 10-1 |
| USB-C | **5.1 kΩ from CC1 and CC2 to ground** (sink only); ESD protection on VBUS and CC | USB Type-C spec not retrieved; MCU ADC reads CC voltage to learn the source's advertised current [K] |

Budget at the USB port [calc, bus ≈ 4.7 V]: 3.3 V at 0.4 A is 0.30 A of bus current; adding 5 V at 0.5 A raises it to 0.86 A; adding 0.7 A of charging makes it about 1.6 A, above the 1.5 A limit, so the charger reduces charge current (DPPM at 4.3 V) before the battery supplements. At full load (3.3 V 1 A plus 5 V 2 A) the bus current would be 3 A, beyond the charger's 1.5 A maximum; the battery then supplies the difference.

## 3. Fuel gauge: MAX17048

Part: MAX17048G+T10 (TDFN-8 2×2 mm); Evelta ₹507.45 ex GST (₹598.79 incl.), stock ambiguous; 7Semi breakout at Hubtronics out of stock. Facts [P, SparkFun mirror of Rev 7, 11/16; analog.com unreachable]:
- I²C address 0x36; 400 kHz max; VDD 2.5–4.5 V and VDD is also the cell voltage sense input; **no sense resistor**; 23 µA typical active, 3 µA hibernate.
- Voltage error ±7.5 mV per cell at 3.6 V, 25 °C; **voltage-only gauge**: while charging or discharging and for about 30 min after, VCELL and OCV differ, so SOC reads high while charging at 0.7 A and low under a large load.
- ALRT is open-drain, active low, enabled by default (can fire at power-up); five alert sources (low SOC, 1 % change, voltage reset, over- and under-voltage).
- Connect VDD to the **BAT node** (not OUT, which can sit near or above 4.5 V on USB), 0.1 µF close to the pin, pull-ups on SDA/SCL/ALRT.
- Update RCOMP at least once a minute if temperature compensation is wanted; the default model "performs well for some batteries" only.
- The datasheet says nothing about power-path chargers.
BQ27441 alternative (impedance track, coulomb counter, needs a 10 mΩ sense resistor, 93 µA normal, SON-12) is more accurate with a load but costs more power and area; not chosen.

## 4. 3.3 V rails

Candidates [P unless noted]:

| | TLV62568 | TPS62822 |
|---|---|---|
| Package | SOT-23-5 (hand-solderable) | QFN-8, 2×1.5 mm (hot air) |
| Vin | 2.5–5.5 V | 2.4–5.5 V |
| Iout | 1 A | 2 A |
| Output | adjustable 0.6 V to VIN (no fixed 3.3 V version) | adjustable 0.6–4 V |
| Switching | 1.5 MHz | 2.2 MHz |
| 100 % duty (dropout mode) | yes | yes |
| Quiescent | 35 µA | 4 µA |
| Inductor | 2.2 µH | 0.47 µH (1 µH allowed) |
| Indian stock | Evelta ₹12.86 incl., **38 pcs** | Evelta ₹52.26 ex GST, **4 pcs** |
| Divider (3.3 V) | VOUT = 0.6 V × (1 + R1/R2); R2 ≤ 200 kΩ | R1 = R2 × (VOUT/0.6 − 1); R2 ≤ 120 kΩ |

Dropout [calc, datasheet formulas, typical RDS(on) at 5 V, assumed inductor DCR, plus the 50 mV BAT-to-OUT drop]:

| Converter | Battery voltage below which 3.3 V is lost |
|---|---|
| TPS62822 | 3.34 V at 0.4 A; 3.39 V typ (3.44 V max drop) at 1 A |
| TLV62568 | 3.40–3.42 V at 0.4 A; 3.55–3.65 V at 1 A depending on assumed inductor resistance |

Conclusion: with either part, 3.3 V cannot be held at 1 A on a 3.0 V cell; the firmware must warn and shut down before brownout, and the lowest usable battery voltage is about 3.4 V at typical load. A buck-boost would extend this; none was found in India. **V1 choice (PROPOSED): two TLV62568 (stocked, hand-solderable, Isat of the inductor to be checked), with the TPS62822 as the upgrade for a hot-air build once its stock is confirmed.** The usable capacity lost below 3.4 V is not in the datasheets [N].
Inductor: ElectronicsComp CD54 2.2 µH (₹11 ex GST, 1,244 available; 1.5 A rated, DCR 105 mΩ, **saturation current not listed**). The TLV62568 datasheet recommends other inductors by name; check Isat before use.
Recommended capacitors: 4.7 µF in, 10–47 µF out.

## 5. 5 V boost

| | TPS61088 (data from the TPS61088-Q1 sheet, SLVSE52A) | TPS61023 (SLVSF14B, Aug 2020) |
|---|---|---|
| Package | VQFN-20 | SOT-563 |
| Vin | 2.7–12 V | 0.5–5.5 V (start-up needs 1.8 V) |
| Current limit | resistor-set; 82 kΩ gives 6.7 A typ, 5.2 A min (agent's calc for 5 V / 2 A) | fixed valley limit 2.7 A min / 3.7 A typ |
| Output at Vin = 3.0 V | 5 V / 2 A is within range [calc]; input 3.7 A DC at 2 A out | 5 V / 2.37 A at the 3.7 A limit, but only 1.83 A guaranteed at the 2.7 A minimum limit [calc]; reference design is 5 V / 1.5 A |
| True disconnect in shutdown | **not found**; datasheet implies a body-diode path (my inference) | **yes** ("true disconnection between input and output during shutdown") |
| Pass-through (Vin > Vout) | not documented | yes |
| Efficiency at 5 V out [read from graphs, ±2–3 %] | about 95–97 % from 0.5 to 2 A | about 92–93 % at 3.0 V in, 94–95 % at 3.6 V, 96 % at 4.2 V |
| Indian stock | Evelta ₹112.10 incl., 20 pcs | **bare IC not found**; 7Semi module ₹86 at Hubtronics (out of stock), ₹79 at Robocraze (snippet) |

V1 (PROPOSED): **TPS61023 module for the prototype**, 5 V budget **1.5 A** (matches the datasheet reference design); **TPS61088 for a hot-air custom PCB**, possible 2 A, with the datasheet's non-Q1 version still to be read and the compensation values for a 5 V output still to be found [N]. Because the TPS61088 has no confirmed disconnect, nothing but the per-port switches may hang on the 5 V rail; when the boost is disabled, the rail sits near the battery voltage and the port switches are off.
MT3608 is **not** used (no load disconnect; 2 A output rating vs about 2 A input at 3.0 V and 1 A out).

## 6. Calculations (agent, stated assumptions)

Assumptions: 3.0 Ah × 3.7 V = 11.1 Wh cell; BAT-to-OUT resistance 50 mΩ; 3.3 V buck 95 % efficient; 5 V boost 93/94/95 % (TPS61088) or 90/93/95 % (TPS61023) at 3.0/3.6/4.2 V.

| Vbat | 3.3 V @ 1 A | 5 V @ 2 A (TPS61088) | 3.3 V @ 1 A + 5 V @ 2 A |
|---|---|---|---|
| 3.0 V | dropout, not regulated | 3.83 A | n/a |
| 3.6 V | 0.98 A | 3.09 A | 4.16 A (about 1.4 C on 3000 mAh) |
| 4.2 V | 0.84 A | 2.59 A | 3.48 A |

- Runtime on battery: system 0.4 A at 3.3 V alone: about 8.0 h (7.2 h at 90 % usable); plus 0.5 A average at 5 V: about 2.7 h; plus 1 A average at 5 V: about 1.65 h. The last few percent below 3.4 V are lost.
- Charge time at 1 A: at least 3 h constant-current plus a taper (estimated 3.5–4 h total; not in the datasheet); at the V1 setting of about 0.7 A allow about 5 h or more, and more again under load.
- The 4.16 A worst case is under the charger's 4.5 A recommended BAT-pin limit but is a high C-rate for a typical protected pouch cell; the cell's continuous discharge rating is not published on the pages found. **The power manager must cap total draw.**

## 7. Per-port power switching and sensing

Defined in `08-smis-v0.2.md` §7: P-FET high-side switches (Si2333CDS-T1-GE3 and BSS138 level shifters), INA219 sensing on 5V_P, resettable fuses, ESD. Notes from the datasheets:
- Si2333CDS: Vds −12 V, Rds(on) max 35 mΩ at −4.5 V gate drive, 59 mΩ at −1.8 V.
- A 3.3 V GPIO cannot turn off a P-FET whose source is at 5 V (gate swing only 1.7 V for a threshold up to 1.3 V on AO3401-class parts), hence the level shifter.
- PCA9535: VCC 2.3–5.5 V, address 0x20–0x27, **all outputs are inputs at power-on, no internal pull-ups**, so gate nets need pull-downs; 25 mA per pin sink, INT is open-drain. Known erratum: INT can be wrongly cleared if the last command byte written was 00h and another slave acknowledges; write a non-zero command byte after reads. PCA9535 in SOIC-24: Evelta ₹193.37 incl., 261 pcs.
- INA219 (16 addresses, 12-bit, 26 V bus): board-level accuracy is stated as 0.5–1 % on the Indian modules; gain setting for a 0.1 Ω shunt at 0.5 A to be verified.

## 8. Load shedding and protection policy (firmware)

1. Below a warning battery voltage (about 3.45 V as measured by the MAX17048, to leave margin for the dropout above): stop transmit features, power off 5V_P ports, warn the user.
2. Below shutdown voltage (about 3.40 V): save state and enter ship mode through SYSOFF.
3. Over-current or over-temperature on a port: that port to FAULT; the rest continue.
4. If the USB source is limited (default USB500): reduce charge current and refuse new ports whose requests exceed the bus budget.
5. Never enable a port that the budget cannot support.

## 9. BOM candidates (Indian-stocked, opened pages unless noted; nothing ordered)

| Function | Part | Seller | Price | Stock | Note |
|---|---|---|---|---|---|
| Charger | BQ24075RGTR | Evelta | ₹85.24 incl. | ambiguous | VQFN-16 |
| Fuel gauge | MAX17048G+T10 | Evelta | ₹598.79 incl. | ambiguous | TDFN-8 |
| 3.3 V buck | TLV62568DBVR (×2) | Evelta | ₹12.86 incl. | 38 | SOT-23-5 |
| 3.3 V buck (alt.) | TPS62822DLCR | Evelta | ₹52.26 ex | 4 | QFN-8 |
| 5 V boost | TPS61088RHLR | Evelta | ₹112.10 incl. | 20 | VQFN-20 |
| 5 V boost module | TPS61023 (7Semi) | Hubtronics / Robocraze | ₹86 / ₹79 | out / "51 left" (snippet) | prototype |
| Expander | PCA9535DWR (×2) | Evelta | ₹193.37 incl. | 261 | SOIC-24 |
| Port FET | Si2333CDS-T1-GE3 | Hubtronics | ₹8.85 incl. | 2,887 | SOT-23 |
| Level shifter FET | BSS138 | Hubtronics | ₹5.02 incl. | not shown | |
| Current monitor | INA219 module | ElectronicsComp | ₹95 ex | 219 | |
| Shunt 0.1 Ω 3 W 2512 | — | DNA Tech | ₹21.12 ex | 46 | |
| Fuse (PTC) | WT1206-050 ×5 | Hubtronics | ₹49 per 5 incl. | 743 | hold current to check |
| ESD | USBLC6-2SC6 | DNA Tech | ₹31.86 incl. | 18 | |
| ESD (4-line) | SRV05-4 | DNA Tech | ₹20 ex | 100 | |
| USB-C receptacle | 16-pin SMD | Evelta | ₹7.75 ex | 494 | |
| Inductor 2.2 µH | CD54 | ElectronicsComp | ₹11 ex | 1,244 | check Isat |
| Cell | 3.7 V 3000 mAh pouch, JST-PH 2 mm | Probots KP-355085 / KP-045090 | ₹529 | out of stock | ask for datasheet, polarity, BIS number |

## 10. Test plan

1. Rail bring-up with a bench supply in place of the cell: 3V3_SYS, 3V3_IO, 5 V voltage, ripple and start-up.
2. Charger: charge current vs RISET, termination, timer, thermal rise at 0.7 A, behaviour with no battery, SYSOFF ship mode and wake.
3. USB: default 500 mA limit, CC reading, switch to 1.5 A, DPPM behaviour when the system load exceeds the input.
4. Brown-out: Wi-Fi TX bursts, sd card writes, radio bursts, and the 5 V rail at full load, while the battery sags to 3.4 V.
5. Fuel gauge: SOC while charging and under load, ALRT thresholds.
6. Per-port switches: soft start, trip current and response, fault isolation (see SMIS test plan).
7. Cell at full load: confirm the pack's protection does not trip at the worst-case 4.2 A.

## 11. Risks and unknowns

- Evelta stock for the charger, fuel gauge and converters is ambiguous; confirm with Evelta before relying on it.
- Non-Q1 TPS61088 and TCA9535/PCA9555 datasheets not read; TPS61088 compensation values for 5 V not found.
- The 3.3 V rail is lost at about 3.4–3.6 V battery under load; usable capacity below that is unquantified.
- High C-rate at the 4.16 A worst case; the cell's continuous rating is unpublished.
- The charger dissipation at 1 A (about 1.6 W) is a JEDEC estimate; real boards differ.
- USB Type-C Rp advertisement details were not retrieved; reading CC with the ADC is my proposal.
- No BIS registration, ETA or e-waste position is settled (see `07-india-regulatory.md`); a charger sold with the device is its own BIS item.
- Two bucks, a boost and a charger on one board need disciplined layout (switching nodes away from the RF and analog sections); layout rules are still to be written.
