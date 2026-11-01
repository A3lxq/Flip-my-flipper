# Indian licence-exempt bands and equipment type approval

Condensed from a research-agent report (2026-11-01). **Facts and citations only; not legal advice.** `dot.gov.in` returned 403/404 to every fetch; `eservices.dot.gov.in` opened. G.S.R. 853(E) was read from a `thc.nic.in` copy of the Gazette PDF (government site, not a DoT/e-Gazette copy). G.S.R. 870(E), 1047(E) (2018 text) and the 2005 G.S.R. 45(E) text are secondary copies (taxguru, legitquest, TI e2e). G.S.R. 1048(E) (5 GHz) could not be opened from any primary source.

## Context: Telegraph Act repealed
Every delicensing rule below was made under the Indian Telegraph Act 1885 and the Indian Wireless Telegraphy Act 1933. Secondary sources (JSA, Verdictum) report the Telecommunications Act 2023 repealed both and commenced sections 1, 2, 10–30, 42–44, 46, 47, 50–58, 61, 62 on 26 June 2024. The eServices ETA page (updated 28 May 2025) says new applications under the Telegraph Act for licences and authorisations have stopped. How the old exemption rules are saved under the new Act: could not determine.

## Bands
All are "Exemption from Licence" rules on a non-interference, non-protection, shared basis.

**865–868 MHz — G.S.R. 853(E), 10 Dec 2021** (File R-11018/06/2020-PP; supersedes the 2005 865–867 MHz RFID rules; 2005 type approvals stay valid to end of life). https://www.thc.nic.in/Central%20Governmental%20Rules/use%20of%20low%20power%20Equipment%20in%20the%20frequency%20band%20865%20to%20868%20MHz%20for%20Short%20Range%20Devices%20Exemption%20from%20Licence%20Rules,2021.pdf
| Table | Use | Power | Duty / parameters | Bandwidth |
|---|---|---|---|---|
| I | Non-specific SRD | 25 mW e.r.p. | 1 % duty cycle; FHSS; max occupied bandwidth 50 kHz for 58+ hop channels (cell ambiguous) | EN 300 220 |
| II | Tracking, tracing, data acquisition | 500 mW e.r.p. | adaptive power control; ≤ 10 % (access points) / ≤ 2.5 %; ≤ 200 kHz | |
| III | Wideband data | 25 mW e.r.p. | ≤ 10 % / ≤ 2.8 % | > 600 kHz to ≤ 1 MHz (EN 304 220) |
| IV | RFID | 2 W e.r.p. only on 865.7, 866.3, 866.9, 867.5 MHz | transmit ≤ 4 s, ≥ 100 ms between | ≤ 200 kHz (EN 302 208) |
Rule 5: equipment "shall be type approved"; application to the Central Government in the annexure format; must comply with the EN standards; safety to ITU/ETSI/ANSI/BIS/ICNIRP. Rule 4: the Authority may direct relocation, power reduction or antenna change after a licensed user reports harmful interference. No amendment found.

**433.05–434.79 MHz — G.S.R. 347(E), 9 May 2022** (F. No. R-11019/01/2022-PP; supersedes the 2012 indoor rules and the 2015 very-low-power RFID rules G.S.R. 698(E); Gazette issue 332 dated 11 May 2022 per a news summary). https://eservices.dot.gov.in/sites/default/files/circular-notifications/the-use-of-low-power-radio-frequency-devices-in-the-frequency-band-433.05-to-434.79-mhz-exemption-from-license-rules-2022.pdf
Rows: 433.05–434.79 MHz 10 mW e.r.p. at ≤ 10 % duty cycle (EN 300 220); 1 mW with spectrum access per Note 1 (power density −13 dBm/10 kHz above 250 kHz bandwidth); 434.04–434.79 MHz 10 mW e.r.p. ≤ 25 kHz. Voice allowed at ≤ 25 kHz with listen-before-talk, ≤ 1 minute. Type approval required. (A different agent quoted "GSR 680(E)" from a secondary source; this primary reading supersedes it.)

