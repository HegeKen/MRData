import common

roms = ["miui_VENUS_V14.0.23.8.15.DEV_3bb57a35f6_13.0.zip",
        "water_global_images_V14.0.14.0.TGOMIXM_20230728.0000.00_13.0_51d00b79c3.tgz",
        "miui-blockota-zircon-V14.0.1.0.TNOCNXM-V14.0.3.0.TNOCNXM-45749d772b-13.0.zip"]

for file in roms:
  common.checkExit(file)
