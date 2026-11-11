# Flip my flipper

> **Status: UNDER DEVELOPMENT.** This is an early-stage design project. Nothing here is built, tested, certified or ready to use. Documents are drafts and will change.

A modular, portable electronics and authorised security-research handheld, designed in India to be built from parts sold by Indian sellers. The working project name is **Synnefo Handheld**. It aims to offer Flipper-Zero-style capabilities (Sub-GHz, NFC/RFID, infrared, GPIO, Wi-Fi/BLE, USB) on an independent platform with its own firmware and an open module interface standard (SMIS), with a future Linux compute module.

This project is not affiliated with, endorsed by or connected to Flipper Devices Inc. "Flipper" and "Flipper Zero" belong to their owners.

## What is here

| File | Contents |
|---|---|
| `HANDOFF.md` | **Start here when picking the project up**: status, decisions, what was verified, gaps, how to resume, next steps |
| `01-requirements-and-architecture.md` | Requirements traceability matrix, decisions (CONFIRMED / PROPOSED / OPEN), risks |
| `02-pin-maps.md` | Pin maps for STM32H743IIT6 and STM32F429ZIT6 |
| `03-core-module.md` | Swappable MCU core-module architecture and connector table |
| `04-india-sourcing.md`, `05-deep-sourcing-and-compatibility.md` | Indian sourcing and compatibility checks (snapshots, unverified stock) |
| `06-nfc-modules.md` | Two NFC modules: PN532 and ST25R3916 |
| `07-india-regulatory.md` | Indian regulatory research (not legal advice) |
| `08-smis-v0.2.md` | Synnefo Module Interface Standard v0.2 |
| `09-power-architecture.md` | Power architecture v1 |
| `10-firmware-architecture.md` | Firmware architecture v0.1 and RTOS decision record |
| `11-os-options-and-linux-architecture.md` | Other OS options and the Linux-first (Flipper One-style) question |
| `hardware/pinouts/` | Module pinout tables (with how well each pinout is known) and the connection diagrams (system and SM-S port) |
| `hardware/kicad/` | KiCad skeletons for the PN532 adapter and the ST25R3916 module, with ERC/DRC outputs |
| `firmware/board/` | Generated pin headers for both MCUs |
| `firmware/zephyr/` | Zephyr 4.5.0 toolchain setup and the three build-level de-risk test apps with results |
| `sourcing/quote-requests.md` | Drafts of quote and stock-confirmation requests to Indian sellers (not sent) |
| `research/` | Condensed research-agent reports behind the documents (limits listed in its README) |
| `CONTRIBUTING.md` | How to contribute and what the licence requires |
| `CHAT_SUMMARY.md` | Project log: decisions, findings, corrections, open items |
| `tools/` | Scripts that solve and check the pin maps |

## Ground rules

- **Lawful use only.** The device is meant for authorised testing, electronics development and education. It must not include jamming or blocking functions, and transmit features are designed to stay inside licence-exempt bands and power limits.
- **Not legal advice.** The regulatory notes list what sources say, with their gaps. They have not been reviewed by a lawyer or a test lab. Check the rules in your country before building or selling anything.
- **Stock, prices and datasheet figures are snapshots** found during research and may be wrong or out of date. Verify against the manufacturer's current datasheet and the seller before relying on anything.
- **Safety:** this design involves lithium cells and RF circuits. Do not build it without the knowledge and equipment to do so safely.

## License

GNU General Public License v3.0 or later, the same family of licence used by the Flipper Zero firmware. See [LICENSE](LICENSE), [NOTICE](NOTICE) and [CONTRIBUTING.md](CONTRIBUTING.md).

In short: anyone may use the source and build from it; if they distribute a modified version, they must publish their source under the GPL too. We ask that improvements be contributed back through pull requests, but the licence itself cannot require that.

Earlier commits (the first two) were published under Apache-2.0; anyone who copied that version keeps those rights for that version.
