# Synnefo Handheld: MCU pin maps (draft 2)

Draft 2 (2026-11-01) adds 8 per-port ID clock lines (IDC_P1..8) and renames the ID data lines IDD_P1..8, for the two-wire module ID in SMIS v0.2 (see 08-smis-v0.2.md). Both maps re-solved and re-verified: 97 pins assigned, EXTI lines still unique.

Status: PROPOSED. Not validated on hardware, not yet checked against the datasheet PDFs.

Two maps with the same logical signals: **STM32H743IIT6 (LQFP176)**, the preferred part (Indian sourcing unconfirmed), and **STM32F429ZIT6 (LQFP144)**, the fallback that Indian sellers list.

## How these were made

- Signal data comes from ST's `STM32_open_pin_data` repository (commit 7d1f151, 2026-06-29), files `STM32H743IITx.xml` and `STM32F429ZITx.xml`.
- `tools/pinmap.py` searches for an assignment; `tools/verify.py` independently re-checks the result. Both maps passed: every peripheral signal exists on its pin, no pin is used twice, and the 14 interrupt lines (EXTI) all have different pin numbers (each EXTI line number can serve only one pin).
- **Not in this data, so not checked:** alternate-function (AF) numbers, 5 V tolerance and drive strength per pin, DMA stream conflicts, maximum SPI speed per pin, and clock-tree limits. Take these from the datasheet and CubeMX before layout.

## Assumptions behind the signal list

- Buttons (8) and port fault inputs sit on I²C port expander B, with one interrupt line INT_B (the only way to wake from sleep by button). Port power-enable and reset lines sit on expander A (output only). Neither expander appears below because they are I²C devices.
- Per port: one ID line and one interrupt, direct to the MCU. Five SM-S (SPI) ports each have a dedicated chip-select; SM-I and SM-U ports share the I²C_EXP and UART_EXP buses.
- The GPIO header carries the shared SPI/I²C/UART buses (no extra MCU pins), 4 ADC inputs and 12 plain GPIO. Both MCUs also fit more GPIO: the H743 map has room for at least 36 and the F429 map for about 24 to 30 (tested).
- Display on SPI with a separate chip-select, command/data, reset and PWM backlight line. SD card on 4-bit SDMMC/SDIO plus card-detect.
- The Linux link has a UART, a USB port (the second USB controller, full-speed through its internal PHY on PB14/PB15, to be confirmed in the datasheet), enable, reset, presence and wake lines.
- PWM and timer capture use different timers for IR transmit, IR receive, buzzer and backlight.
- Pins avoided on purpose: SWD, SWO, both crystals, PC13 (weak drive), the analog-switch pads, and (F429) PB2 which is the BOOT1 strap.
- The 8 EXTI users: 8 port interrupts, INT_B, power interrupt, ESP32 handshake, SD card detect, Linux wake, Linux presence. Only 16 EXTI lines exist per chip, so this budget is nearly full.

## STM32H743IIT6 (LQFP176): 140 I/O pins, 97 assigned, 7 reserved, 36 spare

Instance choices: DISP_SPI=SPI1, EXP_SPI=SPI2, I2C_EXP=I2C2, I2C_SYS=I2C1, LINUX_USB=USB_OTG_HS, SD=SDMMC1, UART_CON=USART2, UART_ESP=USART1, UART_EXP=USART3, UART_LINUX=UART4, USB_FS=USB_OTG_FS

