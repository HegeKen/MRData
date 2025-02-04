import common
from openpyxl import load_workbook
import pandas as pd


file_path = "roms.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')
data_string = df.to_csv(sep='\t', index=False, header=False)

for device in common.fullDevices:
  devcode = common.stringify(device)
  devdata = common.loadJson(device)
  for branch in devdata['branches']:
    code = common.stringify(branch['code'])
    type=common.stringify("MIUI")
    region = common.stringify(branch['region'])
    btag = common.stringify(branch['btag'])
    tag = common.stringify(branch['branch'])
    zone = int(branch['zone'])
    for rom in reversed(branch['links']):
      version = common.stringify(rom['miui'])
      android = common.stringify(rom['android'])
      recovery = common.stringify(rom['recovery'])
      fastboot = common.stringify(rom['fastboot'])
      if rom['recovery'] in data_string:
        i = 0
      else:
        print("not in",device,rom['recovery'])