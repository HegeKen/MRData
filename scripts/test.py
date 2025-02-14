import common
roms = ["peridot_ep_stdee_images_OS1.0.25.1.7.EP.STDEE.N16T_20250107.0000.00_14.0_cn_3ef3aecc31.tgz",
        "peridot_ep_stdee_images_OS1.0.25.1.7.EP.STDEE.N16T_20250107.0000.00_14.0_cn_chinatelecom_c59ea87dcc.tgz",
        "miui_FLAMEEPSTDEE_OS1.0.24.12.27.EP.STDEE.C3F_97af60a416_14.0.zip",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_2c120a3ae0.tgz",
        "flame_ep_stdee_images_OS1.0.24.12.27.EP.STDEE.C3F_20241227.0000.00_14.0_cn_chinatelecom_5c2774437c.tgz",
        "miui_PERIDOTEPSTDEE_OS1.0.25.1.7.EP.STDEE.N16T_27f6fa83e1_14.0.zip"]


def getData(filename):
  if "miui" in filename:
    android = filename.split("_")[4].split(".zip")[0]
    version = filename.split("_")[2]
    get_sql = "SELECT code FROM devices WHERE branchcode = %s" % (common.stringify(filename.split("_")[1]))
    if len(common.db_job(get_sql)) > 0:
      code = common.db_job(get_sql)[0][0]
    else:
      code = 0
  else:
    if filename.endswith(".tgz"):
      android = filename.split("images_")[1].split("_")[2]
      version = filename.split("images_")[1].split("_")[0]
      code = filename.split('_images')[0]
    else:
      android = filename.split("ota_full-")[1].split("-")[2]
      version = filename.split("ota_full-")[1].split("-")[0]
      code = filename.split("-ota_full")[0]
  return code, android, version
for rom in roms:
  print(getData(rom))