| Pkg pin | Port | Function | Signal |
|---|---|---|---|
| 2 | PE3 | ESP_EN | GPIO |
| 4 | PE5 | IR_TX | TIM15_CH1 |
| 7 | PI8 | ESP_HS | GPIO |
| 9 | PC14 | RESERVED | LSE crystal |
| 10 | PC15 | RESERVED | LSE crystal |
| 11 | PI9 | UART_LINUX_RX | UART4_RX |
| 12 | PI10 | IRQ_P1 | GPIO |
| 13 | PI11 | IDC_P8 | GPIO |
| 16 | PF0 | I2C_EXP_SDA | I2C2_SDA |
| 17 | PF1 | I2C_EXP_SCL | I2C2_SCL |
| 18 | PF2 | PWR_INT | GPIO |
| 19 | PF3 | ADC_H1 | ADC3_INP5 |
| 20 | PF4 | ADC_H2 | ADC3_INP9 |
| 21 | PF5 | ADC_H3 | ADC3_INP4 |
| 24 | PF6 | ADC_H4 | ADC3_INP8 |
| 25 | PF7 | IR_RX | TIM17_CH1 |
| 26 | PF8 | BUZZER | TIM13_CH1 |
| 27 | PF9 | DISP_BL | TIM14_CH1 |
| 28 | PF10 | GPIO_H8 | GPIO |
| 29 | PH0 | RESERVED | HSE crystal |
| 30 | PH1 | RESERVED | HSE crystal |
| 33 | PC1 | EXP_SPI_MOSI | SPI2_MOSI |
| 40 | PA0 | UART_LINUX_TX | UART4_TX |
| 42 | PA2 | UART_CON_TX | USART2_TX |
| 43 | PH2 | CS_P4 | GPIO |
| 44 | PH3 | CS_P5 | GPIO |
| 45 | PH4 | IDC_P4 | GPIO |
| 46 | PH5 | LED_G | GPIO |
| 47 | PA3 | UART_CON_RX | USART2_RX |
| 51 | PA5 | DISP_SPI_SCK | SPI1_SCK |
| 52 | PA6 | DISP_SPI_MISO | SPI1_MISO |
| 53 | PA7 | DISP_SPI_MOSI | SPI1_MOSI |
| 59 | PF11 | GPIO_H9 | GPIO |
| 60 | PF12 | LINUX_WAKE | GPIO |
| 63 | PF13 | IRQ_P2 | GPIO |
| 64 | PF14 | ESP_BOOT | GPIO |
| 65 | PF15 | IRQ_P6 | GPIO |
| 66 | PG0 | INT_B | GPIO |
| 67 | PG1 | LINUX_PRSNT | GPIO |
| 68 | PE7 | GPIO_H7 | GPIO |
| 73 | PE10 | CS_P1 | GPIO |
| 75 | PE12 | GPIO_H5 | GPIO |
| 76 | PE13 | GPIO_H6 | GPIO |
| 77 | PE14 | IDD_P8 | GPIO |
| 79 | PB10 | UART_EXP_TX | USART3_TX |
| 80 | PB11 | UART_EXP_RX | USART3_RX |
| 83 | PH6 | IDC_P5 | GPIO |
| 84 | PH7 | IRQ_P7 | GPIO |
| 85 | PH8 | LED_B | GPIO |
| 86 | PH9 | IDC_P6 | GPIO |
| 87 | PH10 | LINUX_RST | GPIO |
| 89 | PH12 | VIBRATION | GPIO |
| 93 | PB13 | EXP_SPI_SCK | SPI2_SCK |
| 94 | PB14 | LINUX_USB_DM | USB_OTG_HS_DM |
| 95 | PB15 | LINUX_USB_DP | USB_OTG_HS_DP |
| 96 | PD8 | IDD_P6 | GPIO |
| 97 | PD9 | IDD_P7 | GPIO |
| 98 | PD10 | IDD_P4 | GPIO |
| 101 | PD13 | IDD_P5 | GPIO |
| 104 | PD14 | IRQ_P4 | GPIO |
| 106 | PG2 | DISP_DC | GPIO |
| 107 | PG3 | IRQ_P3 | GPIO |
| 108 | PG4 | LINUX_EN | GPIO |
| 109 | PG5 | DISP_CS | GPIO |
| 110 | PG6 | IDC_P1 | GPIO |
| 111 | PG7 | IDC_P2 | GPIO |
| 112 | PG8 | GPIO_H12 | GPIO |
| 117 | PC8 | SD_D0 | SDMMC1_D0 |
| 118 | PC9 | SD_D1 | SDMMC1_D1 |
| 120 | PA9 | USB_VBUS | USB_OTG_FS_VBUS |
| 121 | PA10 | UART_ESP_RX | USART1_RX |
| 122 | PA11 | USB_FS_DM | USB_OTG_FS_DM |
| 123 | PA12 | USB_FS_DP | USB_OTG_FS_DP |
| 124 | PA13 | RESERVED | SWD |
| 128 | PH13 | LED_R | GPIO |
| 129 | PH14 | IDC_P3 | GPIO |
| 130 | PH15 | CS_P3 | GPIO |
| 131 | PI0 | IDC_P7 | GPIO |
| 133 | PI2 | EXP_SPI_MISO | SPI2_MISO |
| 134 | PI3 | BOOST_EN | GPIO |
| 137 | PA14 | RESERVED | SWD |
| 139 | PC10 | SD_D2 | SDMMC1_D2 |
| 140 | PC11 | SD_D3 | SDMMC1_D3 |
| 141 | PC12 | SD_CK | SDMMC1_CK |
| 142 | PD0 | IDD_P2 | GPIO |
| 143 | PD1 | IDD_P3 | GPIO |
| 144 | PD2 | SD_CMD | SDMMC1_CMD |
| 145 | PD3 | GPIO_H2 | GPIO |
| 146 | PD4 | IRQ_P5 | GPIO |
| 147 | PD5 | SD_CD | GPIO |
| 151 | PD7 | GPIO_H3 | GPIO |
| 153 | PG10 | GPIO_H10 | GPIO |
| 157 | PG14 | GPIO_H11 | GPIO |
| 160 | PG15 | CS_P2 | GPIO |
| 161 | PB3 | RESERVED | SWO (JTDO), kept free for trace |
| 164 | PB6 | UART_ESP_TX | USART1_TX |
| 165 | PB7 | I2C_SYS_SDA | I2C1_SDA |
| 167 | PB8 | I2C_SYS_SCL | I2C1_SCL |
| 169 | PE0 | GPIO_H4 | GPIO |
| 170 | PE1 | DISP_RST | GPIO |
| 173 | PI4 | GPIO_H1 | GPIO |
| 174 | PI5 | PWR_PG | GPIO |
| 175 | PI6 | IRQ_P8 | GPIO |
| 176 | PI7 | IDD_P1 | GPIO |

