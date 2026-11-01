# Deeper India sourcing and compatibility check (2026-11-01)

Status: PROPOSED findings. Produced by four parallel research agents plus my own earlier checks. I have not independently re-verified the agents' figures. Rule R17 still applies: DigiKey India, Mouser India, Tanotis, element14/Farnell and overseas sellers are imports. "Not found" is never treated as "import-only".

Blocked or not searched in every area: Robu (HTTP 403), Robocraze (429), Robodo (429), Thingbits, Rhydolabz, Silverline, Sunrom (partly), Tanna TechBiz, IndiaMART. Evelta stock labels are contradictory on many ICs ("in stock" next to "Sold Out"): treat as unconfirmed until Evelta confirms by email.

## 1. Summary: part by part

| Function | Chosen/candidate part | Indian source status | Compatibility | Action |
|---|---|---|---|---|
| MCU | STM32H743IIT6 / F429ZIT6 | H743 none confirmed; F429ZIT6 at DNA Tech ₹649 (importer ElectroSource) and IndiaMART | see 02, 03 | Seller quotes; ST authenticity proof |
| Wi-Fi/BLE | ESP32-S3-WROOM-1 | Available (DNA Tech ₹379.96, 30 in stock) | OK with caveats: own 3.3 V rail ≥500 mA, strapping pins GPIO0/3/45/46, no India WPC/ETA found | Dedicated rail; ask about WPC |
| Sub-GHz | CC1101 868 MHz module | Available (Robu snippet ₹267; Electropi out of stock) | OK with caveats: 3.3 V only, SPI ≤ 6.5–10 MHz, pinout differs by seller, power must be capped for India rules | Buy 868 MHz; cap TX power in firmware |
| NFC | ST25R3916 | **No Indian seller found** (DigiKey India, Mouser India, Tanotis, Elechouse only) | n/a | Fallback PN532 (DNA Tech ₹317, 50 in stock): loses ISO15693; RC522 (Probots ₹139) loses much more |
| LF RFID | RDM6300 | Available (about ₹210–265) | EM4100 only; 5 V supply; TX level unverified | Measure TX; level-shift |
| IR RX | TSOP1738 | Available (₹24–35) | Datasheet seen says 4.5–5.5 V, not 3.3 V | Use a 2.5–5.5 V variant or 5 V supply |
| Display | Waveshare 3.5" ST7796S (touch version) | Available (Zbotic, Evelta, Hubtronics about ₹1,650–1,994) | OK: 3.3 V, RGB565 over SPI; SPI clock and backlight current not published | Bench test |
| LiPo cell | 3000 mAh pouch | Probots KP-355085 ₹529 (out of stock), KP-045090; DNA Tech 3000 mAh | JST-PH 2 mm; cutoff, max discharge, polarity, BIS not published | Ask seller for datasheet and BIS no. |
| Charger + power path | BQ24075 (VQFN-16) | Evelta ₹85.24 incl. GST, **stock ambiguous**; BQ24070 217 pcs; SparkFun BQ24075 board ₹2,772 (19) | Input 4.35–6.6 V, 1.5 A charge, 4.2 V, SYSOFF pin | Confirm stock with Evelta; reflow only |
| 5 V boost | TPS61023 | Bare IC not found; 7Semi module ₹79–86 (Robocraze snippet, Hubtronics out of stock); TPS61088 Evelta ₹112 incl. GST, 20 pcs, VQFN-20 | TPS61023 has true disconnect in shutdown, 3.7 A; MT3608 has none | Prefer TPS61088 or TPS61023 module for prototype; avoid MT3608 for the switched rail |
| 3.3 V rail | TLV62568 buck (SOT-23-5) | Evelta ₹12.86 incl. GST, 38 pcs | 1 A buck; holds 3.3 V only while cell ≳3.4 V (not read in datasheet) | Read datasheet; buck-boost not found in India |
| Per-port load switch + fault | TPS2553/AP2553-class | **None found**; TPS2041B DNA Tech out of stock | n/a | Ask DNA Tech/Evelta; find alternative |
| Fuel gauge | MAX17048 | Evelta ₹598.79, stock ambiguous; 7Semi board Hubtronics out of stock | I²C 0x36; range disputed (4.2 vs 4.5 V) | Read datasheet; confirm stock |
| I²C expander | PCA9535DWR (SOIC-24) | Evelta ₹193.37 incl. GST, 261 pcs; MCP23017-E/SO DNA Tech ₹206.50, 30 pcs | 3.3 V OK, 8 per bus | Use PCA9535 first, MCP23017 as second source |
| USB-C | 16-pin SMD receptacle | Evelta ₹7.75 ex GST, 494 pcs | 5.1 kΩ on each CC for 5 V sink | OK |
| Module connectors | JST SH 1.0 mm | Only generic clones (Hubtronics; 6-pin out of stock); genuine not confirmed | 1 A contact marginal for 0.5 A on SM-S 5 V pin | Prefer GH 1.25 mm, XH 2.5 mm or 2.54 mm box header |
| Core-module connector | 2×30 2.54 mm socket | Evelta ₹410.64 incl. GST, 22 pcs | marginal for 20–40 MHz SPI and 25 MHz SDIO | interleave grounds; keep short |
| microSD socket | TF push-push | DNA Tech ₹29.50, 10 in stock (SMD not confirmed) | | confirm footprint |
| Buttons, buzzer, vibration | 6×6 SMD tact, piezo, coin ERM | Hubtronics, Probots in stock | | OK |

