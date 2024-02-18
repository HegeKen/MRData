import requests
import common
import json
from sys import platform

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


for device in common.test:
  if platform == 'win32':
    devdata = json.loads(open('public/MRdata/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open('/sdcard/Codes/NuxtMR/public/MRdata/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  for branch in devdata['branches']:
    latest = 0
    common.MiOTAForm2['d'] = branch['code']
    if branch['region'] == 'cn':
      common.MiOTAForm2['pn'] = branch['code']
    else:
      if branch['code'] == devdata['codename']+'_global':
        common.MiOTAForm2['pn'] = branch['code']
      else:
        common.MiOTAForm2['pn'] = branch['code'].split('_global')[0]
    common.MiOTAForm2['b'] = branch['btag']
    common.MiOTAForm2['options']['zone'] = branch['zone']
    if branch['ep'] == 1:
      latest = 0
    else:
      i = 0
    for link in branch['links']:
      if latest == link['android']:
        i = 0
      else:
        common.MiOTAForm2['c'] = link['android'].split('.')[0]
        common.MiOTAForm2['v'] = 'MIUI-'+ link['miui']
        if common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm2)),device) == 0:
            if platform == 'win32':
              file = open('public/MRdata/scripts/checkOTA.txt', 'a', encoding='utf-8')
            else:
              file = open('/sdcard/Codes/NuxtMR/public/MRdata/script/checkOTA.txt', 'a', encoding='utf-8')
            if branch['branch'] == 'cnmp':
              i = 0
            else:
              file.write(devdata['zh-cn']+'('+device+'),\t'+branch['code']+',\t'+branch['zh-cn']+',\t'+branch['zone']+'\n')
              file.close()
        else:
          i = 0
        latest = link['android']
  print(devdata['zh-cn']+'已完成')
