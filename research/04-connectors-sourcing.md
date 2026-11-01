# Connectors in Indian stock

Condensed from a research-agent report. About 20 searches and 25 page opens (Hubtronics, Probots, Evelta, DNA Tech, Lion Circuits, Atomlab, Zbotic). Blocked: robu.in (403), robocraze.com and robodo.in (429), Evelta site search (404), zbotic.in product page (403). Not searched: Thingbits, Sunrom, Silverline, Rhydolabz, The Engineer Store (snippet only), Tanna TechBiz, IndiaMART. "Not found" never means "import-only". Datasheet and mating-cycle figures for JST families are from memory, not from opened datasheets, except the 1 A ratings of SH and GH seen on Probots/Mouser snippet pages.

## Wire-to-board and keyed families
| Family | Seller | Price (INR) | Stock | Opened |
|---|---|---|---|---|
| SH-style 6-pin SMD socket 1.0 mm, generic | Hubtronics | 17.70 incl. GST | 0 | yes |
| SH-style 2/3/4/5/8-pin sockets, 10-pin lot of 5 | Hubtronics | 6.00 to 23.60 | add-to-cart, no counts | list view |
| SH 6-pin lead 15 cm | Hubtronics | 36.00 | 0 | yes |
| SH 4-pin lead 15 cm | Hubtronics | 35.00 | 8 | yes |
| SH 200-pc kit (2–5 pin, crimps, 1 A 50 V) | Probots | 619.00 | in stock | yes |
| JST SM06B-SRSS-TB(LF)(SN) 6-pin SH | Lion Circuits | 124.99 (qty 1) | "In Stock", ships in 7–10 days; ship-from not stated | yes |
| JST GH 6-pin right-angle through-hole header, 1.25 mm, 1 A | Probots | 47.00 | in stock | yes |
| JST GHR-06V-S housing | Lion Circuits | 21.93 | "In Stock", 7–10 days | yes |
| JST XH 6-pin header, 3 A, through-hole | Robomart / DNA Tech | about 37 for 5 | not seen | snippet |
| 10-pin (2×5) shrouded box header, right-angle, keyed, 2.54 mm | Probots | 17.00 | in stock | yes |
| 10-pin RA FRC box header | Hubtronics | 6.00 | 0 | yes |
| Qwiic / STEMMA QT SH 4-pin cables | Atomlab / Electronicscomp | 142–175 | out of stock / unknown | partly |

Not found in Indian stock: JST SH vertical SMD; SH 6-pin female crimp housing sold loose; JST PH SMD header; Molex PicoBlade / Micro-Lock. Excluded as imports: DigiKey India, Mouser India, element14 India, Tanotis.

## Board-to-board, 60+ contacts
- 2×30 2.54 mm female socket, through-hole: Evelta ₹410.64 incl. GST, 22 in stock (machined round pin; its male partner not looked up).
- 2.0 mm, 1.27 mm, 0.8 mm mezzanine at 60+ contacts: nothing from an Indian seller. Hubtronics sells only FPC/FFC adapter boards up to 24 pins. (The later port-protection report found generic Berg-strip 2.0 mm and 1.27 mm 2×40 headers; see `07-`.)

## microSD, tact switches, buzzer, vibration motor
- microSD: DNA Tech TF-07F push-push, 9-pin with card-detect, ₹29.50, 10 in stock (SMD not stated). Others (Robodo, Sharvi, iFutureTech) not opened.
- Tact switch 6×6×5 mm SMD: Hubtronics ₹4.72 incl. GST, 694 in stock (min qty 5).
- Buzzer: Hubtronics piezo 5 V ₹15. Coin vibration motor 10 mm: Probots about ₹58 + GST (snippet).

## Compatibility notes
1 A per contact is ample for 3V3 signals; for 0.5 A on the 5 V pin it is marginal after derating (SH needs AWG 28–32 wire). XH (3 A) or PH (2 A) are safer. SPI at 10–20 MHz over a 1.0/1.25 mm harness: pitch does not limit frequency, wire length and crosstalk do (engineering judgement). A 2×30 2.54 mm board-to-board joint at 20–40 MHz SPI and 25 MHz SDIO is marginal; interleave grounds.

## Verdict
Genuine JST SH from an Indian shelf is not confirmed (generic clones at Hubtronics; the Lion Circuits part looks distributor-fed). Best available domestic alternatives: JST GH 1.25 mm (through-hole verified), JST XH 2.5 mm, and the 2.54 mm 2×5 box header (verified).
