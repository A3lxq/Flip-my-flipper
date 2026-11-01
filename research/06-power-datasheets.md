# Power IC datasheet facts and calculations

Condensed from a research-agent report. Documents: BQ24072/3/4/5/9 SLUS810N (Oct 2021) https://www.ti.com/lit/ds/symlink/bq24075.pdf ; BQ24070/71 SLUS694G (only skimmed); TLV62568 SLVSD89B; TLV62566 SLVSBC1D; TPS62822 SLVSDV6C; TPS61023 SLVSF14B (Aug 2020); **TPS61088-Q1** SLVSE52A used as a proxy because the plain TPS61088 URL returned 404; PCA9535 SCPS129K (Mar 2021); MAX17048/49 Rev 7 (11/16) from a SparkFun mirror (analog.com unreachable); BQ27441-G1 SLUSBH1C (brief). TCA9535 and PCA9555 not retrieved. Page numbers ±1; graph readings ±2–3 %.

## BQ24075
- OUT is 5.4–5.6 V only when VIN > VOUT + dropout. On 5 V USB the input FET is in dropout (VDO(IN-OUT) 300 mV typ / 475 mV max at 4.3 V, 1 A), so OUT ≈ VBUS − 0.3 to 0.5 V under load (estimate). On battery OUT ≈ VBAT − 50 mV typ (100 mV max) at 1 A. The charger is linear: input current = charge current + system load.
- ISET: 590 Ω–8.9 kΩ, ICHG = KISET/RISET, KISET 797/890/975 AΩ, range 100–1500 mA, 1 % resistor. Precharge IPRECHG = KPRECHG/RISET (70/88/106 AΩ). ILIM: 1.1–8 kΩ, IIN-MAX = KILIM/RILIM, KILIM 1500/1610/1720 AΩ (design example uses 1550). EN1/EN2: 00 USB100, 01 USB500, 10 resistor-set, 11 standby; internal ≈285 kΩ pull-downs. No ITERM pin (termination 0.1×ICHG). TMR 18–72 kΩ, tMAXCHG = 10×KTMR×RTMR, KTMR 36/48/60 s/kΩ; floating = 5 h. TS needs a 10 kΩ NTC or a 10 kΩ fixed resistor to VSS. CE and SYSOFF must not float. PGOOD/CHG open-drain.
- Input 4.35–6.4 V, OVP 6.6 V; VBAT(REG) 4.20 V; precharge below 3.0 V; recharge at VBAT(REG) − 100 mV; battery-supplement entry at VOUT ≤ VBAT − 40 mV; DPPM 4.3 V; thermal regulation at 125 °C, shutdown 155 °C; θJA 44.5 °C/W; sleep current 4.3 µA typ. Capacitors: IN 1 µF, OUT 4.7 µF, BAT 4.7 µF (typical application). Typical application RILIM 1.18 kΩ, RISET 1.13 kΩ, RTMR 46.4 kΩ.
- Derived settings for a 3000–3500 mAh cell: RISET 887 Ω → about 1.0 A (0.90–1.10); 1.27 kΩ → about 0.70 A. RILIM 1.1 kΩ → 1.46 A typ (1.36–1.56); 1.2 kΩ → 1.34 A typ (1.25–1.43); 1.8 kΩ → 0.894 A (0.83–0.96). RTMR 60.4 kΩ → 8.05 h typ fast-charge timer. Thermal at 1 A charge (5 V in, 4.7 V OUT, 3.4 V battery): about 1.6 W (+71 °C using θJA); at 0.7 A about 1.1 W.
- Ship mode: SYSOFF high turns off the battery-to-OUT FET; waking by button or USB plug is the agent's inference.
- Family: BQ24072 VOUT = VBAT + 225 mV; BQ24073/4 4.4 V (BQ24074 OVP 10.5 V, ITERM resistor); BQ24075 5.5 V, DPPM 4.3 V, SYSOFF; BQ24079 4.1 V cell. BQ24070 (VQFN-20, VCC 4.35–16 V, up to 2 A total, charge 100–1500 mA) not studied in depth.

