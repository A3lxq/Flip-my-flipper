# KiCad skeletons for the two NFC modules

Status: **skeleton v0.1 (2026-11-02)**. Not fabricable. Nothing has been routed, ordered or built.

| Project | What it is | State |
|---|---|---|
| `pn532-adapter/` | SM-S adapter carrying the PN532 V3 breakout (Variant A, `06-nfc-modules.md` §3) | schematic + placement-only PCB (unrouted) |
| `st25r3916-module/` | ST25R3916 module (Variant B, `06-nfc-modules.md` §5) | **block-level schematic only** (blocked on ST documents and chip sourcing); no PCB |
| `lib/` | shared symbols (`synnefo.kicad_sym`) and footprints (`synnefo.pretty/`) | generic geometry, to check per chosen part |
| `tools/gen_kicad.py` | generator for all of the above (Python standard library) | reproducible: `python3 tools/gen_kicad.py hardware/kicad` |
| `checks/` | KiCad ERC, DRC and netlist outputs from this run | see below |

Open the `.kicad_pro` files with KiCad 8 or newer. The files were generated in the KiCad 8 file format and checked with `kicad-cli` 10.0.8 (official `kicad/kicad:10.0` container). Edit the generator (not the generated files) if you want the changes to survive a regeneration.

## What was checked

- **PN532 adapter schematic:** KiCad ERC reports 0 violations. The exported netlist has exactly the intended connections (`checks/pn532-adapter.nets.txt`): the SMIS SM-S port pins go to SCK, MOSI, MISO, CS (= the breakout's SSEL), IRQ; IDC and IDD go to the ID EEPROM; 3V3_P feeds the EEPROM and, through jumper JP1, the breakout; RSTPDN is pulled up.
- **PN532 adapter PCB:** KiCad DRC reports **no clearance, courtyard or board-edge violations**; the 23 "unconnected items" are the unrouted nets (expected for a placement-only board). Rendered and inspected visually.
- **ST25R3916 schematic:** KiCad ERC reports 4 errors, all intentional open items on the placeholder block: the crystal pins `XTI`, `XTO` and the antenna pin are unconnected (`checks/st25r3916-module.erc.rpt`).
- **Not checked:** electrical correctness of any value against datasheets, footprint geometry against real parts, signal integrity, EMC, or anything on the real breakout board.

## Unverified items (must be resolved before fabrication)

PN532 adapter:
1. **PN532 V3 breakout header pin order and position.** Signal names come from the Elechouse guide; the physical order, pitch and which of the board's two headers (J1 10-pin, J2 8-pin in the vendor schematic) carry which signal were not verified. Buy the board, measure it, and fix symbol `PN532_V3_Header_UNVERIFIED_ORDER`, the footprint and the placement.
2. **Breakout supply and I/O levels.** The board's regulator and the PVDD source were not found; the adapter powers it from 3V3_P through JP1 (default 1-2). Do not use 5V_P until measured (`06-nfc-modules.md` §4.2). DIP switch settings (SPI) are on the breakout, not the adapter; verify with a meter.
3. **ID EEPROM.** 24C02-class SOIC-8, address 0x50. ElectronicsComp stocks the M24C04-WMN6P (SOIC-8) and a DIP-8 24C02; the M24C04's pin 1 is not a plain A0, so check its datasheet before freezing. WP is grounded (programmable); decide the production setting.
4. **Connector.** The footprint is a generic 2x05 2.54 mm vertical header with IDC pin numbering; the real part (Probots 10-pin right-angle shrouded box header was found in stock), its orientation, outline and mating cable are not chosen.
5. **Passives.** 0603 pad geometry is approximate; the 10 uF value and voltage rating are not selected; IRQ pull-up, if any, belongs on the carrier (SMIS) and is not on the adapter.
6. **Routing, mounting holes, board shape, silkscreen.** Not done.

ST25R3916 module:
1. Pin numbers marked `TBD-n` are unknown; only pins 1, 3, 7, 8, 9, 10, 11, 14 and 33 come from DS12484 Rev 3 text (an old revision).
2. The decoupling capacitor net assignments, the VDD_RF/VDD_DR tie and the supply plan are placeholders to confirm against DS12484/DS13541 Figure 1 and §4.2.11.
3. Absent on purpose: antenna coil, EMC filter, matching network, 27.12 MHz crystal and load capacitors, exposed-pad thermal vias, layout. They need AN5276, AN5240, AN5322, AN5592 and the NFC08A1 design files (`06-nfc-modules.md` §9).
4. No Indian source for the chip was found (`04-` to `06-`).

## Parts list (draft, nothing ordered; Indian-stock status from `04-`, `05-`, `06-`)

PN532 adapter:

| Ref | Part | Source and status |
|---|---|---|
| (module) | PN532 V3 breakout | DNA Tech India, ₹317.43 incl. GST, stock 50 (page opened 2026-11-01) |
| J1 | 2x05 2.54 mm shrouded box header | Probots, ₹17 incl. GST, in stock (right-angle); orientation/footprint to confirm |
| JP1, J2 | 1x03 and 1x08 2.54 mm pin headers, shunt | generic; not yet searched |
| U1 | 24C02-class EEPROM, SOIC-8 | ElectronicsComp M24C04-WMN6P ₹17 ex GST (154 in stock); check pin-1 difference |
| C1 | 100 nF 0603 | generic stocked family (Evelta, Probots listings); part not chosen |
| C2 | 10 uF 0603, rating TBD | Probots has a Samsung 22 uF 0805; 0603 10 uF not chosen |
| R1 | 10 kohm 0603 | generic stocked family |

ST25R3916 module: chip, crystal, antenna parts all TBD (see unverified list); ID EEPROM and decoupling as for the adapter.

## Reproduce the checks

```bash
cd hardware/kicad
k() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD:/work" -w /work kicad/kicad:10.0 kicad-cli "$@"; }
k sch erc --severity-all --format report -o /work/checks/pn532-adapter.erc.rpt pn532-adapter/pn532-adapter.kicad_sch
k pcb drc --severity-all --format report -o /work/checks/pn532-adapter.drc.rpt pn532-adapter/pn532-adapter.kicad_pcb
```
