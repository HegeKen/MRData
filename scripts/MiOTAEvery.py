import common
import json
from sys import platform

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


def FormRun(link):
  if link['android'] == '':
    common.MiOTAForm2['c'] = '13'
  else:
    common.MiOTAForm2['c'] = link['android'].split('.')[0]
  common.MiOTAForm2['sdk'] = common.sdk[common.MiOTAForm2['c']]
  common.MiOTAForm2['v'] = 'MIUI-'+ link['miui']
  if common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm2)),device) == 0:
      if platform == 'win32':
        file = open('static/data/scripts/checkOTA.txt', 'a', encoding='utf-8')
      else:
        file = open('/sdcard/Codes/NuxtMR/static/data/script/checkOTA.txt', 'a', encoding='utf-8')
      if branch['branch'] == 'cnmp':
        i = 0
      else:
        file.write(devdata['zh-cn']+'('+device+'),\t'+branch['code']+',\t'+branch['zh-cn']+',\t'+link['android']+',\t'+branch['zone']+'\n')
        file.close()
  else:
    i = 0

for device in common.currentStable:
  if platform == 'win32':
    devdata = json.loads(open('static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open('/sdcard/Codes/NuxtMR/static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  for branch in devdata['branches']:
    if branch['btag'] == 'X':
      i = 0
    else:
      common.MiOTAForm2['d'] = branch['code']
      if branch['region'] == 'cn':
        common.MiOTAForm2['pn'] = branch['code']
      else:
        if branch['code'] == devdata['codename']+'_global':
          common.MiOTAForm2['pn'] = branch['code']
        else:
          common.MiOTAForm2['pn'] = branch['code'].split('_global')[0]
      common.MiOTAForm2['b'] = branch['btag']
      common.MiOTAForm2['options']['zone'] = '1'
      for link in branch['links']:
        FormRun(link)
      common.MiOTAForm2['options']['zone'] = '2'
      for link in branch['links']:
        FormRun(link)
      common.MiOTAForm2['options']['zone'] = '3'
      for link in branch['links']:
        FormRun(link)
  print('\r'+devdata['zh-cn']+'已完成                            ',end='')
