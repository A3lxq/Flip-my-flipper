# Per-port protection, ID EEPROMs, ESD, crystals and connectors (Indian stock)

Condensed from a research-agent report. DNA Tech, ElectronicsComp, Hubtronics and Sunrom site searches worked; Evelta and Probots site searches ignored queries (web search restricted to their domains used); Robu returned 403 (snippets only, unconfirmed). Prices ex-GST unless stated; DNA Tech, Hubtronics and Evelta add 18 %; Sunrom does not say whether prices include GST.

## Current-limited switches with fault flag
No Indian-stocked 0.5–1 A USB-style limiter with a fault flag in confirmed stock. Options:
- **Hubtronics TPS1HC100BQPWPRQ1** (TI automotive high-side switch, 100 mΩ): ₹83 incl. GST, 49 in stock. Supply 3–28 V; current limit set by a resistor, 0.633–6.9 A (±18 % at 1.9 A); open-drain status output; analog current sense (±6 % at 1 A); HTSSOP-14 with exposed pad. 12 V automotive part; 5 V behaviour not verified. https://hubtronics.in/tps1hc100bqpwprq1
- **Hubtronics TPD3S014**: ₹176, 1 in stock, current limit 0.65–1.05 A, 0.5 A continuous, **no fault pin**.
- **Evelta AP2337SA-7**: ₹24.78 incl., stock ambiguous, no fault flag or enable.
- **DNA Tech TPS2041B**: ₹109.38 ex, out of stock (1 A typ limit, OC flag). TPS22810DBVR plain load switch ₹155.25 ex, 20 in stock (no limit, no flag).
- **Lion Circuits AP2151AW-7**: ₹49.71, "In Stock", ships in 7–10 days; ship-from not stated, so import-suspect. Limit 0.6/0.8/1.0 A at 5 V, open-drain FLG, 7 ms deglitch (datasheet is for the AP2151A).
Not found at any searched seller: TPS2051/2065/2557, MIC2025/2026, AP2171/2191/22615, SY6280, NCP380, eFuse/hot-swap ICs.

## Discrete alternative
- P-FETs: **Hubtronics Si2333CDS-T1-GE3** ₹8.85 incl., 2,887 in stock (Vds −12 V, Rds(on) max 35 mΩ at −4.5 V, 59 mΩ at −1.8 V); AO3401 (Hubtronics ₹5.90, 2,403; Sunrom ₹7.19, min 10, 1,900; Rds(on) < 60 mΩ at −4.5 V, Vgs(th) up to −1.3 V); Evelta DMG2305UX-13 ambiguous stock. A 5 V-source P-FET cannot be turned off by a 3.3 V GPIO (gate swing 1.7 V), so use an N-FET/NPN level shifter (BSS138 at Hubtronics ₹5.02).
- Current sensing: INA219 modules at ElectronicsComp (CJMCU-219 ₹95, 219 available), DNA Tech (₹113, 10), Evelta 7Semi (₹205, 124); IC at Hubtronics (₹99.15, 7). 16 I²C addresses. INA226 only out-of-stock at Probots; INA180 snippet only. Shunt 0.1 Ω 3 W 2512 at DNA Tech ₹21.12 (46).
- PTC fuses: Hubtronics WT1206-050 (5 pcs ₹49, 743 in stock; hold current not on the page), Sunrom Bourns MF-PSMF050X-2 0.5 A (₹13.28, 4,330), Evelta SMD0805B050TF (hold 0.5 A, trip 1 A; stock ambiguous). A PTC gives no fault signal by itself.

## ID EEPROMs
DS2431, DS28E07, DS2502, DS24B33, AT21CS01/11: **not found** at DNA Tech, ElectronicsComp, Hubtronics, Sunrom, Evelta; Robu snippets list DS2431 (₹119), DS24B33, AT21CS01 (unconfirmed). 24-series I²C EEPROMs confirmed: ElectronicsComp 24C02 DIP-8 (₹11, 1,036), M24C04-WMN6P SOIC-8 (₹17, 154); DNA Tech AT24C04 DIP-8 (₹21, 7). Fixed addresses (A0–A2, at most 8) collide for identical modules on one bus.

## ESD / TVS
USBLC6-2SC6: DNA Tech ₹27 ex (18); Evelta ₹14 (ambiguous). SRV05-4: DNA Tech ₹20 (100); Sunrom ₹27.14 (1,300). Evelta TPD4E02B04DQAR USB-C 4-channel ₹35 (521, USON-10, hard to solder). PESD5V2S2UT Evelta (3). ESDA5V3L DNA Tech ₹39.55 (14). 5.1 kΩ CC resistors were not specifically searched.

## Crystals and passives
27.12 MHz: Evelta YSX530GA 20 pF 10 ppm ₹30.45 (40); DNA Tech HC49 through-hole 20 pF 20 ppm ₹14 (50); Epson FA-128 out of stock. ST25R3916 load capacitance unverified. 8 MHz: DNA Tech HC49 SMD ₹14.40 (10). 25 MHz: ElectronicsComp YSX321SL 12 pF ₹29 (16). 32.768 kHz: DNA Tech cylinder ₹5.25 (600); ElectronicsComp CFS206 ₹13 (15). Inductors: ElectronicsComp CD54 2.2 µH ₹11 (1,244; 1.5 A rated, DCR 105 mΩ, saturation current not listed); CDRH104R/CDRH127 also listed. MLCCs: generic Evelta/Probots/Hubtronics listings.

## Board-to-board
Generic Berg-strip headers only: Evelta 2.0 mm 2×40 female 4 mm height ₹28 (669); Evelta 1.27 mm 2×40 male SMT ₹39 (300); ElectronicsComp 1.27 mm 2×40 female 7 mm ₹59 (53); Sunrom 1.27 mm 40×2 SMD. 0.8 mm board-to-board: not found. Mating compatibility between sellers unverified; none is controlled-impedance.

## Recommendations
Best confirmed protection switch: Hubtronics TPS1HC100 (verify 5 V, hard to solder), else the discrete P-FET + INA219 + PTC build. ID: 24C02/M24C04 with per-port addressing. ESD: DNA Tech USBLC6/SRV05-4. Gaps: USB-style limiter ICs, 1-wire ID chips, INA226 in stock, 0.8 mm board-to-board, 5.1 kΩ resistor stock.
