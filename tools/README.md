# tools

Scripts used to build and check the pin maps. They need Python 3 (standard library only).

Regenerating the pin dumps (not included, third-party data):

1. Clone STMicroelectronics' open pin data: `git clone --depth 1 https://github.com/STMicroelectronics/STM32_open_pin_data.git` (BSD-3-Clause).
2. Dump the pins: `python3 -I dumppins.py <clone>/mcu/STM32H743IITx.xml > pins_H743IITx.txt` and the same for `STM32F429ZITx.xml` -> `pins_F429ZITx.txt`.
3. Solve: `python3 -I pinmap.py pins_H743IITx.txt H743 12 out_H743.md` (and `F429`).
4. Check: `python3 -I verify.py pins_H743IITx.txt out_H743.md`.
5. Generate firmware headers and the connector table: `python3 -I genboard.py <repo root>`.

`summ.py` prints a peripheral summary per part from the same XML files.