Spare I/O: PE2 (1), PE4 (3), PE6 (5), PC13 (8), PC0 (32), PC2_C (34), PC3_C (35), PA1 (41), PA4 (50), PC4 (54), PC5 (55), PB0 (56), PB1 (57), PB2 (58), PE8 (69), PE9 (70), PE11 (74), PE15 (78), PH11 (88), PB12 (92), PD11 (99), PD12 (100), PD15 (105), PC6 (115), PC7 (116), PA8 (119), PI1 (132), PA15 (138), PD6 (150), PG9 (152), PG11 (154), PG12 (155), PG13 (156), PB4 (162), PB5 (163), PB9 (168)

Deliberately avoided: PC13 (RTC/tamper pin, weak drive), PC2_C (analog-switch pad, kept free), PC3_C (analog-switch pad, kept free)

## STM32F429ZIT6 (LQFP144): 114 I/O pins, 97 assigned, 7 reserved, 10 spare

Instance choices: DISP_SPI=SPI1, EXP_SPI=SPI2, I2C_EXP=I2C2, I2C_SYS=I2C1, LINUX_USB=USB_OTG_HS, SD=SDIO, UART_CON=USART2, UART_ESP=USART1, UART_EXP=USART3, UART_LINUX=UART4, USB_FS=USB_OTG_FS