**2.4 GHz.** (a) G.S.R. 45(E), 28 Jan 2005 (secondary copy): transmitter output 1 W (30 dBm) with 10 MHz or wider spread, max e.r.p. 4 W (36 dBm), antenna ≤ 5 m above roof top; type approval required; amendment status undetermined. (b) G.S.R. 1047(E), 18 Oct 2018, amended by G.S.R. 271(E), 9 May 2024 (read from eservices): rows for radio determination 25 mW e.i.r.p., RFID 2446–2454 MHz 500 mW, non-specific SRD 2400–2483.5 MHz 10 mW e.i.r.p., 5725–5875 MHz 25 mW; no Wi-Fi/BLE-specific row found. Which instrument governs BLE and Wi-Fi: could not determine.

**5 GHz — G.S.R. 1048(E), 22 Oct 2018** (text not opened; a press source says 18 Oct). Secondary (Linux wireless-regdb, third-party): 5150–5250 30 dBm EIRP; 5250–5350 24 dBm with DFS; 5470–5725 24 dBm with DFS; 5725–5875 30 dBm. Indoor/outdoor scope conflicting.

**125 kHz and 13.56 MHz — G.S.R. 870(E), 21 Dec 2021** (inductive applications; secondary copy at taxguru; number as printed there; supersedes the 2015 inductive rules). Note to rule 3 lists RFID, access control and NFC. Magnetic-field limits at 10 m (EN 300 330): 119–135 kHz 66 dBµA/m; 5000–30000 kHz (except listed sub-bands) −20 dBµA/m, which is how 13.56 MHz reads (no separate row; the agent says this seems low versus the usual ETSI limit, so check the Gazette). Type approval required.

**Infrared:** no WPC/DoT delicensing notification found.

## Equipment Type Approval (ETA)
- Each delicensing rule says equipment "shall be type approved". DoT's ETA page (https://eservices.dot.gov.in/equipment-type-approval-eta) says ETA "is required for the import, sale, and use of wireless communication devices that operate in de-licensed frequency bands or involve radio frequency (RF) transmission".
- OM R-11017/01/2018-PP(part-1), 9 Sept 2024: ETA for licence-exempt wireless equipment on self-declaration via Saral Sanchar; ETA holders must get DGFT NOC or other clearances before import. OM of 26 Feb 2019: self-declaration for finished products including short-range devices; importer/authorised representative declaration may suffice for Customs.
- Applicant: manufacturer or Indian representative with authorisation. Excluded from self-declaration: radar, jamming devices, drones, satellite equipment. Documents: RF test report (accredited lab named with country; accepted accreditation scheme not stated), authorisation, technical literature. Fee ₹10,000 per model (Bharat Kosh); validity lifetime unless revoked; declarant liable for wrong declarations and must cooperate with audits. Applicant manual: 13 Jun 2023.
- Test/prototype/sample/pre-launch devices: OM of 26 Feb 2019 (Annex-5) exempts them from ETA up to 1,000 units per model with a Customs undertaking, not for commercial sale. The 2022 import compendium (scanned, read via summaries) also says "Free"-category devices use self-declaration ETA plus a system-generated import undertaking, "Restricted" ones need scrutiny-based ETA and a WPC import licence; dealers may need a Dealer Possession Licence; domestic OEMs may import radio modules against their DPL (OM 26 Jul 2019).
- Module versus end product: no primary source. Espressif publishes module-level self-declaration ETAs (e.g. for ESP32-PICO-V3-ZERO); consultancies disagree on whether a module ETA covers a host product.
- No labelling requirement and no penalty text for selling without ETA found. No special treatment of receive/transmit/replay tools found; jamming devices are excluded from self-declaration.

## Open questions
Saving of the old exemption rules under the 2023 Act; 13.56 MHz limit; G.S.R. 1048(E) text; which 2.4 GHz instrument governs; module-ETA reuse; applicant for an integrator; CC1101 configurable outside limits; prototype exemption scope; labelling; penalties; DPL need; accepted test labs; BIS, Legal Metrology, safety (see report 09).
