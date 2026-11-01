# NFC frontend sourcing and compatibility (India)

Condensed from a research-agent report. See `research/README.md` for limits.

**Verdict.** No Indian seller with stock of the ST25R3916/B chip or a module was found. It appears only on import routes. This is a fair summary but the search was limited (see "How hard it looked").

## How hard it looked
Two or three web searches per part. Pages opened: DigiKey India, Probots, PoshAce search, DNA Tech India (PN532, PN5180, ST25R searches). Failed: robu.in (403), Robocraze (429, twice), Evelta search (404), Thingbits (generic results). Not opened: Hubtronics, Sunrom, Silverline, Rhydolabz, Tanna TechBiz, Amazon.in, IndiaMART.

## ST25R3916 / 3916B
| Seller | Price | Stock | Origin | Opened |
|---|---|---|---|---|
| DigiKey India (import) | ₹596.34 for 1, ₹396 at 1000+ | 3,754 | Shipped CPT, duty due on delivery; free over ₹7,000, else ₹1,200 | yes |
| Mouser India (import) | ST25R3916-AQET about ₹528; STEVAL-25R3916B kit ₹9,607 | 110 (kit) | import | snippet |
| Tanotis (import) | ST25R3916B-AQET about ₹761 for 2 | n/a | import ("includes GST and import duties") | snippet |
| Elechouse module | $10.90 | not stated | China; India shipping unconfirmed | yes |
| DNA Tech India | none ("no match") | | | yes |

The WLCSP (BWLT) package is hard to hand-assemble; the QFN (AQET/AQWT) parts are the practical packages.

## Alternatives
- **PN5180:** only PoshAce, ₹2,699, "imported to order, 12-21 days" (counts as an import); DigiKey India OM25180FDKM ₹25,198, 16-week lead time. No Indian-stocked PN5180 found.
- **PN532 V3 module:** DNA Tech India ₹317.43 incl. GST, stock 50 (page opened). Robu ₹369 and Robocraze ₹254 are snippets only (pages blocked).
- **RC522:** Probots ₹139 incl. GST (in stock; 3.3 V only, SPI, ISO14443A/MIFARE). Zbotic about ₹59 + GST (unverified).

## Compatibility
| | ST25R3916/B | PN5180 | PN532 | MFRC522 |
|---|---|---|---|---|
| Protocols | 14443A/B, ISO15693, FeliCa, NFC Forum T1-T5, reader, NFC-A/F card emulation, P2P, EMVCo | 14443A/B, ISO15693, ICODE, FeliCa, MIFARE, 18092 (card emulation limited) | 14443A/B, FeliCa, MIFARE, P2P, card emulation; **no ISO15693** | 14443A/MIFARE only |
| Interface | SPI, I2C | SPI | I2C, SPI, HSU | SPI (Probots board SPI only) |
| Supply | 2.4–5.5 V | 2.7–5.5 V | 2.7–5.5 V | 2.5–3.3 V |

Licences of the host libraries were unverified in this report (checked later; see `02-` and `03-`).

## What PN532 and RC522 cannot do versus ST25R3916
- RC522: no ISO14443B, no ISO15693, no FeliCa, no card emulation, no P2P, no NFC-V.
- PN532: no ISO15693; FeliCa limited; lower RF output power and shorter range; no EMVCo-grade analog control (from the agent's knowledge, not re-fetched).