| Pkg pin | Port | Function | Signal |
|---|---|---|---|
| 1 | PE2 | CS_P1 | GPIO |
| 2 | PE3 | LED_B | GPIO |
| 3 | PE4 | GPIO_H4 | GPIO |
| 4 | PE5 | IR_TX | TIM9_CH1 |
| 5 | PE6 | GPIO_H11 | GPIO |
| 8 | PC14 | RESERVED | LSE crystal |
| 9 | PC15 | RESERVED | LSE crystal |
| 10 | PF0 | I2C_EXP_SDA | I2C2_SDA |
| 11 | PF1 | I2C_EXP_SCL | I2C2_SCL |
| 12 | PF2 | DISP_DC | GPIO |
| 13 | PF3 | ADC_H1 | ADC3_IN9 |
| 14 | PF4 | ADC_H2 | ADC3_IN14 |
| 15 | PF5 | ADC_H3 | ADC3_IN15 |
| 18 | PF6 | ADC_H4 | ADC3_IN4 |
| 19 | PF7 | IR_RX | TIM11_CH1 |
| 20 | PF8 | BUZZER | TIM13_CH1 |
| 21 | PF9 | DISP_BL | TIM14_CH1 |
| 22 | PF10 | IDD_P6 | GPIO |
| 23 | PH0 | RESERVED | HSE crystal |
| 24 | PH1 | RESERVED | HSE crystal |
| 26 | PC0 | IDC_P5 | GPIO |
| 27 | PC1 | BOOST_EN | GPIO |
| 28 | PC2 | EXP_SPI_MISO | SPI2_MISO |
| 29 | PC3 | EXP_SPI_MOSI | SPI2_MOSI |
| 34 | PA0 | UART_LINUX_TX | UART4_TX |
| 35 | PA1 | UART_LINUX_RX | UART4_RX |
| 36 | PA2 | UART_CON_TX | USART2_TX |
| 37 | PA3 | UART_CON_RX | USART2_RX |
| 41 | PA5 | DISP_SPI_SCK | SPI1_SCK |
| 42 | PA6 | DISP_SPI_MISO | SPI1_MISO |
| 43 | PA7 | DISP_SPI_MOSI | SPI1_MOSI |
| 44 | PC4 | ESP_BOOT | GPIO |
| 45 | PC5 | LINUX_EN | GPIO |
| 49 | PF11 | GPIO_H5 | GPIO |
| 50 | PF12 | INT_B | GPIO |
| 53 | PF13 | PWR_INT | GPIO |
| 54 | PF14 | ESP_HS | GPIO |
| 55 | PF15 | IDD_P7 | GPIO |
| 56 | PG0 | SD_CD | GPIO |
| 57 | PG1 | LINUX_WAKE | GPIO |
| 58 | PE7 | IDD_P3 | GPIO |
| 59 | PE8 | IDD_P4 | GPIO |
| 60 | PE9 | IDD_P5 | GPIO |
| 63 | PE10 | IRQ_P6 | GPIO |
| 65 | PE12 | IDC_P6 | GPIO |
| 66 | PE13 | IDC_P7 | GPIO |
| 67 | PE14 | IDC_P8 | GPIO |
| 68 | PE15 | GPIO_H10 | GPIO |
| 69 | PB10 | UART_EXP_TX | USART3_TX |
| 70 | PB11 | UART_EXP_RX | USART3_RX |
| 74 | PB13 | EXP_SPI_SCK | SPI2_SCK |
| 75 | PB14 | LINUX_USB_DM | USB_OTG_HS_DM |
| 76 | PB15 | LINUX_USB_DP | USB_OTG_HS_DP |
| 77 | PD8 | IRQ_P5 | GPIO |
| 78 | PD9 | IRQ_P8 | GPIO |
| 79 | PD10 | PWR_PG | GPIO |
| 80 | PD11 | GPIO_H1 | GPIO |
| 81 | PD12 | IDD_P1 | GPIO |
| 82 | PD13 | DISP_CS | GPIO |
| 85 | PD14 | LED_R | GPIO |
| 86 | PD15 | GPIO_H2 | GPIO |
| 87 | PG2 | LINUX_PRSNT | GPIO |
| 88 | PG3 | IRQ_P1 | GPIO |
| 89 | PG4 | DISP_RST | GPIO |
| 90 | PG5 | ESP_EN | GPIO |
| 91 | PG6 | IRQ_P7 | GPIO |
| 92 | PG7 | IDC_P2 | GPIO |
| 93 | PG8 | IDC_P3 | GPIO |
| 96 | PC6 | GPIO_H7 | GPIO |
| 97 | PC7 | GPIO_H8 | GPIO |
| 98 | PC8 | SD_D0 | SDIO_D0 |
| 99 | PC9 | SD_D1 | SDIO_D1 |
| 100 | PA8 | CS_P5 | GPIO |
| 101 | PA9 | USB_VBUS | USB_OTG_FS_VBUS |
| 102 | PA10 | UART_ESP_RX | USART1_RX |
| 103 | PA11 | USB_FS_DM | USB_OTG_FS_DM |
| 104 | PA12 | USB_FS_DP | USB_OTG_FS_DP |
| 105 | PA13 | RESERVED | SWD |
| 109 | PA14 | RESERVED | SWD |
| 111 | PC10 | SD_D2 | SDIO_D2 |
| 112 | PC11 | SD_D3 | SDIO_D3 |
| 113 | PC12 | SD_CK | SDIO_CK |
| 114 | PD0 | LINUX_RST | GPIO |
| 115 | PD1 | VIBRATION | GPIO |
| 116 | PD2 | SD_CMD | SDIO_CMD |
| 117 | PD3 | GPIO_H3 | GPIO |
| 118 | PD4 | IRQ_P2 | GPIO |
| 119 | PD5 | IRQ_P3 | GPIO |
| 122 | PD6 | GPIO_H9 | GPIO |
| 123 | PD7 | IRQ_P4 | GPIO |
| 124 | PG9 | CS_P4 | GPIO |
| 125 | PG10 | CS_P2 | GPIO |
| 126 | PG11 | GPIO_H12 | GPIO |
| 127 | PG12 | CS_P3 | GPIO |
| 128 | PG13 | IDD_P8 | GPIO |
| 129 | PG14 | IDC_P1 | GPIO |
| 132 | PG15 | GPIO_H6 | GPIO |
| 133 | PB3 | RESERVED | SWO (JTDO), kept free for trace |
| 134 | PB4 | IDC_P4 | GPIO |
| 136 | PB6 | UART_ESP_TX | USART1_TX |
| 137 | PB7 | I2C_SYS_SDA | I2C1_SDA |
| 139 | PB8 | I2C_SYS_SCL | I2C1_SCL |
| 141 | PE0 | IDD_P2 | GPIO |
| 142 | PE1 | LED_G | GPIO |

