#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate the KiCad skeleton for the two NFC modules (stdlib only, KiCad 8 file format).

  hardware/kicad/lib/synnefo.kicad_sym         custom symbols
  hardware/kicad/lib/synnefo.pretty/*.kicad_mod custom footprints
  hardware/kicad/pn532-adapter/                schematic + PCB (placement only, unrouted)
  hardware/kicad/st25r3916-module/             block-level schematic only (blocked on ST documents)

usage: gen_kicad.py <hardware/kicad directory>
Connectivity is expressed with net labels placed exactly on pin end points.
Nothing here replaces ERC/DRC review in KiCad.
"""
import json
import os
import sys
import uuid

OUT = sys.argv[1]
NS = uuid.UUID("6f1d7a3e-5c0d-4e57-8a11-5ec0de5f1195")
DATE = "2026-11-02"
FONT = "(effects (font (size 1.27 1.27)))"
FONT_HIDE = "(effects (font (size 1.27 1.27)) hide)"


def U(name):
    return str(uuid.uuid5(NS, name))


def esc(s):
    return s.replace('"', "'")


# ---------------------------------------------------------------- symbols
class Pin:
    def __init__(self, name, number, etype="passive", side="L", y=0.0, hidden=False):
        self.name, self.number, self.etype, self.side, self.y, self.hidden = name, number, etype, side, y, hidden


class Sym:
    """A symbol: rectangle body plus pins on the left (x=-hw-2.54) and/or right (x=+hw+2.54)."""

    def __init__(self, name, ref, value, footprint, desc, hw, hh, pins, custom_body=None, power=False):
        self.name, self.ref, self.value, self.footprint, self.desc = name, ref, value, footprint, desc
        self.hw, self.hh, self.pins, self.custom_body, self.power = hw, hh, pins, custom_body, power

    def pin_end(self, pin):
        """Library-coordinates of the pin's connection point."""
        if pin.side == "L":
            return (-self.hw - 2.54, pin.y)
        if pin.side == "R":
            return (self.hw + 2.54, pin.y)
        return (0.0, 0.0)

    def sexp(self, prefix=""):
        n = f'"{prefix}{self.name}"'
        o = [f"(symbol {n}"]
        if self.power:
            o.append("  (power)")
            o.append("  (pin_numbers hide)")
            o.append("  (pin_names (offset 0) hide)")
        o.append("  (exclude_from_sim no) (in_bom %s) (on_board %s)" % (("no", "no") if self.power else ("yes", "yes")))
        o.append(f'  (property "Reference" "{self.ref}" (at 0 {self.hh + 2.54:.2f} 0) {FONT})')
        o.append(f'  (property "Value" "{esc(self.value)}" (at 0 {-self.hh - 2.54:.2f} 0) {FONT})')
        o.append(f'  (property "Footprint" "{self.footprint}" (at 0 0 0) {FONT_HIDE})')
        o.append(f'  (property "Datasheet" "~" (at 0 0 0) {FONT_HIDE})')
        o.append(f'  (property "Description" "{esc(self.desc)}" (at 0 0 0) {FONT_HIDE})')
        o.append(f'  (symbol "{self.name}_1_1"')
        if self.custom_body:
            o.append(self.custom_body)
        else:
            o.append(f"    (rectangle (start {-self.hw} {self.hh}) (end {self.hw} {-self.hh}) "
                     f"(stroke (width 0.254) (type default)) (fill (type background)))")
        for p in self.pins:
            x, y = self.pin_end(p)
            ang = {"L": 0, "R": 180, "T": 270, "B": 90, "N": 90}[p.side]
            length = 0 if self.power else 2.54
            nm = FONT_HIDE if p.hidden else FONT
            o.append(f'    (pin {p.etype} line (at {x:.2f} {y:.2f} {ang}) (length {length}) '
                     f'(name "{p.name}" {nm}) (number "{p.number}" {nm}))')
        o.append("  )")
        o.append(")")
        return "\n".join(o)


def stack(names, side, start_y, step=2.54):
    return [(n, side, start_y - i * step) for i, n in enumerate(names)]


# SMIS port connector, SM-S class (08-smis-v0.2.md section 2); numbers follow IDC odd/even footprint pads
SMS_NAMES = ["GND", "3V3_P", "5V_P", "SCK", "MOSI", "MISO", "CS", "IRQ", "IDC", "IDD"]
SYM_SMS = Sym("SMIS_SM-S_10", "J", "SMIS_SM-S_10", "synnefo:IDC_Header_2x05_P2.54mm_Vertical",
              "SMIS v0.2 SM-S port, 10 contacts: 1 GND 2 3V3_P 3 5V_P 4 SCK 5 MOSI 6 MISO 7 CS 8 IRQ 9 IDC 10 IDD",
              7.62, 13.97,
              [Pin(n, str(i + 1), "passive", "L", 11.43 - i * 2.54) for i, n in enumerate(SMS_NAMES)])

# PN532 V3 breakout signal header. ORDER IS UNVERIFIED: names come from the Elechouse guide; physical order must be measured.
PN_NAMES = ["VCC", "GND", "SCK", "MISO", "MOSI", "SSEL", "IRQ", "RSTPDN"]
SYM_PN = Sym("PN532_V3_Header_UNVERIFIED_ORDER", "J", "PN532_V3_8pin", "synnefo:PinHeader_1x08_P2.54mm_Vertical",
             "PN532 V3 breakout signal header. Pin ORDER and POSITION UNVERIFIED: measure the real board before layout.",
             7.62, 11.43,
             [Pin(n, str(i + 1), "passive", "L", 8.89 - i * 2.54) for i, n in enumerate(PN_NAMES)])

SYM_EEP = Sym("EEPROM_24C02_SOIC8", "U", "24C02", "synnefo:SOIC-8_3.9x4.9mm_P1.27mm",
              "I2C ID EEPROM, standard 24Cxx SOIC-8 pinout (A0 A1 A2 GND SDA SCL WP VCC), address 0x50",
              5.08, 6.35,
              [Pin("A0", "1", "input", "L", 3.81), Pin("A1", "2", "input", "L", 1.27),
               Pin("A2", "3", "input", "L", -1.27), Pin("GND", "4", "power_in", "L", -3.81),
               Pin("VCC", "8", "power_in", "R", 3.81), Pin("WP", "7", "input", "R", 1.27),
               Pin("SCL", "6", "input", "R", -1.27), Pin("SDA", "5", "bidirectional", "R", -3.81)])

CAP_BODY = ("    (polyline (pts (xy -1.27 0.508) (xy 1.27 0.508)) (stroke (width 0.254) (type default)) (fill (type none)))\n"
            "    (polyline (pts (xy -1.27 -0.508) (xy 1.27 -0.508)) (stroke (width 0.254) (type default)) (fill (type none)))")
# vertical two-pin parts: pins at (0, +3.81) and (0, -3.81); built by hand because Sym places pins left/right
class VSym(Sym):
    def pin_end(self, pin):
        return (0.0, 3.81 if pin.side == "T" else -3.81)


SYM_C = VSym("C_generic", "C", "C", "synnefo:C_0603_1608Metric", "Capacitor", 1.27, 1.27,
             [Pin("1", "1", "passive", "T"), Pin("2", "2", "passive", "B")], custom_body=CAP_BODY)
RES_BODY = "    (rectangle (start -1.016 2.54) (end 1.016 -2.54) (stroke (width 0.254) (type default)) (fill (type none)))"
SYM_R = VSym("R_generic", "R", "R", "synnefo:R_0603_1608Metric", "Resistor", 1.27, 2.54,
             [Pin("1", "1", "passive", "T"), Pin("2", "2", "passive", "B")], custom_body=RES_BODY)

SYM_JP = Sym("Conn_01x03_SupplySelect", "JP", "SupplySelect", "synnefo:PinHeader_1x03_P2.54mm_Vertical",
             "Supply select: pin 1 3V3_P, pin 2 to the module, pin 3 5V_P. Shunt on 1-2 by default.",
             5.08, 5.08,
             [Pin("3V3_P", "1", "passive", "L", 2.54), Pin("COMMON", "2", "passive", "L", 0.0),
              Pin("5V_P", "3", "passive", "L", -2.54)])

FLAG_BODY = ("    (polyline (pts (xy 0 0) (xy 0 1.27) (xy 1.27 1.905) (xy 0 2.54) (xy -1.27 1.905) (xy 0 1.27)) "
             "(stroke (width 0) (type default)) (fill (type none)))")
SYM_FLAG = Sym("PWR_FLAG", "#FLG", "PWR_FLAG", "", "Marks a net as driven (for ERC)", 0, 1.27,
               [Pin("pwr", "1", "power_out", "N", 0.0)], custom_body=FLAG_BODY, power=True)

# ST25R3916 block symbol. Pin numbers known from DS12484 Rev 3 text: 1 VDD_IO, 3 VDD_D, 7 VDD_A, 8 VDD, 9 VDD_RF,
# 10 VDD_TX, 11 VDD_AM, 14 VDD_DR, 33 exposed pad. All other numbers are TBD until the pin table is read.
ST_LEFT = [("VDD_IO", "1", "power_in"), ("VDD", "8", "power_in"), ("VDD_TX", "10", "power_in"),
           ("VDD_DR", "14", "power_in"), ("SCLK", "TBD-1", "input"), ("MOSI", "TBD-2", "input"),
           ("MISO", "TBD-3", "output"), ("BSS", "TBD-4", "input"), ("IRQ", "TBD-5", "output"),
           ("I2C_EN", "TBD-6", "input")]
ST_RIGHT = [("VDD_A", "7", "power_out"), ("VDD_D", "3", "power_out"), ("VDD_RF", "9", "power_out"),
            ("VDD_AM", "11", "power_out"), ("XTI", "TBD-7", "input"), ("XTO", "TBD-8", "output"),
            ("ANT (TBD)", "TBD-9", "passive"), ("GND / EP", "33", "power_in")]
SYM_ST = Sym("ST25R3916_BLOCK", "U", "ST25R3916 (QFN32) BLOCK", "",
             "Block-level placeholder for the ST25R3916. Pin numbers TBD-n are unknown until DS12484 Table 2 is read.",
             20.32, 15.24,
             [Pin(n, num, t, "L", 12.7 - i * 2.54) for i, (n, num, t) in enumerate(ST_LEFT)] +
             [Pin(n, num, t, "R", 12.7 - i * 2.54) for i, (n, num, t) in enumerate(ST_RIGHT)])

ALL_SYMS = [SYM_SMS, SYM_PN, SYM_EEP, SYM_C, SYM_R, SYM_JP, SYM_FLAG, SYM_ST]
BY_NAME = {s.name: s for s in ALL_SYMS}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def sym_lib():
    body = "\n".join(s.sexp() for s in ALL_SYMS)
    return (f'(kicad_symbol_lib (version 20231120) (generator "synnefo_gen") (generator_version "1.0")\n{body}\n)\n')


# --------------------------------------------------------------- schematic
class Sch:
    def __init__(self, project, title, comments):
        self.project, self.title, self.comments = project, title, comments
        self.root = U(project + "/root")
        self.items = []
        self.used = set()
        self.counter = 0

    def place(self, sym, ref, value, x, y, nets, footprint=None, dnp=False, extra_props=""):
        """nets: {pin_number: netname}. Places the symbol at (x,y) unrotated and a label on every named pin end."""
        self.used.add(sym.name)
        fp = footprint if footprint is not None else sym.footprint
        pinlines, labels = [], []
        for p in sym.pins:
            pinlines.append(f'    (pin "{p.number}" (uuid "{U(self.project + ref + p.number)}"))')
            if p.number in nets:
                lx, ly = sym.pin_end(p)
                sx, sy = x + lx, y - ly
                rot = {"L": 180, "R": 0, "T": 90, "B": 270, "N": 0}[p.side]
                if isinstance(sym, VSym):
                    rot = 90 if p.side == "T" else 270
                just = {"L": "right bottom", "R": "left bottom", "T": "left bottom", "B": "left bottom", "N": "left bottom"}[p.side]
                labels.append(f'  (label "{nets[p.number]}" (at {sx:.2f} {sy:.2f} {rot}) (fields_autoplaced yes) '
                              f'{FONT.replace(")))", ")) (justify " + just + "))")} '
                              f'(uuid "{U(self.project + ref + p.number + "lbl")}"))')
        props = (f'    (property "Reference" "{ref}" (at {x:.2f} {y - sym.hh - 2.54:.2f} 0) {FONT})\n'
                 f'    (property "Value" "{esc(value)}" (at {x:.2f} {y + sym.hh + 2.54:.2f} 0) {FONT})\n'
                 f'    (property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) {FONT_HIDE})\n'
                 f'    (property "Datasheet" "~" (at {x:.2f} {y:.2f} 0) {FONT_HIDE})\n{extra_props}')
        in_bom = "no" if sym.power else "yes"
        self.items.append(
            f'  (symbol (lib_id "synnefo:{sym.name}") (at {x:.2f} {y:.2f} 0) (unit 1)\n'
            f'    (exclude_from_sim no) (in_bom {in_bom}) (on_board {in_bom}) (dnp {"yes" if dnp else "no"})\n'
            f'    (uuid "{U(self.project + ref)}")\n{props}\n' + "\n".join(pinlines) + "\n"
            f'    (instances (project "{self.project}" (path "/{self.root}" (reference "{ref}") (unit 1))))\n  )')
        self.items.extend(labels)

    def note(self, text, x, y, size=1.27):
        self.counter += 1
        self.items.append(f'  (text "{esc(text)}" (exclude_from_sim no) (at {x:.2f} {y:.2f} 0) '
                          f'(effects (font (size {size} {size})) (justify left bottom)) '
                          f'(uuid "{U(self.project + "note" + str(self.counter))}"))')

    def emit(self):
        libs = "\n".join(BY_NAME[n].sexp("synnefo:") for n in sorted(self.used))
        tb = "".join(f'    (comment {i + 1} "{esc(c)}")\n' for i, c in enumerate(self.comments))
        return (f'(kicad_sch (version 20231120) (generator "synnefo_gen") (generator_version "1.0")\n'
                f'  (uuid "{self.root}")\n  (paper "A3")\n'
                f'  (title_block (title "{esc(self.title)}") (date "{DATE}") (rev "0.1")\n'
                f'    (company "Flip my flipper (Synnefo Handheld)")\n{tb}  )\n'
                f'  (lib_symbols\n{libs}\n  )\n' + "\n".join(self.items) + "\n"
                f'  (sheet_instances (path "/" (page "1")))\n)\n')


# ------------------------------------------------------------- footprints
def pad(num, kind, x, y, w, h, shape, layers, drill=None, net=None, uid=""):
    d = f" (drill {drill})" if drill else ""
    n = f' (net {net[0]} "{net[1]}")' if net else ""
    rr = " (roundrect_rratio 0.25)" if shape == "roundrect" else ""
    return (f'(pad "{num}" {kind} {shape} (at {x:.3f} {y:.3f}) (size {w} {h}){d} '
            f'(layers {layers}){rr}{n} (uuid "{U(uid + "pad" + str(num))}"))')


class FP:
    def __init__(self, name, descr, pads, bbox, silk_note=""):
        self.name, self.descr, self.pads, self.bbox = name, descr, pads, bbox

    def body(self, ref, value, uidseed, nets=None):
        x0, y0, x1, y1 = self.bbox
        pads = []
        for p in self.pads:
            num, kind, x, y, w, h, shape, layers, drill = p
            net = nets.get(num) if nets else None
            pads.append("  " + pad(num, kind, x, y, w, h, shape, layers, drill, net, uidseed))
        # make pad uuids unique per footprint instance
        cy = f"(fp_rect (start {x0:.2f} {y0:.2f}) (end {x1:.2f} {y1:.2f}) (stroke (width 0.05) (type default)) (fill none) (layer \"F.CrtYd\") (uuid \"{U(uidseed + 'crt')}\"))"
        sx0, sy0, sx1, sy1 = x0 + 0.25, y0 + 0.25, x1 - 0.25, y1 - 0.25
        silk = f"(fp_rect (start {sx0:.2f} {sy0:.2f}) (end {sx1:.2f} {sy1:.2f}) (stroke (width 0.12) (type default)) (fill none) (layer \"F.SilkS\") (uuid \"{U(uidseed + 'slk')}\"))"
        if self.pads[0][1] == "smd":
            silk = ""
        return pads, cy, silk

    def mod_file(self):
        pads, cy, silk = self.body("REF**", self.name, "lib/" + self.name)
        return (f'(footprint "{self.name}" (version 20240108) (generator "synnefo_gen") (generator_version "1.0")\n'
                f'  (layer "F.Cu")\n  (descr "{esc(self.descr)}")\n  (tags "synnefo skeleton")\n'
                f'  (property "Reference" "REF**" (at 0 -3 0) (layer "F.SilkS") {FONT.replace(")))", ")))")})\n'
                f'  (property "Value" "{self.name}" (at 0 3 0) (layer "F.Fab") {FONT})\n'
                f'  (property "Footprint" "" (at 0 0 0) (layer "F.Fab") hide {FONT})\n'
                f'  (property "Datasheet" "" (at 0 0 0) (layer "F.Fab") hide {FONT})\n'
                f'  (attr {"smd" if self.pads[0][1] == "smd" else "through_hole"})\n  {cy}\n  {silk}\n' +
                "\n".join(pads) + "\n)\n")

    def placed(self, ref, value, x, y, nets, rot=0):
        seed = f"{ref}@{self.name}"
        pads, cy, silk = self.body(ref, value, seed, nets)
        r = f" {rot}" if rot else ""
        return (f'(footprint "synnefo:{self.name}" (layer "F.Cu") (uuid "{U(seed)}") (at {x:.3f} {y:.3f}{r})\n'
                f'  (descr "{esc(self.descr)}")\n'
                f'  (property "Reference" "{ref}" (at 0 {self.bbox[1] - 1.2:.2f} 0) (layer "F.SilkS") (uuid "{U(seed + "r")}") {FONT})\n'
                f'  (property "Value" "{esc(value)}" (at 0 {self.bbox[3] + 1.2:.2f} 0) (layer "F.Fab") (uuid "{U(seed + "v")}") {FONT})\n'
                f'  (property "Footprint" "synnefo:{self.name}" (at 0 0 0) (layer "F.Fab") hide (uuid "{U(seed + "f")}") {FONT})\n'
                f'  (attr {"smd" if self.pads[0][1] == "smd" else "through_hole"})\n  {cy}\n  {silk}\n' +
                "\n".join(pads) + "\n)")


TH = '"*.Cu" "*.Mask"'


def header(name, rows, cols, descr):
    pads = []
    for n in range(1, rows * cols + 1):
        if cols == 2:
            col, row = (n - 1) % 2, (n - 1) // 2   # IDC numbering: 1 2 / 3 4 / ...
        else:
            col, row = 0, n - 1
        shape = "rect" if n == 1 else "circle"
        pads.append((str(n), "thru_hole", col * 2.54, row * 2.54, 1.7, 1.7, shape, TH, 1.0))
    w = (cols - 1) * 2.54
    h = (rows - 1) * 2.54
    return FP(name, descr, pads, (-1.77, -1.77, w + 1.77, h + 1.77))


FP_IDC = header("IDC_Header_2x05_P2.54mm_Vertical", 5, 2,
                "2x05 2.54 mm header footprint for the SMIS port connector; shrouded/box-header mechanical outline and orientation to be set once the part is chosen")
FP_H8 = header("PinHeader_1x08_P2.54mm_Vertical", 8, 1, "1x08 2.54 mm pin header")
FP_H3 = header("PinHeader_1x03_P2.54mm_Vertical", 3, 1, "1x03 2.54 mm pin header")
SMDL = '"F.Cu" "F.Paste" "F.Mask"'
FP_SOIC8 = FP("SOIC-8_3.9x4.9mm_P1.27mm", "SOIC-8, 3.9 mm body, 1.27 mm pitch (generic 24Cxx footprint)",
              [(str(n), "smd", -2.475, -1.905 + (n - 1) * 1.27, 1.95, 0.6, "roundrect", SMDL, None) for n in range(1, 5)] +
              [(str(n), "smd", 2.475, 1.905 - (n - 5) * 1.27, 1.95, 0.6, "roundrect", SMDL, None) for n in range(5, 9)],
              (-3.4, -2.7, 3.4, 2.7))
FP_C = FP("C_0603_1608Metric", "Capacitor 0603 (pad geometry approximate, check against the chosen part)",
          [("1", "smd", -0.825, 0, 0.8, 0.95, "roundrect", SMDL, None), ("2", "smd", 0.825, 0, 0.8, 0.95, "roundrect", SMDL, None)],
          (-1.6, -0.9, 1.6, 0.9))
FP_R = FP("R_0603_1608Metric", "Resistor 0603 (pad geometry approximate, check against the chosen part)",
          [("1", "smd", -0.825, 0, 0.8, 0.95, "roundrect", SMDL, None), ("2", "smd", 0.825, 0, 0.8, 0.95, "roundrect", SMDL, None)],
          (-1.6, -0.9, 1.6, 0.9))
ALL_FPS = [FP_IDC, FP_H8, FP_H3, FP_SOIC8, FP_C, FP_R]

# ------------------------------------------------------------ PN532 adapter
PN_NETS = ["GND", "3V3_P", "5V_P", "SCK", "MOSI", "MISO", "CS", "IRQ", "IDC", "IDD", "VCC_PN", "RSTPDN"]


def pn532_adapter():
    p = "pn532-adapter"
    s = Sch(p, "SMIS SM-S adapter for the PN532 V3 breakout (Variant A)",
            ["SKELETON v0.1: ERC/DRC not a substitute for review. See hardware/kicad/README.md.",
             "UNVERIFIED: PN532 V3 header pin order and position. Measure the real board before layout.",
             "Supply: breakout powered from 3V3_P by default (JP1 1-2). Do not use 5V_P until the board's regulator is confirmed."])
    # SM-S connector J1: all ten pins labelled with their SMIS net names
    s.place(SYM_SMS, "J1", "SMIS_SM-S_10", 50.8, 88.9, {str(i + 1): n for i, n in enumerate(SMS_NAMES)})
    # supply select JP1
    s.place(SYM_JP, "JP1", "SupplySelect", 127.0, 63.5, {"1": "3V3_P", "2": "VCC_PN", "3": "5V_P"})
    # PN532 breakout header J2 (signal names -> SMIS nets)
    s.place(SYM_PN, "J2", "PN532_V3_8pin", 127.0, 101.6,
            {"1": "VCC_PN", "2": "GND", "3": "SCK", "4": "MISO", "5": "MOSI", "6": "CS", "7": "IRQ", "8": "RSTPDN"})
    # RSTPDN pull-up (keeps the chip out of hard power-down) and bulk capacitor on the breakout supply
    s.place(SYM_R, "R1", "10k", 160.02, 63.5, {"1": "VCC_PN", "2": "RSTPDN"})
    s.place(SYM_C, "C2", "10uF", 175.26, 63.5, {"1": "VCC_PN", "2": "GND"})
    # ID EEPROM
    s.place(SYM_EEP, "U1", "24C02", 220.98, 63.5,
            {"1": "GND", "2": "GND", "3": "GND", "4": "GND", "8": "3V3_P", "7": "GND", "6": "IDC", "5": "IDD"})
    s.place(SYM_C, "C1", "100nF", 248.92, 63.5, {"1": "3V3_P", "2": "GND"})
    # ERC power flags
    s.place(SYM_FLAG, "#FLG01", "PWR_FLAG", 220.98, 101.6, {"1": "3V3_P"})
    s.place(SYM_FLAG, "#FLG02", "PWR_FLAG", 233.68, 101.6, {"1": "GND"})
    s.place(SYM_FLAG, "#FLG03", "PWR_FLAG", 246.38, 101.6, {"1": "5V_P"})
    s.note("SMIS v0.2 SM-S port (08-smis-v0.2.md): 1 GND 2 3V3_P 3 5V_P 4 SCK 5 MOSI 6 MISO 7 CS 8 IRQ 9 IDC 10 IDD", 25.4, 38.1)
    s.note("PN532 SPI: mode 0, LSB first, max 5 MHz, IRQ active low (06-nfc-modules.md). RSTPDN tied high: reset by power cycling 3V3_P.", 25.4, 43.18)
    s.note("Net names that match the breakout silkscreen: SSEL = CS. Breakout pin names/order are NOT verified.", 25.4, 48.26)
    s.note("ID: 24C02-class EEPROM at 0x50 on IDD/IDC, powered from 3V3_P. WP grounded so it can be programmed (set per release).", 190.5, 38.1)
    s.note("Candidate part: ElectronicsComp M24C04-WMN6P SOIC-8 is in Indian stock; its E0 pin differs from 24C02 A0 - check before freezing.", 190.5, 43.18)
    write(f"{OUT}/{p}/{p}.kicad_sch", s.emit())
    write(f"{OUT}/{p}/{p}.kicad_pro", json.dumps(
        {"meta": {"filename": f"{p}.kicad_pro", "version": 1}, "sheets": [[s.root, "Root"]]}, indent=2) + "\n")
    write(f"{OUT}/{p}/sym-lib-table",
          '(sym_lib_table\n  (version 7)\n  (lib (name "synnefo")(type "KiCad")(uri "${KIPRJMOD}/../lib/synnefo.kicad_sym")(options "")(descr "Synnefo skeleton symbols"))\n)\n')
    write(f"{OUT}/{p}/fp-lib-table",
          '(fp_lib_table\n  (version 7)\n  (lib (name "synnefo")(type "KiCad")(uri "${KIPRJMOD}/../lib/synnefo.pretty")(options "")(descr "Synnefo skeleton footprints"))\n)\n')
    pn532_pcb(p)


def pn532_pcb(p):
    nets = {n: i + 1 for i, n in enumerate(PN_NETS)}

    def nn(name):
        return (nets[name], name)

    j1 = {str(i + 1): nn(n) for i, n in enumerate(SMS_NAMES)}
    j2 = {str(i + 1): nn(n) for i, n in enumerate(["VCC_PN", "GND", "SCK", "MISO", "MOSI", "CS", "IRQ", "RSTPDN"])}
    jp1 = {"1": nn("3V3_P"), "2": nn("VCC_PN"), "3": nn("5V_P")}
    u1 = {"1": nn("GND"), "2": nn("GND"), "3": nn("GND"), "4": nn("GND"), "5": nn("IDD"), "6": nn("IDC"),
          "7": nn("GND"), "8": nn("3V3_P")}
    W, H = 70.0, 50.0
    fps = [
        FP_IDC.placed("J1", "SMIS_SM-S_10", 8.0, 10.0, j1),
        FP_H3.placed("JP1", "SupplySelect", 35.0, 10.0, jp1),
        FP_H8.placed("J2", "PN532_V3_8pin", 55.0, 10.0, j2),
        FP_R.placed("R1", "10k", 42.0, 32.0, {"1": nn("VCC_PN"), "2": nn("RSTPDN")}),
        FP_C.placed("C2", "10uF", 42.0, 38.0, {"1": nn("VCC_PN"), "2": nn("GND")}),
        FP_SOIC8.placed("U1", "24C02", 20.0, 38.0, u1),
        FP_C.placed("C1", "100nF", 30.0, 38.0, {"1": nn("3V3_P"), "2": nn("GND")}),
    ]
    layers = ('(layers (0 "F.Cu" signal) (31 "B.Cu" signal) (32 "B.Adhes" user "B.Adhesive") (33 "F.Adhes" user "F.Adhesive") '
              '(34 "B.Paste" user) (35 "F.Paste" user) (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen") '
              '(38 "B.Mask" user) (39 "F.Mask" user) (40 "Dwgs.User" user "User.Drawings") (41 "Cmts.User" user "User.Comments") '
              '(42 "Eco1.User" user "User.Eco1") (43 "Eco2.User" user "User.Eco2") (44 "Edge.Cuts" user) (45 "Margin" user) '
              '(46 "B.CrtYd" user "B.Courtyard") (47 "F.CrtYd" user "F.Courtyard") (48 "B.Fab" user) (49 "F.Fab" user))')
    netlist = '(net 0 "")\n' + "\n".join(f'(net {i} "{n}")' for n, i in nets.items())
    outline = (f'(gr_rect (start 0 0) (end {W} {H}) (stroke (width 0.1) (type default)) (fill none) '
               f'(layer "Edge.Cuts") (uuid "{U(p + "outline")}"))')
    txt = (f'(gr_text "PN532 adapter v0.1 SKELETON\\nplacement only, unrouted\\nPN532 header ORDER/POSITION UNVERIFIED" '
           f'(at 8 48.5 0) (layer "F.SilkS") (uuid "{U(p + "txt")}") (effects (font (size 1 1)) (justify left bottom)))')
    body = (f'(kicad_pcb (version 20240108) (generator "synnefo_gen") (generator_version "1.0")\n'
            f'(general (thickness 1.6) (legacy_teardrops no))\n(paper "A4")\n{layers}\n'
            f'(setup (pad_to_mask_clearance 0.05) (allow_soldermask_bridges_in_footprints no))\n{netlist}\n' +
            "\n".join(fps) + f"\n{outline}\n{txt}\n)\n")
    write(f"{OUT}/{p}/{p}.kicad_pcb", body)


# --------------------------------------------------------- ST25R3916 module
def st25r3916_module():
    p = "st25r3916-module"
    s = Sch(p, "SMIS SM-S NFC module around the ST25R3916 (Variant B), BLOCK-LEVEL SKELETON",
            ["NOT A DESIGN. Blocked on ST documents (DS13541, AN5276, AN5240, AN5322, NFC08A1 schematic) and on an Indian chip source.",
             "Pin numbers marked TBD-n are unknown; pins 1,3,7,8,9,10,11,14,33 come from DS12484 Rev 3 text (old revision).",
             "Antenna, EMC filter, matching network and crystal values are intentionally absent."])
    s.place(SYM_SMS, "J1", "SMIS_SM-S_10", 50.8, 127.0, {str(i + 1): n for i, n in enumerate(SMS_NAMES)})
    s.place(SYM_ST, "U2", "ST25R3916 (QFN32) BLOCK", 160.02, 127.0,
            {"1": "3V3_P", "8": "5V_P", "10": "5V_P", "14": "VDD_RF", "TBD-1": "SCK", "TBD-2": "MOSI", "TBD-3": "MISO",
             "TBD-4": "CS", "TBD-5": "IRQ", "TBD-6": "GND", "7": "VDD_A", "3": "VDD_D", "9": "VDD_RF", "11": "VDD_AM",
             "33": "GND"})
    s.place(SYM_EEP, "U1", "24C02", 50.8, 66.04,
            {"1": "GND", "2": "GND", "3": "GND", "4": "GND", "8": "3V3_P", "7": "GND", "6": "IDC", "5": "IDD"})
    s.place(SYM_C, "C1", "100nF", 78.74, 66.04, {"1": "3V3_P", "2": "GND"})
    # datasheet decoupling (DS12484 Rev 3 section 4.2.11) - assignments to confirm against Figure 1 before layout
    s.place(SYM_C, "C10", "2.2uF", 215.9, 66.04, {"1": "VDD_A", "2": "GND"})
    s.place(SYM_C, "C11", "10nF", 228.6, 66.04, {"1": "VDD_A", "2": "GND"})
    s.place(SYM_C, "C12", "2.2uF", 241.3, 66.04, {"1": "VDD_D", "2": "GND"})
    s.place(SYM_C, "C13", "10nF", 254.0, 66.04, {"1": "VDD_D", "2": "GND"})
    s.place(SYM_C, "C14", "2.2uF", 266.7, 66.04, {"1": "VDD_AM", "2": "GND"})
    s.place(SYM_C, "C15", "1nF", 279.4, 66.04, {"1": "VDD_AM", "2": "GND"})
    s.place(SYM_FLAG, "#FLG01", "PWR_FLAG", 114.3, 93.98, {"1": "3V3_P"})
    s.place(SYM_FLAG, "#FLG02", "PWR_FLAG", 127.0, 93.98, {"1": "GND"})
    s.place(SYM_FLAG, "#FLG03", "PWR_FLAG", 139.7, 93.98, {"1": "5V_P"})
    s.note("SPI: CPOL 0, CPHA 1 (mode 1), MSB first, max 10 MHz; IRQ ACTIVE HIGH; no reset pin (power-cycle 3V3_P or command C0). DS12484 Rev 3.", 12.7, 20.32)
    s.note("Supply plan: VDD and VDD_TX from 5V_P (same supply, +-0.2 V); VDD_IO from 3V3_P; set sup3V only if supplied from 3.3 V. Do not supply VDD_A externally.", 12.7, 25.4)
    s.note("Decoupling per section 4.2.11: 2.2uF + 10nF on regulator pins, 1uF + 10nF on AGDC, 2.2uF + 1nF on VDD_AM. Net assignment on the right is a TO-CONFIRM placeholder.", 12.7, 30.48)
    s.note("VDD_RF is tied to VDD_DR in this skeleton: CONFIRM against Figure 1 (above 350 mA both tie to VDD_TX instead).", 12.7, 35.56)
    s.note("To add after reading AN5276/AN5240/AN5322: antenna coil, EMC filter, matching network (fixed first, AAT later), 27.12 MHz crystal and load capacitors, exposed-pad thermal vias, layout.", 12.7, 190.5)
    write(f"{OUT}/{p}/{p}.kicad_sch", s.emit())
    write(f"{OUT}/{p}/{p}.kicad_pro", json.dumps(
        {"meta": {"filename": f"{p}.kicad_pro", "version": 1}, "sheets": [[s.root, "Root"]]}, indent=2) + "\n")
    write(f"{OUT}/{p}/sym-lib-table",
          '(sym_lib_table\n  (version 7)\n  (lib (name "synnefo")(type "KiCad")(uri "${KIPRJMOD}/../lib/synnefo.kicad_sym")(options "")(descr "Synnefo skeleton symbols"))\n)\n')
    write(f"{OUT}/{p}/fp-lib-table",
          '(fp_lib_table\n  (version 7)\n  (lib (name "synnefo")(type "KiCad")(uri "${KIPRJMOD}/../lib/synnefo.pretty")(options "")(descr "Synnefo skeleton footprints"))\n)\n')


def main():
    write(f"{OUT}/lib/synnefo.kicad_sym", sym_lib())
    for fp in ALL_FPS:
        write(f"{OUT}/lib/synnefo.pretty/{fp.name}.kicad_mod", fp.mod_file())
    pn532_adapter()
    st25r3916_module()
    print("generated into", OUT)


if __name__ == "__main__":
    main()
