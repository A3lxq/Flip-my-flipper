# Indian sourcing check, remaining parts (2026-11-01)

Rule R17: only Indian sellers with Indian stock. DigiKey India, Mouser India, Tanotis (its page says "includes import duties") and Farnell/element14 ship from overseas, so they count as **imports** here.
Method: web search plus opening some seller pages. "Page checked" means I opened the listing; "snippet" means only search-result text, so stock is unverified. All prices are snapshots; check before buying. Nothing has been ordered or confirmed with a seller.

## Result by part

| Part | Indian listing found | Evidence | Verdict |
|---|---|---|---|
| ESP32-S3 module (Wi-Fi/BLE coprocessor) | [DNA Tech ESP32-S3-WROOM-1-N8](https://www.dnatechindia.com/esp-32-s3-wroom-1-n8-module-buy-in-india.html): ₹379.96 incl. GST, "Stock: 30", importer ElectroSource, origin China. Also Lion Circuits (N8 ₹341, N16R2 ₹654), Techiesms N16R8 ₹430, Tenet Tech N4R8 ₹421 | DNA Tech page checked; others snippet | **Available in India** |
| CC1101 (Sub-GHz) | [Robu 868 MHz](https://st.robu.in/product/cc1101-868mhz-wireless-transceiver-module) ₹267 incl. GST "in stock"; FlyRobo SMA-antenna module; [Electropi 868](https://www.electropi.in/cc1101-868mhz-wireless-transceiver-module) ₹260 + GST but **out of stock** and the page contradicts itself (868 vs 433 MHz) | Electropi page checked; Robu snippet | **Available (868/433 MHz variants)**; a 915 MHz one only appeared as an import. Confirm band with the seller |
| NFC frontend ST25R3916 | Only [DigiKey India](https://www.digikey.in/en/products/detail/stmicroelectronics/ST25R3916B-BWLT/18085803) (chip, ₹455 to ₹525) and [Tanotis](https://www.tanotis.com/products/stmicroelectronics-st25r3916b-aqet-rfid-read-write-13-56-mhz-2-4-v-to-5-5-v-40-to-125-deg-c-ufqfpn-32) (import duties included) | Snippet | **Import only so far** (one search round; not proof). PN532 modules are in Indian stock (about ₹344) but are not an equivalent (brief §5.2) |
| LF RFID | RDM6300 module at Hubtronics, Robodo, FlyRobo, Engineer Store and others at about ₹210 to ₹265. No Indian EM4095 | Snippet | RDM6300 available; EM4095 frontend not found. RDM6300 is not a full frontend (brief §5.3) |
| IR receiver TSOP1738 | Probots, Zbotic, Shokitech, DNA Tech about ₹24 to ₹35 | Snippet | **Available** |
| 3.5" ST7796 display | Waveshare 3.5" IPS ST7796S + touch ([Zbotic](https://zbotic.in/product/waveshare-3-5inch-capacitive-touch-display-module/) ₹1,954, Evelta ₹1,994, Hubtronics). Robocraze SmartElex 3.5" ₹1,239 (driver not confirmed). Some cheap 3.5" modules use ILI9488, not ST7796 | Snippet; Zbotic page blocked (403) | **Available with touch layer** (unused, costs extra). Non-touch ST7796 not confirmed |
| Li-ion/LiPo 3000 to 3500 mAh | DNA Tech lists 3.7 V 3000 mAh (62×71×4.75 mm) and 3500 mAh (3500 mAh out of stock); price for the 3000 mAh page unclear | Snippet | Probably available; verify price and stock |
| Boost converter | [Evelta TPS61023DRLR](https://evelta.com/tps61023drlr-boost-switching-regulator-ic-3a-sot-563-6) ₹35.43 ex-GST, **sold out** (page checked); MT3608 and SX1308 ICs at Techtonions, Sunrom, DNA Tech about ₹7 to ₹28 | Evelta page checked | Cheap boost ICs available; TPS61023 out of stock |
| LiPo charger / power-path IC | BQ24074 and BQ24072 only at DigiKey India; MCP73871 not found in India | Snippet | **Import only so far.** TP4056 boards are common in India but are not a power-path solution (brief §12) |
| Fuel gauge MAX17048 | [Evelta](https://evelta.com/max17048g-t10-battery-management-3a-1-cell-2-cell-fuel-gauge-ic-tdfn-8) ₹598.79 incl. GST (stock not seen); also DigiKey India | Snippet | Possibly available; confirm stock |
| I²C expander (PCA9555/TCA9535/MCP23017) | MCP23017-E/SP (DIP-28) at DNA Tech; PCA9555 and TCA9535 only at Mouser India | Snippet | SMD expander **import only so far**; DIP part too big for the board |
| Load switch (TPS22918 etc.) | None found | Snippet | **Not found in India** |
| USB-C 16-pin receptacle | Evelta ₹7.75, Hubtronics ₹8, Probots ₹39 | Snippet | **Available** |
| microSD socket (SMD) | One doubtful listing (iFuturetech, price unclear); the rest were overseas | Snippet | **Not confirmed** |
| JST SH 1.0 mm connectors | No Indian listing for 1.0 mm SMD (only a 1.15 mm wire-leaded kit at The Engineer Store) | Snippet | **Import only so far** |

## Not yet searched
Board-to-board connectors for the core module, 1-Wire ID chips (DS2431-class), ESD protection diodes, crystals, inductors, buck/LDO regulators (AP2112K not found), tact switches/d-pad, buzzer, vibration motor, SD cards, USB-C CC/PD controller.

## What this means (PROPOSED, nothing changed)
Per R17 no part is replaced yet. The parts where I found **no Indian source** at all, and so need a firmer import-only check before any substitution, are:
1. **ST25R3916** (NFC): ask Indian distributors for a quote first. Fallback candidates (not equivalent): PN532, RC522.
2. **BQ24074/BQ24072** charger: check Indian stores for other power-path chargers before substituting.
3. **JST SH 1.0 mm**: possibly switch the connector family to something Indian stores stock (my suggestion: look at 1.25 mm or 2.0 mm families, or 2.54 mm with keyed housings), since pitch affects board space.
4. **Load switches, SMD I/O expanders, SMD microSD socket.**

The regulatory question matters for CC1101 too: the 868 MHz and 433 MHz variants sold here may not match the licence-free bands in India. I have not researched this and make no claim; it stays on the regulatory research list.
