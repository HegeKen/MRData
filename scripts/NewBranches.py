import common
from datetime import datetime

for device in common.fullDevices:
  devdata = common.loadJson(device)
  for branch in devdata['branches']:
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      i = 0
    else:
      for bigv in devdata['miui']:
        for andv in devdata['android']:
          version = bigv+".2.0."+common.android(andv)+devdata['code']+branch['tag']
          if version in devdata:
            i = 0
          else:
            print('\r', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device, branch['code'], branch['region'], 'F', branch['zone'], andv, version,'          ', end='')
            if device in common.onedevices:
              common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], '', 'F', branch['zone'], andv, version)),device)
            else:
              common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], 'F', branch['zone'], andv, version)),device)