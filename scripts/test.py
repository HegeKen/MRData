import common
roms = ["flame_images_OS1.0.14.0.UGUCNXM_20250126.0000.00_14.0_cn_a63c78f373.tgz",
        "peridot_ep_stdee_images_OS1.0.25.1.7.EP.STDEE.N16T_20250107.0000.00_14.0_cn_chinatelecom_c59ea87dcc.tgz",
        "miui_FLAMEEPSTDEE_OS1.0.24.12.27.EP.STDEE.C3F_97af60a416_14.0.zip",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_2c120a3ae0.tgz",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_chinatelecom_5c2774437c.tgz",
        "miui_PERIDOTEPSTDEE_OS1.0.25.1.7.EP.STDEE.N16T_27f6fa83e1_14.0.zip",
        "miui_RUANEPSTDEE_OS1.0.24.12.11.EP.STDEE.N83U_8d87caae84_14.0.zip",
        "ruan_ep_stdee_images_OS1.0.24.12.11.EP.STDEE.N83U_20241210.0000.00_14.0_cn_98a096b3fd.tgz",
        "ruan_ep_stdee_images_OS1.0.24.12.11.EP.STDEE.N83U_20241210.0000.00_14.0_cn_chinatelecom_4c17ebb3c6.tgz"]

for rom in roms:
  device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = common.getData(rom)
  common.checkDatabase(device, code, android, version, type, bigver, region,tag,zone,branch, filetype, filename)
  common.add_rom_to_json(device, code, android, version, filetype, filename, devdata=None)
  common.checkExist(rom)