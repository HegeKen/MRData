import common
from datetime import datetime
roms = ['miui_VENUS_V14.0.23.8.15.DEV_3bb57a35f6_13.0.zip',
        'water_global_images_V14.0.14.0.TGOMIXM_20230728.0000.00_13.0_51d00b79c3.tgz',
        'miui-blockota-zircon-V14.0.1.0.TNOCNXM-V14.0.3.0.TNOCNXM-45749d772b-13.0.zip']

# for file in roms:
#   common.checkExist(file)


# # import datetime
# # today = datetime.date(2024,2,7)
# # print(today)
# # dayOfWeek = today.weekday()
# # print(dayOfWeek)
# link = "https://bn.d.miui.com/OS1.0.24.1.29.DEV/miui_RUBENS_OS1.0.24.1.29.DEV_43b39a9e96_14.0.zip"
# print(link.split('/')[4])

# pack = "miui_EMERALDRUGlobal_OS1.0.2.0.UNFRUXM_535997a0b0_14.0.zip"
# origin = pack.split('_')[2]
# replaced = origin.replace(origin.split('.')[2],str(int(origin.split('.')[2])+1))
# print(origin +"- >"+ replaced)

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))