import common

for device in common.fullDevices:
  devdata = common.loadJson(device)
  for branch in devdata['branches']:
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      # common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], branch['links'][0]['android'], branch['links'][0]['miui'])),device)
      i = 0
    else:
      for rom in branch['links']:
        for i in range(-3,3):
          if rom['miui'][0] == 'V':
            if int(rom['miui'].split('.')[2])+i > 0 :
              version = common.versionAdd(rom['miui'],i)
              if version in devdata:
                i = 0
              else:
                common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], rom['android'], version)),device)
            else:
              i = 0