## 3.3 V buck candidates
| | TLV62568 (DBV) | TLV62566 | TPS62822 |
|---|---|---|---|
| Vin | 2.5–5.5 V | 2.7–5.5 V | 2.4–5.5 V |
| Iout | 1 A | 1.5 A | 2 A |
| Frequency | 1.5 MHz | 1.5 MHz | 2.2 MHz |
| Output | adjustable, VFB 0.6 V; no fixed 3.3 V version | adjustable | adjustable 0.6–4 V |
| 100 % duty | yes | no (95 % max) | yes |
| Quiescent | 35 µA | 50 µA | 4 µA |
| Inductor / caps | 2.2 µH; 4.7 µF in, 10–47 µF out | 2.2 µH | 0.47 µH (1 µH allowed); 4.7 µF in, 10 µF out |
| Package | SOT-23-5 | SOT-23-5 | QFN-8 2×1.5 mm |
Dropout (calculated with datasheet formulas, typical RDS(on) at 5 V, assumed inductor DCR, plus 50 mV BAT-to-OUT): battery voltage needed for 3.3 V at 1 A: TPS62822 3.39 V typ (3.44 max drop); TLV62568 3.55–3.65 V; TLV62566 ≥ 3.47 V. At 0.4 A: TPS62822 3.34 V; TLV62568 3.40–3.42 V. Conclusion: none holds 3.3 V at 1 A on a 3.0 V cell.

## 5 V boost
| | TPS61088(-Q1) | TPS61023 |
|---|---|---|
| Vin | 2.7–12 V | 0.5–5.5 V (start-up 1.8 V) |
| Current limit | resistor-set, ILIM = 550000/RILIM (PFM), 82 kΩ gives about 6.7 A | fixed valley 2.7 A min / 3.7 A typ |
| Load disconnect | not found (body-diode path, inference) | **yes**, true disconnection in shutdown |
| Pass-through | not documented | yes |
| Output at Vin 3.0 V | 5 V / 2 A within range | 2.37 A at 3.7 A limit; only 1.83 A guaranteed at 2.7 A |
| Efficiency 5 V out | about 95–97 % (0.5–2 A) | about 92–93 % (3.0 V in), 94–95 % (3.6 V), 96 % (4.2 V) |
Inductors: TPS61088 0.47–10 µH (e.g. 1.2 µH Sumida CDMC8D28NP-1R2MC); TPS61023 0.37–2.9 µH (1 µH Coilcraft XEL4030-102ME). TPS61088 compensation values for a 5 V output not found.

## MAX17048 (Rev 7)
I²C 0x36, 400 kHz; VDD 2.5–4.5 V and also the cell sense input; no sense resistor; active 23 µA, hibernate 3 µA; ±7.5 mV per cell at 3.6 V; voltage-only gauge (VCELL differs from OCV during and about 30 min after charge/discharge); ALRT open-drain active low, enabled by default, five sources; hibernate and sleep modes; quick-start "use with caution"; RCOMP update at least once a minute. Connect VDD to the battery node, 0.1 µF at the pin. BQ27441-G1: address 0x55, Impedance Track, 10 mΩ sense resistor, normal 93 µA.

## PCA9535 (SOIC-24)
VCC 2.3–5.5 V; 400 kHz; address 0x20–0x27; IOL 25 mA per pin (100 mA per octal, 200 mA device); **all pins are inputs at power-on**, config registers default 0xFF, no internal pull-ups; POR needs VCC below 0.2 V; open-drain INT (3 mA), triggered by input edges only; erratum: INT can be wrongly cleared if the last command byte written was 00h and another slave acknowledges.

## Calculations (stated assumptions)
Cell 3.0 Ah × 3.7 V = 11.1 Wh; BAT-to-OUT 50 mΩ; 3.3 V buck 95 %; boost 93/94/95 % (TPS61088) or 90/93/95 % (TPS61023) at 3.0/3.6/4.2 V.
| Vbat | 3.3 V @ 1 A | 5 V @ 2 A (TPS61088) | both |
|---|---|---|---|
| 3.0 V | dropout | 3.83 A | n/a |
| 3.6 V | 0.98 A | 3.09 A | 4.16 A |
| 4.2 V | 0.84 A | 2.59 A | 3.48 A |
Runtime: system 0.4 A at 3.3 V ≈ 8.0 h; plus 0.5 A at 5 V ≈ 2.7 h; plus 1 A at 5 V ≈ 1.65 h. Charge at 1 A: ≥ 3 h constant-current plus taper (estimate 3.5–4 h total). USB bus current (bus ≈ 4.7 V): 3.3 V 0.4 A → 0.30 A; plus 5 V 0.5 A → 0.86 A; plus 1 A charge → 1.86 A (above the 1.5 A limit); full load 3.0 A.

## Unknowns
Non-Q1 TPS61088 datasheet; MAX17048 official datasheet; BQ24075 VDO at > 1 A; TLV62568 RDS(on) below 5 V; TPS61088 compensation for 5 V; TPS61023 maximum current limit; USB Type-C Rp details; cell C-rate limits and usable capacity below 3.4 V; BQ24070 behaviour; TCA9535/PCA9555 datasheets; Indian stock.
