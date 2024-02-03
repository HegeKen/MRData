import json
import common


devdata = json.loads(open('static/data/scripts/MiFlashPro/cc.json', 'r', encoding='utf-8').read())

for test in devdata['entity']['ongoingPlans']['items']:
  package = test["testing"]["apps"][0]["downloadUrl"]
  if "ultimateota" in package:
    rom = package.split('/')[4].split('?')[0]
    common.checkExist(rom)