## 2. Findings that change the design

1. **Charger:** my earlier "import only" for the BQ2407x family was too strong. **BQ24075** is listed at Evelta (₹85.24) but its stock is contradictory. TP4056 has no power path and must not be used. IP5306 (DNA Tech, ₹63.72) is a power-bank chip with a 5 V output only, not suitable as the main power manager.
2. **5 V rail:** MT3608 is out. It has no load disconnect (the diode and inductor keep input connected to output in shutdown) and 5 V at 1 A from 3.0 V needs about 2 A from the cell against a "2 A" datasheet rating. Use a part with true disconnect: TPS61023 (bare IC not found in India; module available) or TPS61088.
3. **3.3 V rail:** AP2112K is only 600 mA, not 1 A. AMS1117/AZ1117 need about 1.1 V headroom and fail near 4.4 V cell. TLV62568 (1 A buck) is the Indian-stocked pick. If 3.3 V must hold down to a 3.0 V cell, a buck-boost is needed and none was found in India.
4. **Per-port load switch:** gap. Eight ports each need a current-limited switch with a fault output. If none is found in India, a fallback is a plain load switch (TPS22810 at DNA Tech, ₹155.25 ex GST, no current limit) plus a current-sense resistor and the fuel/power manager, or one limited switch per group, which weakens port protection. OPEN.
5. **Connector family:** pick GH 1.25 mm or XH 2.5 mm / box header over JST SH for SM-S. Genuine SH is not confirmed in India, and 1 A per contact at 0.5 A load is marginal with the thin wire SH needs.
6. **CC1101:** buy the 868 MHz variant; firmware must cap power. The Gazette G.S.R. 853(E) (10 December 2021) as reported by the agent limits non-specific 865–868 MHz devices to 25 mW e.r.p., requires type approval, and does not mention 433 MHz. I have not read it myself and draw no legal conclusion; regulatory research is still pending.
7. **ESP32-S3:** give it its own regulator. Wi-Fi TX peaks at 355 mA.
8. **IR receiver:** do not use a TSOP rated 4.5–5.5 V on 3.3 V without checking a newer datasheet.
9. **NFC:** ST25R3916 stays "no Indian source found". Whether to accept a PN532 module, or buy the chip as an import, is a decision for you (it conflicts with R17).

## 3. Datasheet facts reported by the agents (sources they cited)

- ESP32-S3-WROOM-1 v1.8: VDD33 3.0–3.6 V, external supply ≥0.5 A, Wi-Fi TX peaks 355 mA (11b), BLE TX 344 mA at +20 dBm, not 5 V tolerant, strapping GPIO0/3/45/46, console UART0 on GPIO43/44, IO35–37 unavailable on octal-PSRAM (R8) parts. https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
- CC1101 (TI SWRS061I): 1.8–3.6 V, I/O not 5 V tolerant, SPI 10 MHz with 100 ns byte gap (9 MHz single / 6.5 MHz burst without), bands 300–348 / 387–464 / 779–928 MHz, matching network is band-specific. https://www.ti.com/lit/ds/symlink/cc1101.pdf
- TI bq2407x family: IN 4.35–6.6 V (10.5 V on bq24074), charge up to 1.5 A, 4.2 V; bq24075 OUT 5.5 V when adapter present, SYSOFF input. https://www.ti.com/lit/ds/symlink/bq24075.pdf
- TPS61023: 0.5–5.5 V in, 3.7 A valley limit, true disconnect in shutdown, 1.8 V start-up. https://www.ti.com/lit/ds/symlink/tps61023.pdf
- MT3608: 2–24 V in, 4 A switch, 2 A output quoted by module vendor, no load disconnect (topology).
- AP2112: 600 mA LDO. https://www.diodes.com/assets/Datasheets/AP2112.pdf
- MCP23017 DS20001952: 400 kHz and 1.7 MHz I²C, 1.8–5.5 V, 25 mA per pin, 8 per bus. https://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf
- ST7796S: RGB565 and RGB666 over SPI; 66 ns write cycle. https://dl.espressif.com/dl/schematics/ST7796S_SPEC_V1.0.pdf (ILI9488 is 18-bit on SPI: partial evidence only)
- TSOP17xx (Vishay, Rev. 10, 2001): VS 4.5–5.5 V; newer revisions not checked.

## 4. Still unverified or open

- Datasheets not read: TPS61088, TLV62568, BQ24070, MAX17048, PCA9535.
- RDM6300 TX voltage and frame format; Waveshare backlight current and usable SPI clock; SX1308 specs; ILI9488 datasheet text; BIS status of the LiPo cells; India WPC/ETA status of the ESP32-S3 module.
- Sellers not searched: see the list at the top.
- Evelta stock for BQ24075, BQ27441, MAX17048G, MCP23017-E/SO: email to confirm.
- Per-port load switch, buck-boost, bare TPS61023, bare BQ24074/MCP73871/BQ25895: no Indian-stocked part found, so not yet import-only.
