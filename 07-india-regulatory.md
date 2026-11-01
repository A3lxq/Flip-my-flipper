# India regulatory research (2026-11-01)

**This is a collection of what sources say. It is not legal advice and reaches no conclusion about whether the product is lawful.** It was produced by three research agents; I have not re-read the primary documents myself. Source labels: **[LAW]** Gazette rule/order read; **[GUIDANCE]** official FAQ, memo, SOP; **[SECONDARY]** consultancy, news, blog, aggregator, or a copy not hosted by the government; **[NOT READ]** known to exist but not opened. "Could not determine" means unconfirmed.

Access problems affecting everything below: `dot.gov.in` returned 403 for every fetch (DoT's `eservices.dot.gov.in` portal opened), India Code returned 403, e-Gazette gave a certificate error, `meity.gov.in` listing pages returned 403, and several scanned or Hindi-encoded PDFs could not be text-extracted.

## 1. Headline findings

1. **No official Indian source names the Flipper Zero.** No notification, ban, DGFT/CBIC order, advisory, parliamentary answer or court judgment was found. The "banned in India" claim appears only on unsourced pages. Absence in this search is not proof of absence; Lok Sabha/Rajya Sabha question databases, CBIC notices and Indian Kanoon still need direct searching.
2. **Jammers are prohibited.** Telecommunications Act 2023 s.42(3)(a) and s.48 (possession or use of blocking equipment without permission; up to 3 years or ₹50 lakh; cognizable, non-bailable), and a DoT advisory of 1 July 2022 (private persons cannot buy or use jammers) [LAW + GUIDANCE/SECONDARY]. The device must have no blocking or jamming function.
3. **Possessing/dealing in radio equipment needs authorisation or an exemption.** Telecom Act s.3(1)(c) (commencement of s.3 not confirmed) and the Telecommunications (Radio Equipment Possession Authorisation) Rules, 2026, G.S.R. 592(E), 8 July 2026 [SECONDARY summaries; Gazette text not read]. Whether a maker/seller of licence-exempt-band devices needs an authorisation under these rules is an open question.
4. **Type approval (ETA) is required** for import, sale and use of wireless equipment in licence-exempt bands, via self-declaration on Saral Sanchar (₹10,000 per model, lifetime validity) [GUIDANCE]. Self-declaration excludes radar, jamming devices, drones and satellite equipment.
5. **Licence-exempt bands have power and duty-cycle limits** that bind the radio design (table in §3).
6. **BIS registration may apply to the Li-ion cell and charger**; which Schedule item (if any) covers a modular handheld is unresolved (§5).

## 2. Statutes and rules (law-landscape agent)

| Instrument | Provision | Relevance | Status | Label |
|---|---|---|---|---|
| Telecommunications Act 2023 | s.3(1)(c), 3(3): authorisation to possess radio equipment; exemption power | Possession | s.3/s.32 commencement not confirmed | SECONDARY copy |
| Same | s.42(3)(a),(d): jammers, over-SIM radio equipment; up to 3 years or ₹50 lakh or both; s.42(7) cognizable and non-bailable | Jammers | In force (S.O. 2408(E), 26 June 2024) | SECONDARY confirmation |
| Same | s.43: search and seizure of unauthorised radio equipment | Enforcement | In force | SECONDARY copy |
| Same | s.48: no possession/use of blocking equipment without permission | Jammers | In force from 5 July 2024 per a compiled source | SECONDARY |
| Same | s.19: standards and conformity assessment for telecom equipment | MTCTE basis | In force | SECONDARY |
| Same | s.60: repeals Indian Telegraph Act 1885 and Indian Wireless Telegraphy Act 1933; s.61: old rules continue | Which regime governs old exemption rules | Could not determine if s.60 is in force | SECONDARY |
| Radio Equipment Possession Authorisation Rules 2026 | G.S.R. 592(E), 8 July 2026; purposes: manufacture, purchase or import for sale, hire, repair, testing, demonstration; testing tier up to 100 mW; exemptions in Rule 10 | Dealing/testing | Applications reported open from 6 Aug 2026 | SECONDARY (Khaitan summary, aggregator) |
| DoT letter 22 March 2023 | Online sale/purchase of wireless equipment without authorisation illegal unless exempt | Online sale | Guidance, pre-2023 Act | SECONDARY snippet |
| CCPA guidelines on e-commerce radio equipment | Platforms list only compliant equipment, show frequency range and ETA; remove non-compliant listings in 24 hours | Selling online | May 2025 | SECONDARY (news) |
| DoT advisory 1 July 2022 | Private persons cannot procure/use jammers; selling/importing jammers prohibited | Jammers | Guidance | SECONDARY |
| IT Act 2000 | ss.43 (civil), 66 (up to 3 years or ₹5 lakh), 66B–66F, 69, 70, 72 | Unauthorised access, credential misuse; no research exemption found | In force | SECONDARY copies |
| Bharatiya Nyaya Sanhita 2023 | ss.303, 318, 319, 336 | Fact-dependent | In force; text unread | SECONDARY listings |
| CERT-In RVDCP (3 Sept 2021) | Discloser responsible for own actions, must comply with law; "reporting … does not imply being exempt" | No safe harbour | Policy | Primary page fetched |
| CERT-In Directions 28 Apr 2022 (s.70B(6)) | Incident reporting in 6 hours | Applicability to a hardware seller unclear | Direction | SECONDARY |

## 3. Licence-exempt bands (spectrum agent)

All were made under the old Telegraph/Wireless Acts. Whether they are saved under the 2023 Act: **could not determine**. Each exempts equipment on a non-interference, non-protection basis and requires type approval.

| Band / use | Key limits | Source | Label |
|---|---|---|---|
| 865–868 MHz non-specific SRD (Table I) | 25 mW e.r.p.; 1% duty cycle; frequency hopping; 50 kHz occupied bandwidth with 58 or more hop channels (cell ambiguous in extraction); EN 300 220 | G.S.R. 853(E), 10 Dec 2021 (supersedes the 2005 865–867 MHz RFID rules) | [LAW], read from a government mirror |
| 865–868 MHz tracking/tracing/data (Table II) | 500 mW e.r.p.; adaptive power control; ≤10% duty cycle (access points) or ≤2.5%; ≤200 kHz | same | [LAW] |
| 865–868 MHz wideband (Table III) | 25 mW e.r.p.; ≤10% or ≤2.8%; 600 kHz–1 MHz | same | [LAW] |
| 865–868 MHz RFID (Table IV) | 2 W e.r.p. only on 865.7, 866.3, 866.9, 867.5 MHz; transmit ≤4 s with ≥100 ms between | same | [LAW] |
| 433.05–434.79 MHz | 10 mW e.r.p., ≤10% duty cycle; 1 mW and 434.04–434.79 MHz rows | G.S.R. 347(E), 9 May 2022 (supersedes 2012 and 2015 rules) | [LAW], primary DoT portal copy |
| 2400–2483.5 MHz (Wi-Fi/BLE) | G.S.R. 45(E) (2005): 1 W output, 4 W e.r.p. G.S.R. 1047(E) (2018, amended by G.S.R. 271(E) 9 May 2024): 10 mW e.i.r.p. non-specific, 25 mW radio determination, 500 mW RFID 2446–2454 MHz | G.S.R. 45(E); G.S.R. 1047(E) | 2005 text SECONDARY copy; 2018 text SECONDARY copy; 2024 amendment [LAW]. Which instrument governs BLE: **could not determine** |
| 5 GHz | Secondary regdb numbers 30/24/24/30 dBm EIRP over four bands; DFS in two | G.S.R. 1048(E), 22 Oct 2018 (date also reported 18 Oct) | [NOT READ]; indoor/outdoor scope conflicting |
| 125 kHz LF RFID | 66 dBµA/m at 10 m (119–135 kHz) | G.S.R. 870(E), 21 Dec 2021 (inductive applications; number as printed by taxguru) | SECONDARY copy |
| 13.56 MHz NFC/RFID | Falls in the "5000–30000 kHz" row: −20 dBµA/m at 10 m by the agent's reading; no separate 13.56 MHz row; the agent says this seems low vs ETSI EN 300 330 | same | SECONDARY copy; **needs Gazette check** |
| Infrared | No notification found | none | n/a |
| 315 MHz and 915 MHz | Not found in any source read | none | n/a |

Discrepancy resolved: an earlier agent cited "GSR 680(E)" for 433 MHz from a secondary source. The spectrum agent read G.S.R. 347(E) (2022) directly, which supersedes the older 433 MHz rules. I rely on G.S.R. 347(E).

## 4. Equipment Type Approval and import (spectrum + BIS agents)

- **Rule text:** each exemption notification says the equipment "shall be type approved" [LAW]. DoT's ETA page says ETA "is required for the import, sale, and use" of devices in de-licensed bands or involving RF transmission [GUIDANCE].
- **Self-declaration route:** DoT OM of 9 Sept 2024 (all ETA applications for licence-exempt wireless equipment on self-declaration basis; ETA holders must still get DGFT NOC or other clearances before import) and OM of 26 Feb 2019 [GUIDANCE]. Excluded: radar, jamming devices, drones, satellite equipment.
- **Applicant:** manufacturer or Indian representative with manufacturer authorisation. Documents: RF test report from a named accredited lab (accepted accreditation scheme not stated), authorisation, technical literature. Fee ₹10,000 per model; validity: lifetime unless revoked. Declarant is liable for wrong declarations.
- **Module vs end product:** unresolved. Espressif publishes module-level self-declaration ETAs for other modules, but no Espressif ETA for the ESP32-S3-WROOM-1 was found; consultancies disagree on whether a module ETA covers a host.
- **Prototype/sample exemption:** a secondary summary of the DoT import compendium (scanned, unreadable) mentions an OM exempting test/prototype/sample/pre-launch devices from ETA up to 1,000 units per model under a Customs undertaking, not for commercial sale. Unverified and absent from the ETA page.
- **Dealers:** dealers in licence-band equipment may need a Dealer Possession Licence; domestic OEMs may import radio modules against their DPL (OM 26 July 2019) [secondary summary].
- **Penalty for selling without ETA:** no primary source found.
- **Labelling of the ETA number:** none found.
- **DGFT import status of HS 8517 62 etc.:** could not open the ITC(HS) schedule. This project intends Indian-sourced parts only, so import matters mostly for finished-unit components.
- **Radio equipment possession authorisations:** moved to a new Authorisation Portal from 6 Aug 2026 [secondary snippet]; interaction with ETA: could not determine.

## 5. Product safety and other obligations (BIS agent)

- **BIS Compulsory Registration (CRS):** Electronics and IT Goods (Requirement of Compulsory Registration) Order, 2021, S.O. 1248(E), 18 Mar 2021, as amended [LAW].
  - Schedule items of interest: 20 (sealed Li secondary cells/batteries for portable use, IS 16046 Pt 2:2018), 16/17 (power adaptors), 1/2/15/23/30/44 (electronic games, laptops/tablets, ADP machines, mobile phones, power banks, smart watches).
  - **No entry is named for a modular handheld security/electronics device.** Which item, if any, applies: could not determine.
  - S.O. 4997(E) (29 Oct 2025): IS 13252 Pt 1:2010 and IS 616:2017 replaced by IS/IEC 62368 Pt 1:2023; old standards run in parallel until 1 Nov 2028.
  - FAQ (28 Sept 2022, currency unknown) [GUIDANCE]: integral sealed cells/batteries need BIS registration only if the host product is also covered (Q43, Q66); batteries and adaptors are independently registered (Q40, Q44); finished goods only, not components (Q34); not applicable to goods imported for demonstration, R&D or testing (Q35; underlying circular not opened).
  - Exemptions found: export-only goods, specific MeitY exemption letter, highly specialised equipment under 100 units per model per year with technical criteria (poor fit for a handheld). No small-quantity domestic exemption found.
- **TEC MTCTE:** Phase III (22.09.2021) lists IoT Gateway, Tracking Device, Smart/CCTV Camera, Smart Watch (exempted by S.O. 2372(E), 24 May 2022) and "Equipment Operating in 2.4 GHz and 5 GHz Band" [LAW]. The essential-requirement text defining the last category was not obtained, so whether a Wi-Fi/Bluetooth handheld falls in it: could not determine. No Bluetooth, NFC or sub-GHz category found.
- **E-Waste (Management) Rules 2022:** G.S.R. 801(E), 2 Nov 2022, effective 1 Apr 2023. Producer definition covers anyone manufacturing and offering equipment under their own brand (CPCB SOP quote). Registration on the CPCB portal. Rule 2(c) excludes micro enterprises under the MSMED Act (via a secondary copy; scope and thresholds not verified). Whether the device is in Schedule I: not confirmed.
- **Battery Waste Management Rules 2022:** separate regime; whether a maker with a fitted cell has producer duties: could not determine.
- **Shipping Li-ion in equipment:** IATA/ICAO guidance (UN 3481, PI 967 Section II; UN 38.3 test required). My arithmetic: one 3000–3500 mAh cell at 3.6–3.7 V is about 11–13 Wh, under 20 Wh. India-specific carriage rules (DGCA, PESO): not found.
- **Legal Metrology (Packaged Commodities) Rules 2011:** Rule 6 declarations on packages (manufacturer and address, generic name, net quantity, month/year of manufacture, MRP, consumer-complaint contact, country of origin for imports); website declarations for e-commerce. QR-code relief status: could not determine.

## 6. Design guardrails that follow (PROPOSED requirement R20)

Marked where they come from sources vs my inference.

1. **No jamming or blocking function of any kind** [sources].
2. **Sub-GHz transmit locked** to 865–868 MHz (within Table I/II/III/IV limits and duty cycle, and only the allowed channels for the RFID row) and 433.05–434.79 MHz (10 mW e.r.p., 10% duty cycle). No 315 MHz or 915 MHz transmit [inference from sources; 315/915 not found as exempt]. Firmware enforces power and duty cycle.
3. **Receive-only is the default**; transmit and replay are explicit, logged user actions [inference].
4. **Wi-Fi/BLE** only through an approved module configuration; verify which 2.4 GHz rule applies before fixing power [open].
5. **13.56 MHz and 125 kHz** field strength must be checked against G.S.R. 870(E) once the Gazette text is read; module power settings capped accordingly [open].
6. **Region-aware configuration** with the India profile as default [inference].
7. **Acceptable-use acknowledgement** and authorised-testing wording in documentation [inference]; liability for user-installed firmware is a lawyer question.
8. **ETA, BIS and e-waste** obligations are decided before any sale; the prototype stage may use the prototype/R&D carve-outs, which are unverified.
9. **Do not market** the device as a way to evade restrictions [brief].

## 7. Questions for a lawyer or lab (combined, deduplicated)

1. Does the 2026 Possession Authorisation Rules regime require an authorisation for Synnefo as maker/seller, and for buyers? Are licence-exempt-band devices excluded?
2. Are Telecom Act ss.3, 32 and 60 in force? How are the old exemption rules saved under s.61/62?
3. Does a transmit/replay function create exposure under IT Act ss.43, 66, 66C, 66D or BNS ss.318, 319, 336 for the maker or seller, as opposed to the user?
4. Who must file the ETA (Synnefo as manufacturer, or the module maker), and is a module ETA enough for the end product? Does adding sub-GHz and NFC modules require a new declaration? Does the jamming-device exclusion reach a multi-radio tool?
5. Which 2.4 GHz instrument (G.S.R. 45(E) or 1047(E)) governs Wi-Fi/BLE, and what are the exact limits? Get the 5 GHz Gazette (G.S.R. 1048(E)).
6. Is 13.56 MHz really limited to −20 dBµA/m at 10 m under G.S.R. 870(E)? Is there a separate row?
7. Which BIS CRS Schedule item (if any) covers the handheld; does the fitted Li-ion pack need its own R-number; is a bought-in registered charger enough?
8. Does MTCTE's "Equipment operating in 2.4 GHz and 5 GHz band" category cover a Wi-Fi/BLE handheld?
9. Is the prototype/sample ETA exemption (1,000 units) real and does it cover pre-production units or any transfer?
10. Dealer Possession Licence for sale; DGFT import status of modules.
11. E-waste Schedule I coverage and MSME micro-enterprise status; Battery Waste Management Rules for a fitted cell.
12. Disclaimers, acceptable-use terms, buyer verification, and responsibility for custom firmware; written authorisation research customers should hold.
13. CERT-In 2022 Directions: do they apply to a hardware vendor?

## 8. Source index (selected)

- G.S.R. 853(E) text: https://www.thc.nic.in/Central%20Governmental%20Rules/use%20of%20low%20power%20Equipment%20in%20the%20frequency%20band%20865%20to%20868%20MHz%20for%20Short%20Range%20Devices%20Exemption%20from%20Licence%20Rules,2021.pdf
- G.S.R. 347(E) (433 MHz): https://eservices.dot.gov.in/sites/default/files/circular-notifications/the-use-of-low-power-radio-frequency-devices-in-the-frequency-band-433.05-to-434.79-mhz-exemption-from-license-rules-2022.pdf
- DoT ETA page: https://eservices.dot.gov.in/equipment-type-approval-eta
- BIS CRS order with amendments: https://www.bis.gov.in/wp-content/uploads/2021/11/Electronics-and-Information-Technology-Goods-Requirement-of-Compulsory-Registration-Order-2021-1.pdf
- BIS migration to IS/IEC 62368-1: https://www.bis.gov.in/wp-content/uploads/2025/11/Migration-to-IS-IEC-62368-Part-1-2023-from-IS-13252-Part-1-2010-and-IS-616-2017.pdf
- CRS FAQ: https://www.crsbis.in/BIS/app_srv/tdc/gl/docs/Modified_FAQs.pdf
- TEC MTCTE Phase III/IV notification: http://tec.gov.in/pdf/MTCTE/Notification_MTCTE_3_4.pdf
- TEC exemption of five items: https://www.tec.gov.in/pdf/MTCTE/Exemption%20of%20five%20items.pdf
- CERT-In RVDCP: https://www.cert-in.org.in/RVDCP.jsp
- CPCB e-waste SOP: https://eprewaste.cpcb.gov.in/assets/landingpage%20PDF/SOP_for_grant_of_Registration_to_Producer_on_under_Ewaste_Rules_2022.pdf
- Telecommunications Act 2023 copy (secondary): https://taxguru.in/?p=898706
