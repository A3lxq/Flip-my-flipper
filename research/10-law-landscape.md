# Legal landscape for Flipper-style devices in India

Condensed from a research-agent report (checked 1 Nov 2026). **Not legal advice.** India Code (403), e-Gazette (certificate error) and DoT ETA memoranda (403) were unreadable; statute wording comes from reproductions (taxguru.in, lawx.in) and law-firm summaries and is SECONDARY. Search results were filtered through a summarising tool, so wording is not guaranteed verbatim.

## Flipper Zero in India
No primary source found: no notification, ban, DGFT restriction, customs notice, advisory, parliamentary answer or court judgment names "Flipper Zero". The "banned in India" claim appears only on unsourced secondary pages. Foreign actions (Brazil's Anatel, Amazon's 2023 listing ban) are documented elsewhere but are not Indian. "Not found" does not mean "does not exist"; Lok Sabha/Rajya Sabha question databases, CBIC notices and Indian Kanoon still need direct searching.

## Telecommunications Act, 2023 (Act 44 of 2023)
| Provision | Text (short) | Status |
|---|---|---|
| s.3(1)(c), 3(3) | possession of radio equipment needs authorisation; Centre may exempt | commencement not confirmed |
| s.19 | standards and conformity assessment | in force (S.O. 2408(E), 26 Jun 2024) |
| s.32, Second Schedule | breach adjudication; severe penalty up to ₹5 crore | commencement not confirmed |
| s.42(3)(a),(d) | possessing or using equipment that blocks telecommunication; radio equipment exceeding specified SIMs without authorisation; up to 3 years or ₹50 lakh or both; s.42(7) cognizable and non-bailable; s.42(8) trial by Chief Metropolitan/Chief Judicial Magistrate | in force |
| s.43 | search and seizure of unauthorised radio equipment | in force |
| s.48 | no possession/use of blocking equipment without permission | in force from 5 Jul 2024 (compiled source, S.O. 2623(E)) |
| s.60 | repeals Indian Telegraph Act 1885 and Indian Wireless Telegraphy Act 1933 | could not determine if in force |
| s.61 | old rules continue until superseded | in force |
No jammer-specific rules under the 2023 Act found (COAI request of 5 Feb 2025 pending).

## Telecommunications (Radio Equipment Possession Authorisation) Rules, 2026
G.S.R. 592(E), 8 July 2026 (summaries only; Gazette text not read): authorisation for dealing in radio equipment (manufacture, purchase or import for sale, hire, repair, testing, demonstration); exemptions in Rule 10 (existing licensees, other authorisations, statutory exemptions, spectrum assignees, amateur operators, subscribers who cannot manufacture, sell or let out); testing tier up to 100 mW (no interference protection; above 100 mW follow the spectrum assignment terms; no transfer of possession); inventory and loss reporting; conformity with notified standards; security vetting possible; breach treated as a breach under s.32; the 1965 possession rules not expressly repealed; applications reported open from 6 Aug 2026. Open: whether it covers a product built for sale and licence-exempt-band devices.

## Older guidance
DoT letter 22 Mar 2023 (online sale of wireless equipment without authorisation illegal unless exempt; snippet only); DoT jammer advisory 1 Jul 2022 (private persons cannot procure or use jammers; advertising/selling/importing jammers prohibited; boosters/repeaters restricted to licensed providers; SECONDARY report); DoT notice 21 Jan 2022 to e-commerce platforms. CCPA guidelines (about 27–30 May 2025, news only): platforms must list only compliant radio equipment, show frequency range and ETA details, remove non-compliant listings within 24 hours of a direction; fines reported January 2026.

## IT Act 2000 (secondary text)
s.43 civil liability for unauthorised access/damage; s.66 dishonest or fraudulent acts under s.43 up to 3 years or ₹5 lakh (verified via lawx); s.66B receiving stolen device; s.66C identity theft including fraudulent use of passwords; s.66D cheating by personation; s.66F cyber terrorism; s.69 interception; s.70 protected systems; s.72 breach of confidentiality. No research exemption found. Bharatiya Nyaya Sanhita 2023 ss.303, 318, 319, 336 (theft, cheating, cheating by personation, forgery) from secondary listings only.

## CERT-In
Responsible Vulnerability Disclosure and Coordination Policy (3 Sept 2021) https://www.cert-in.org.in/RVDCP.jsp : "Discloser shall be responsible for any action performed by her / him for discovering the vulnerability whatsoever"; "The reporting party must ensure to comply with all the extant laws and regulations while discovering the vulnerabilities"; "Reporting a vulnerability to CERT-In does not imply being exempt from compliance"; 120-day resolution target; no safe harbour. Directions of 28 Apr 2022 under s.70B(6): incident reporting within 6 hours (law-firm commentary only; relevance to a hardware seller unclear).

## Jammers and design implications
Stated by sources: no blocking/jamming function; transmit only in licence-exempt bands within limits; ETA when sold; possession of radio equipment needs authorisation or exemption; online sales must show frequency range and ETA. Agent's inference (not in sources): receive-only default, region-aware limits, acceptable-use acknowledgement; liability for user-installed firmware is a lawyer question. Authorised-testing practice: only the CERT-In policy was reached; it does not define authorisation or consent.

## Questions for a lawyer
Whether the 2026 possession rules require a manufacturer/dealer authorisation and whether licence-exempt devices are excluded; which Sub-GHz bands (315, 433, 868, 915 MHz) are exempt and at what power/duty cycle; whether Telecom Act ss.3, 32 and 60 are in force; ETA/MTCTE applicability and DGFT NOC; exposure of the maker/seller under IT Act ss.43, 66, 66C, 66D and BNS ss.318, 319, 336 for transmit/replay features; disclaimers, buyer verification and seller safe harbour; region-locking and custom firmware; customs specifics; CERT-In Directions for hardware vendors; written authorisation research customers should hold.
