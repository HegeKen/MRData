import common
roms = ["vermeer-ota_full-OS2.0.102.0.VNKCNXM-user-15.0-2056f5ef49.zip",
        "peridot_ep_stdee_images_OS1.0.25.1.7.EP.STDEE.N16T_20250107.0000.00_14.0_cn_chinatelecom_c59ea87dcc.tgz",
        "miui_FLAMEEPSTDEE_OS1.0.24.12.27.EP.STDEE.C3F_97af60a416_14.0.zip",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_2c120a3ae0.tgz",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_chinatelecom_5c2774437c.tgz",
        "miui_PERIDOTEPSTDEE_OS1.0.25.1.7.EP.STDEE.N16T_27f6fa83e1_14.0.zip",
        "miui_RUANEPSTDEE_OS1.0.24.12.11.EP.STDEE.N83U_8d87caae84_14.0.zip",
        "ruan_ep_stdee_images_OS1.0.24.12.11.EP.STDEE.N83U_20241210.0000.00_14.0_cn_98a096b3fd.tgz",
        "ruan_ep_stdee_images_OS1.0.24.12.11.EP.STDEE.N83U_20241210.0000.00_14.0_cn_chinatelecom_4c17ebb3c6.tgz"]


def getData(filename):
  if "miui" in filename:
    android = filename.split("_")[4].split(".zip")[0]
    version = filename.split("_")[2]
    get_sql = "SELECT code FROM devices WHERE branchcode = %s" % (common.stringify(filename.split("_")[1]))
    if len(common.db_job(get_sql)) > 0:
      code = common.db_job(get_sql)[0][0]
      device = common.db_job("SELECT device FROM roms where code = %s" % (common.stringify(code)))[0][0]
    else:
      code = 0
      device = 0
  else:
    if filename.endswith(".tgz"):
      android = filename.split("images_")[1].split("_")[2]
      version = filename.split("images_")[1].split("_")[0]
      code = filename.split('_images')[0]
    else:
      android = filename.split("ota_full-")[1].split("-")[2]
      version = filename.split("ota_full-")[1].split("-")[0]
      code = filename.split("-ota_full")[0]
    device = common.db_job("SELECT device FROM roms where code = %s" % (common.stringify(code)))[0][0]
  if version.startswith('V'):
    type = "MIUI"
    bigver = "MIUI " + version.split('V')[1].split('.')[0]
  else:
    type = "HyperOS"
    bigver = "HyperOS " + version.split('OS')[1].split('.')[0]
  if code == 0:
    return 0
  else:
    if "CNXM" in version:
      if version.split(".")[3] == 0 or version.split(".")[3] == "0":
        tag = "CnOO"
      else:
        tag = "CnOB"
      region = "cn"
      zone = 1
    else:
      info_sql = "SELECT region,tag,zone FROM roms WHERE code = %s" % (common.stringify(code))
      region,tag,zone = common.db_job(info_sql)[0]
  return device, code, android, version, type, bigver, region,tag,zone, "F"
for rom in roms:
  print(getData(rom))
  # common.checkDatabase(rom)