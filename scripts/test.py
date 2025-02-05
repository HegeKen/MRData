import common
roms = ["miui_ROSEMARYPTWGlobal_V14.0.9.0.TFFTWXM_32f05fdce4_13.0.zip",
        "miui_BLUEIDGlobal_V816.0.8.0.UGRIDXM_f40076ddc4_14.0.zip",
        "miui_DITINGGlobal_OS1.0.11.0.ULFMIXM_cc95677d50_14.0.zip",
        "miui_LISAMXATGlobal_OS1.0.7.0.UKOMXAT_ae0703bbf7_14.0.zip",
        "miro-ota_full-OS2.0.104.0.VOMCNXM-user-15.0-f810008bcf.zip",
        "zircon_tr_global-ota_full-OS2.0.1.0.VNOTRXM-user-15.0-43991a0bac.zip"]
for rom in roms:
  print(common.getRegion(rom))