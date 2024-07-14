import common

for device in common.currentStable:
  devdata = common.loadJson(device)
  for branch in devdata['branches']:
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], branch['links'][0]['android'], branch['links'][0]['miui'])),device)
    else:
      common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], branch['links'][0]['android'], branch['links'][0]['miui'])),device)
      if branch['links'][0]['miui'] == "":
        i = 0
      else:
        for i in range(0,3):
          common.getFromApi(common.miui_encrypt(common.OTAFormer(device, branch['code'], branch['region'], branch['btag'], branch['zone'], branch['links'][0]['android'], common.versionAdd(branch['links'][0]['miui'],i))),device)