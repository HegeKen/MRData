import yaml
import common

# 读取yaml文件
with open('../Sources/xmfirmwareupdater.github.io/data/devices/full.yml', 'r') as file:
  data = yaml.safe_load(file)

# 逐行读取filename并打印
for entry in data:
  if 'filename' in entry:
    if "OS2" in entry['filename']:
      filename = entry['filename'].strip("fw_")
      coder = filename.split("-ota_full")[0]
      code = '_'.join(coder.split("_")[int((coder.count('_')+1)/2):])
      filename = code+"-ota_full"+filename.split("-ota_full")[1]
    else:
      filname = '_'.join(entry['filename'].split("_")[2:])
    if filname.startswith('india_miui'):
      i = 0
    else:
      common.checkExist(filname)