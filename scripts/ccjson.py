import json
import common


devdata = json.loads(open('public/MRdata/scripts/MiFlashPro/cc.json', 'r', encoding='utf-8').read())

for test in devdata['entity']['ongoingPlans']['items']:
  if test['type'] == "MIUI":
    package = test["testing"]["apps"][0]["downloadUrl"]
    if "ultimateota" in package:
      rom = package.split('/')[4].split('?')[0]
      common.checkExist(rom)
  else:
    i = 0
