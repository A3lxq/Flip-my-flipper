# Zephyr de-risk builds

Status: build-level results only. **Nothing here has run on hardware.** The three test applications check the open risks listed in `10-firmware-architecture.md` §14. Results are in `derisk/RESULTS.md`.

## Toolchain and workspace used (2026-11-02, Linux x86_64)

| Item | Version / source |
|---|---|
| Zephyr | v4.5.0, commit `41d10b59730406bbab4ca9f1fbbe9e96aafb4966` (shallow clone of github.com/zephyrproject-rtos/zephyr) |
| Modules fetched | `cmsis` 512cc7e, `cmsis_6` 1c1840a, `hal_stm32` c955019, `lvgl` c9ffd46 (library.json says 9.6.0) via `west config manifest.project-filter -- "-.*,+cmsis,+cmsis_6,+hal_stm32,+lvgl"` and `west update -n -o=--depth=1` |
| Zephyr SDK | 1.0.1 (the version in `zephyr/SDK_VERSION`), installed with `west sdk install --version 1.0.1 -d ~/zephyr-work/zephyr-sdk -t arm-zephyr-eabi` |
| Compiler | `arm-zephyr-eabi-gcc` 14.3.0 (Zephyr SDK 1.0.1); host tools (`dtc` 1.7.0) from the SDK |
| west / CMake / Ninja | west 1.5.0, CMake 4.4.4, Ninja 1.13.2 (installed with pip/uv) |
| Python | 3.12.14 in a uv virtual environment (system Python is 3.14, not used) |
| Disk | Zephyr tree 0.7 GB, modules 1.6 GB, SDK 2.0 GB, builds ~0.4 GB |

Downloads were fetched from GitHub releases by `west sdk install`. The tool's source (`scripts/west_commands/sdk.py`) fetches the release's `sha256.sum` and checks archives against it; the log of this run kept only its last lines, so the check itself is not shown here.
Only the ARM toolchain was installed. Without `-t`, `west sdk install` downloads every architecture (several GB).

## Reproduce

```bash
# once
uv venv --python 3.12 ~/zephyr-work/venv && . ~/zephyr-work/venv/bin/activate
uv pip install west cmake ninja && git clone --depth 1 --branch v4.5.0 https://github.com/zephyrproject-rtos/zephyr.git ~/zephyr-work/ws/zephyr
cd ~/zephyr-work/ws && west init -l zephyr
west config manifest.project-filter -- "-.*,+cmsis,+cmsis_6,+hal_stm32,+lvgl" && west update -n -o=--depth=1
uv pip install -r zephyr/scripts/requirements-base.txt
west sdk install --version 1.0.1 -d ~/zephyr-work/zephyr-sdk -t arm-zephyr-eabi

# every session: copy env.sh.example to ~/zephyr-work/env.sh and source it
D=<repo>/firmware/zephyr/derisk
west build -p always -b nucleo_f429zi zephyr/samples/subsys/display/lvgl -d build/lvgl_f429 -- \
    -DEXTRA_DTC_OVERLAY_FILE=$D/lvgl/lvgl_f429.overlay -DEXTRA_CONF_FILE=$D/lvgl/lvgl.conf
west build -p always -b nucleo_h743zi $D/usb2 -d build/usb2_h743
west build -p always -b nucleo_f429zi $D/spi3 -d build/spi3_f429
```

## Caveats

- **Paths with spaces break the builds.** Zephyr's devicetree preprocessing fails on an overlay path containing a space (error: `fatal error: ...Hand: No such file or directory`). The repository folder name has a space, so copy `firmware/zephyr/derisk` to a space-free folder (for example `~/zephyr-work/derisk`) before building; the results below were produced that way.
- The boards used are Nucleo-144 development boards, not our hardware. The overlays use pins from `02-pin-maps.md` where the 144-pin package has them; the 176-pin H743 map uses pins that package lacks (for example PI2), so SPI2 on the H743 test uses the Nucleo's pins.
- The ST7796S gamma tables in `derisk/lvgl/*.overlay` are **placeholders copied from Zephyr's reference shield**; they must be replaced with the real panel's values.
- The H743 OTG-HS node in `derisk/usb2/boards/nucleo_h743zi.overlay` was modelled on the H723 definition and its address, interrupt numbers and clock bit were checked against ST's `stm32h743xx.h`; they have not been tested on silicon.
