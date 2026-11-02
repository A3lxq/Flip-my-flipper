/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * De-risk build 3 for "Flip my flipper": three modules with different SPI modes on one
 * bus, each with its own struct spi_config built from the devicetree:
 *   PN532     mode 0, LSB first, 1 MHz   (IRQ active low)
 *   CC1101    mode 0, MSB first, 6.5 MHz (burst limit without inter-byte delay)
 *   ST25R3916 mode 1, MSB first, 5 MHz   (IRQ active high)
 * The BUILD_ASSERTs fail the build if the devicetree does not yield the intended flags.
 * Build-level proof only: nothing here has run on hardware.
 */
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(spi3_derisk, LOG_LEVEL_INF);

#define OPS (SPI_WORD_SET(8) | SPI_OP_MODE_CONTROLLER)

#define PN532_N     DT_NODELABEL(mod_pn532)
#define CC1101_N    DT_NODELABEL(mod_cc1101)
#define ST25R_N     DT_NODELABEL(mod_st25r3916)

/* One struct spi_config per device: the STM32 driver reprograms CPOL/CPHA/bit order/prescaler
 * whenever the config POINTER differs from the last one used (spi_context_configured()).
 * Changing a shared struct in place would be missed, so never do that. */
static const struct spi_dt_spec pn532 = SPI_DT_SPEC_GET(PN532_N, OPS);
static const struct spi_dt_spec cc1101 = SPI_DT_SPEC_GET(CC1101_N, OPS);
static const struct spi_dt_spec st25r = SPI_DT_SPEC_GET(ST25R_N, OPS);

static const struct gpio_dt_spec irq_pn532 = GPIO_DT_SPEC_GET(PN532_N, irq_gpios);
static const struct gpio_dt_spec irq_cc1101 = GPIO_DT_SPEC_GET(CC1101_N, irq_gpios);
static const struct gpio_dt_spec irq_st25r = GPIO_DT_SPEC_GET(ST25R_N, irq_gpios);

/* All three are on the same bus controller */
BUILD_ASSERT(DT_SAME_NODE(DT_BUS(PN532_N), DT_BUS(CC1101_N)));
BUILD_ASSERT(DT_SAME_NODE(DT_BUS(PN532_N), DT_BUS(ST25R_N)));

/* Compile-time checks on what the devicetree says (SPI_CONFIG_DT is an initializer and cannot be
 * used inside an expression, so the properties are read directly) */
/* PN532: mode 0 (no CPOL, no CPHA), LSB first, 1 MHz */
BUILD_ASSERT(!DT_PROP(PN532_N, spi_cpol) && !DT_PROP(PN532_N, spi_cpha));
BUILD_ASSERT(DT_PROP(PN532_N, spi_lsb_first));
BUILD_ASSERT(DT_PROP(PN532_N, spi_max_frequency) == 1000000);

/* CC1101: mode 0, MSB first, 6.5 MHz */
BUILD_ASSERT(!DT_PROP(CC1101_N, spi_cpol) && !DT_PROP(CC1101_N, spi_cpha));
BUILD_ASSERT(!DT_PROP(CC1101_N, spi_lsb_first));
BUILD_ASSERT(DT_PROP(CC1101_N, spi_max_frequency) == 6500000);

/* ST25R3916: CPOL 0, CPHA 1 (mode 1), MSB first, 5 MHz */
BUILD_ASSERT(!DT_PROP(ST25R_N, spi_cpol) && DT_PROP(ST25R_N, spi_cpha));
BUILD_ASSERT(!DT_PROP(ST25R_N, spi_lsb_first));
BUILD_ASSERT(DT_PROP(ST25R_N, spi_max_frequency) == 5000000);

/* IRQ polarity comes from the gpio flags in the devicetree */
BUILD_ASSERT((DT_GPIO_FLAGS(PN532_N, irq_gpios) & GPIO_ACTIVE_LOW) != 0);
BUILD_ASSERT((DT_GPIO_FLAGS(ST25R_N, irq_gpios) & GPIO_ACTIVE_LOW) == 0);

/* A transaction on one module, serialised by the caller (the SPI arbiter in the real firmware) */
static int xfer(const struct spi_dt_spec *dev, uint8_t *tx, uint8_t *rx, size_t len)
{
	const struct spi_buf txb = { .buf = tx, .len = len };
	const struct spi_buf rxb = { .buf = rx, .len = len };
	const struct spi_buf_set txs = { .buffers = &txb, .count = 1 };
	const struct spi_buf_set rxs = { .buffers = &rxb, .count = 1 };

	return spi_transceive_dt(dev, &txs, &rxs);
}

int main(void)
{
	uint8_t tx[4] = { 0 }, rx[4];

	if (!spi_is_ready_dt(&pn532) || !spi_is_ready_dt(&cc1101) || !spi_is_ready_dt(&st25r)) {
		LOG_ERR("SPI bus not ready");
		return 0;
	}
	ARG_UNUSED(irq_pn532);
	ARG_UNUSED(irq_cc1101);
	ARG_UNUSED(irq_st25r);

	/* The flags the SPI driver will actually receive for each device */
	LOG_INF("pn532 op=0x%04x f=%u | cc1101 op=0x%04x f=%u | st25r op=0x%04x f=%u",
		pn532.config.operation, pn532.config.frequency,
		cc1101.config.operation, cc1101.config.frequency,
		st25r.config.operation, st25r.config.frequency);
	__ASSERT(pn532.config.operation & SPI_TRANSFER_LSB, "PN532 must be LSB first");
	__ASSERT(!(cc1101.config.operation & SPI_TRANSFER_LSB), "CC1101 must be MSB first");
	__ASSERT(st25r.config.operation & SPI_MODE_CPHA, "ST25R3916 must be mode 1");

	/* Interleaved use of the shared bus: each call reconfigures the controller as needed */
	for (int i = 0; i < 3; i++) {
		LOG_INF("pn532 %d", xfer(&pn532, tx, rx, sizeof(tx)));
		LOG_INF("cc1101 %d", xfer(&cc1101, tx, rx, sizeof(tx)));
		LOG_INF("st25r3916 %d", xfer(&st25r, tx, rx, sizeof(tx)));
	}
	return 0;
}
