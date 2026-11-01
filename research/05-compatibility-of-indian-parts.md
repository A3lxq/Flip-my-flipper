# Datasheet compatibility of parts found in India

Condensed from a research-agent report. PDFs downloaded and text-extracted: ESP32-S3-WROOM-1 v1.8, CC1101 SWRS061I, MCP23017 DS20001952, MT3608 (Aerosemi), Vishay TSOP17 Rev. 10, EM4095, ST7796S V1.0, and the Indian G.S.R. 853(E) Gazette text. Items marked "no" were not verified from a primary source.

## ESP32-S3-WROOM-1 — compatible with caveats
Datasheet https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf (v1.8). VDD33 3.0–3.6 V (abs max 3.6 V); external supply ≥ 0.5 A; Wi-Fi TX peaks 355 mA (11b), 297 mA (11g), 285 mA (11n MCS7); BLE TX 344 mA at +20 dBm; not 5 V tolerant (max VDD+0.3). Strapping pins GPIO0 (weak pull-up), GPIO3 (floating), GPIO45 (weak pull-down), GPIO46 (weak pull-down); GPIO0+GPIO46 select boot mode, GPIO45 the VDD_SPI voltage, GPIO3 the JTAG source. Serial download: GPIO0 = 0 and GPIO46 = 0 at reset release; the exact STM32 sequencing is the agent's inference. Default console UART0 TXD0 = GPIO43, RXD0 = GPIO44. R8 modules lose IO35–37 and are limited to 65 °C. EN must not float. Antenna: PCB on WROOM-1, connector on -1U. Espressif certificate list shows FCC, CE, SRRC, MIC, IC, KCC, NCC, ANATEL, Vietnam MIC, Wi-Fi Alliance; **no India WPC/ETA for ESP32-S3-WROOM-1** (it hosts ETAs for other modules). Whether a module ETA covers an end product: unresolved.
Advice: dedicated 3.3 V rail ≥ 500 mA with bulk capacitance; keep strapping pins off the link or at default levels at reset; EN and GPIO0 from STM32 GPIOs for flashing.

## CC1101 — compatible with caveats
Datasheet https://www.ti.com/lit/ds/symlink/cc1101.pdf. VDD 1.8–3.6 V (abs max 3.9 V); digital pins −0.3 to VDD+0.3 V, not 5 V tolerant. SPI 10 MHz with 100 ns inter-byte delay; without the delay 9 MHz (single access) / 6.5 MHz (burst). GDO0 (pin 6) and GDO2 (pin 3) are digital outputs; GDO0 is also the async serial TX input; outputs rated about 4 mA. Bands 300–348, 387–464, 779–928 MHz. Max output programmable to about +12 dBm; reference-design settings +10 dBm at 315/433 MHz, +12 dBm at 868 MHz, +11 dBm at 915 MHz. Matching networks are band-specific (multilayer inductors at 315/433, wire-wound at 868/915). Indian module pinouts differ (8- and 10-pin boards put GDO0/GDO2 on different pins; check the silkscreen). A 433-tuned module at 865–867 MHz would be mismatched (inference).
India: G.S.R. 853(E), 10 Dec 2021, 865–868 MHz short-range devices (non-specific 25 mW e.r.p., tracking/tracing 500 mW with duty-cycle limits, wideband 25 mW, RFID 2 W on four channels), type approval required; the agent noted the default top CC1101 setting exceeds 25 mW e.r.p. if antenna gain adds. No legal conclusion drawn.

## RDM6300 (125 kHz EM4100) — compatible with caveats (EM4100 only)
No manufacturer datasheet found. Vendor pages: 5 V supply (some say 3.3–5 V), UART 9600 baud, read-only EM4100-compatible. **TX voltage level not verified**: measure; level-shift. EM4095 is an analog front end (VDD 4.1–5.5 V, PLL, demodulated data on DEMOD_OUT; firmware decodes) and allows read/write of other 125 kHz tags but needs coil design.

## TSOP1738 — compatible with caveats
Vishay TSOP17xx Rev. 10 (2001): **VS 4.5–5.5 V** (abs max 6.0 V), 0.4–1.5 mA, active-low output, bursts ≥ 10 cycles with ≥ 14 cycle gap, series 100 Ω + 4.7 µF recommended on the supply. 3.3 V operation is not specified in that revision (newer revisions not checked). IR LED drive: a transistor switch driven by timer PWM at 38 kHz is general practice (not from a cited source).

## 3.5" ST7796S SPI display (Waveshare) — compatible
Pages https://www.waveshare.com/wiki/3.5inch_Capacitive_Touch_LCD and https://www.waveshare.com/3.5inch-capacitive-touch-lcd.htm ; ST7796S spec https://dl.espressif.com/dl/schematics/ST7796S_SPEC_V1.0.pdf. ST7796S + FT6336U touch, 320×480; on-board voltage translator, 3.3 V / 5 V; ST7796S write cycle ≥ 66 ns (about 15 MHz), read ≥ 150 ns; RGB565 and RGB666 over SPI. Waveshare gives no SPI clock or backlight current; about 63 mA at 3.3 V quoted once (unclear if backlight included). ILI9488 runs 18-bit on SPI (partial evidence). Pinout: VCC, GND, MISO, MOSI, SCLK, LCD_CS, LCD_DC, LCD_RST, LCD_BL, TP_SDA, TP_SCL, TP_INT, TP_RST.

## MT3608 boost — marginal / not for a switched rail
Input 2–24 V, UVLO 1.98 V, 4 A switch limit, module rated 2 A output, "up to 97 %" efficiency headline; boost topology with external diode, so input stays connected to output in shutdown (no load disconnect). 5 V at 1 A from 3.0 V needs about 2 A from the cell. SX1308 specs not checked.

## 3.7 V 3000–3500 mAh cells (India)
Probots KP-355085 (3000 mAh, about 85×50×3.5 mm, JST-PH 2 mm, protection described without numbers, ₹529, out of stock) and KP-045090 (about 60×50×4 mm); DNA Tech 3000 mAh (62×71×4.75 mm, 120 g, no protection/connector/polarity info). No BIS number, discharge limit or polarity on the pages. ThinkRobotics page hit HTTP 429.

## MCP23017 — compatible
Datasheet https://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf. 100 kHz / 400 kHz / 1.7 MHz I²C, 1.8–5.5 V, 25 mA per pin (VOH only VDD−0.7 V at −3 mA), INTA/INTB with mirror bit, up to 8 per bus, packages SOIC, SPDIP, SSOP, QFN.

## Design risks noted
Strapping pins; brown-out on Wi-Fi TX; 5 V vs 3.3 V logic (RDM6300 TX, TSOP1738, display translator); no load disconnect on MT3608; CC1101 SPI speed limit; cell protection ratings unpublished. Unverified: SX1308, ThinkRobotics BIS cells, RDM6300 TX level and frame format, ILI9488 datasheet text, Waveshare backlight current, ESP32-S3 WPC/ETA status.
