# Indian availability of Nucleo-144 test boards (checked 2026-11-02)

Purpose: find Indian sellers for the boards needed by the hardware checks in `firmware/zephyr/derisk/RESULTS.md` (NUCLEO-F429ZI and NUCLEO-H743ZI). Pages were opened by me (WebFetch) unless marked snippet. Rule R17: DigiKey India, Mouser India, element14, Tanotis (import duties included) and overseas sellers are imports. Evelta shows contradictory stock labels; Robu (403), Robocraze (429), Thingbits, Probots, Sunrom, Quartz Components were not readable or not searched. Prices are snapshots.

## NUCLEO-F429ZI (STM32F429ZIT6)
| Seller | Price | Stock evidence | Verdict |
|---|---|---|---|
| Hubtronics https://hubtronics.in/microcontroller-development-boards/nucleo-f429zi | ₹4,012 incl. GST (₹3,400 + 18 %) | "Stock: 0 in Stock", "Notify when available" | out of stock |
| Evelta https://evelta.com/nucleo-f429zi-nucleo-dev-board-arduino-compatible/ | ₹2,645 ex GST, ₹3,121.10 incl. | page text shows both "in stock" and "Sold Out"; structured data says OutOfStock; "Usually Delivered in 2-5 Days"; ship-from not stated | ambiguous, ask Evelta |
| Tanotis | ₹2,989.65 "includes GST and import duties" | page blocked (429) this time | import, excluded |
| Amazon.in (ROBOTICSSIGN listing) | n/a | "currently unavailable" (search snippet) | unavailable |
| DNA Tech India, ElectronicsComp | not listed (DNA Tech search; ElectronicsComp search pages 1–3) | | not stocked |
| Lion Circuits, Tenet Tech | product URLs returned 404 | | not found |

## NUCLEO-H743ZI (STM32H743ZIT6) and relatives
| Seller | Board | Price | Stock evidence |
|---|---|---|---|
| Hubtronics https://hubtronics.in/stmh743zi-development-board | NUCLEO-H743ZI | ₹3,122.28 incl. GST (₹2,646 + 18 %) | "Stock: 0 in Stock", "Notify when available" |
| Hubtronics category page https://hubtronics.in/st?page=4 | NUCLEO-H743ZI2 ₹3,410.20; H753ZI ₹5,225; H723ZG ₹3,540; H745ZI-Q ₹3,775; H755ZI-Q ₹3,424; H563ZI ₹4,078; H7A3ZI-Q ₹4,956 | | all "Notify when available" |
| IndiaMART (Hubtronics, Pune) | NUCLEO-H743ZI | ₹2,900 ex taxes | "In Stock" — **contradicts Hubtronics' own site (0 in stock); treat as stale** |
| Lion Circuits https://www.lioncircuits.com/parts/NUCLEO-H753ZI | NUCLEO-H753ZI | ₹5,084.63 (GST not stated) | "In Stock", "Ships in 7-10 days", ship-from not stated; looks distributor-fed, so **not counted as Indian stock** until Lion Circuits confirms in writing |
| Evelta | NUCLEO-H743ZI2 page exists (SKU 033-NUCLEO-H743ZI2), price and stock not captured; H743ZI and H753ZI not found | | |
| DNA Tech India, ElectronicsComp | no H743ZI, H743ZI2 or H753ZI found | | |
| DigiKey India, element14 India | NUCLEO-H743ZI2 listed obsolete/no longer manufactured; H753ZI recommended as substitute | | imports, excluded |

Notes: the NUCLEO-H753ZI is ST's recommended substitute for the discontinued H743ZI2 (same 144-pin STM32H7 Nucleo, STM32H753 = H743 plus crypto) and Zephyr 4.5.0 has a `nucleo_h753zi` board. ElectronicsComp lists a "NUCLEO-H7A3ZI-Q" at ₹3,203 with "STM32H743ZI MCU" in the title; the H7A3ZI-Q is a different MCU, so do not order it as an H743 board.

## NUCLEO-H723ZG (a nearby H7 board that is in Indian stock)
- DNA Tech India https://www.dnatechindia.com/st-nucleo-h723zg-nucleo-144-development-board?search=NUCLEO-H723ZG : ₹4,707.22 incl. GST (₹3,989.17 + GST), **"Stock: 3"**, GST invoices; origin not stated.
- Evelta: ₹4,895 ex GST / ₹5,776.10 incl.; stock labels contradictory (in stock / Sold Out / schema OutOfStock).
- Relevance: different MCU from the H743 (STM32H723, 550 MHz, different RAM map), but it already has the `usbotg_hs` node in Zephyr's dtsi that our H743 node was modelled on, and Zephyr has `nucleo_h723zg`. It could run the dual-USB, SPI and display checks on an H7-family part, but it cannot confirm H743 silicon behaviour.

## Reading
- No confirmed in-stock listing of either exact board from an Indian seller. Hubtronics lists both and about twenty other Nucleo-144 boards as "Notify when available", so they can probably order them; Evelta's F429ZI is the closest to available but ambiguous.
- Under R17, nothing here shows the boards are import-only.
- Actions: ask Hubtronics for lead time on F429ZI and H743ZI (and H753ZI); ask Evelta to confirm F429ZI stock and ship-from; ask Lion Circuits for ship-from and an invoice for the H753ZI; check Robu, Robocraze, Probots, Thingbits, Sunrom and Quartz Components by hand.
