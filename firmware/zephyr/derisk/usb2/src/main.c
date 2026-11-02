/*
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * De-risk build 2 for "Flip my flipper": bring up TWO independent USB device
 * contexts in one Zephyr image. usbd_fs sits on the OTG FS controller (the
 * USB-C console port), usbd_hs on the OTG HS controller running in full-speed
 * mode on its embedded PHY (PB14/PB15, reserved for the Linux link).
 * Build-level proof only: nothing here has run on hardware.
 */
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/usb/usbd.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(usb2_derisk, LOG_LEVEL_INF);

#define VID 0x2fe3 /* Zephyr test VID, for samples only */

USBD_DEVICE_DEFINE(usbd_fs, DEVICE_DT_GET(DT_NODELABEL(usbotg_fs)), VID, 0x0001);
USBD_DEVICE_DEFINE(usbd_hs, DEVICE_DT_GET(DT_NODELABEL(usbotg_hs)), VID, 0x0002);

/* A descriptor node can only be linked into one context, so each context gets its own set */
USBD_DESC_LANG_DEFINE(lang_fs);
USBD_DESC_MANUFACTURER_DEFINE(mfr_fs, "Synnefo");
USBD_DESC_PRODUCT_DEFINE(prod_fs, "Synnefo console (OTG FS)");
USBD_DESC_CONFIG_DEFINE(cfgdesc_fs, "FS config");
USBD_CONFIGURATION_DEFINE(config_fs, 0, 100, &cfgdesc_fs);

USBD_DESC_LANG_DEFINE(lang_hs);
USBD_DESC_MANUFACTURER_DEFINE(mfr_hs, "Synnefo");
USBD_DESC_PRODUCT_DEFINE(prod_hs, "Synnefo link (OTG HS, FS mode)");
USBD_DESC_CONFIG_DEFINE(cfgdesc_hs, "HS-port config");
USBD_CONFIGURATION_DEFINE(config_hs, 0, 100, &cfgdesc_hs);

static int bring_up(struct usbd_context *ctx, struct usbd_desc_node *lang,
		    struct usbd_desc_node *mfr, struct usbd_desc_node *prod,
		    struct usbd_config_node *cfg, const char *class_name)
{
	int err;

	err = usbd_add_descriptor(ctx, lang);
	if (err) {
		return err;
	}
	err = usbd_add_descriptor(ctx, mfr);
	if (err) {
		return err;
	}
	err = usbd_add_descriptor(ctx, prod);
	if (err) {
		return err;
	}
	err = usbd_add_configuration(ctx, USBD_SPEED_FS, cfg);
	if (err) {
		return err;
	}
	err = usbd_register_class(ctx, class_name, USBD_SPEED_FS, 1);
	if (err) {
		return err;
	}
	usbd_device_set_code_triple(ctx, USBD_SPEED_FS, USB_BCC_MISCELLANEOUS, 0x02, 0x01);
	err = usbd_init(ctx);
	if (err) {
		return err;
	}
	return usbd_enable(ctx);
}

int main(void)
{
	int err;

	err = bring_up(&usbd_fs, &lang_fs, &mfr_fs, &prod_fs, &config_fs, "cdc_acm_0");
	LOG_INF("OTG FS context: %d", err);

	err = bring_up(&usbd_hs, &lang_hs, &mfr_hs, &prod_hs, &config_hs, "cdc_acm_1");
	LOG_INF("OTG HS (FS mode) context: %d", err);

	return 0;
}