Spare I/O: PC13 (7), PA4 (40), PB0 (46), PB1 (47), PB2 (48), PE11 (64), PB12 (73), PA15 (110), PB5 (135), PB9 (140)

Deliberately avoided: PC13 (RTC/tamper pin, weak drive), PB2 (BOOT1 strap)

## Comparison

| | H743IIT6 | F429ZIT6 |
|---|---|---|
| I/O pins | 140 | 114 |
| Assigned (baseline, 12 header GPIO) | 97 | 97 |
| Reserved | 7 | 7 |
| Spare | 36 | 10 |
| Instance choices | identical on both | identical on both |
| Max header GPIO that still fits | at least 36 (before the ID lines were added) | about 20 (tested to 20) |

The same instance choices work on both chips (SPI1 display, SPI2 expansion, I2C1/I2C2, USART1/2/3 + UART4, SD, USB FS, second USB for Linux). That keeps firmware drivers portable between the two chips even though the pin numbers differ.

## Open points

1. Check AF numbers, 5 V tolerance and DMA against the datasheets.
2. Verify the second USB port works as full-speed on PB14/PB15 for the Linux link.
3. Pin positions are for the LQFP packages only; both need a custom PCB and a 0.5 mm-pitch LQFP (hot air or drag soldering).
4. Sourcing for the H743 is unconfirmed (see section 10 of `01-requirements-and-architecture.md`).
