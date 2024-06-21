import common

for device in common.currentStable:
  devdata = common.loadJson(device)
  for branch in devdata['branches']:
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], branch['links'][0]['android'], branch['links'][0]['miui'])),device)
    else:
      for rom in branch['links']:
        for i in range(-3,3):
          if int(rom['miui'].split('.')[2])+i > 0 :
            version = common.versionAdd(rom['miui'],i)
            if version in devdata:
              i = 0
            else:
              common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], rom['android'], version)),device)
          else:
            i = 0