import json
from sys import platform
import common


for device in common.currentStable:
  devdata = json.loads(open('static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())['branches']
  for branch in devdata:
    if branch['cnname'] == '开发者预览版' or branch['cnname'] == '原生安卓':
      i = 0
    else:
      for rom in branch['links']:
        if rom['miui'] == '':
          print(device +'\t'+ branch['cnname'] +'\t'+rom['miui'] +'\t'+ ' MIUI 版本为空')
        if rom['android'] == '':
          print(device +'\t'+ branch['cnname'] +'\t'+rom['miui'] +'\t'+ ' Android 版本为空')
        if rom['recovery'] == '':
          if rom['android'] in rom['fastboot']:
            i = 0
            # print(device + branch['cnname'] +rom['miui'] + 'check passed')
          else:
            print(device +'\t'+ branch['cnname'] +'\t'+rom['miui'] +'\t'+ ' android version check failed')
          if rom['miui'] in rom['fastboot']:
            i = 0
            # print(device + branch['cnname'] +rom['miui'] + 'check passed')
          else:
            print(device +'\t'+ branch['cnname'] +'\t'+rom['miui'] +'\t'+ ' miui version check failed')
        elif rom['android'] in rom['recovery']:
          i = 0
          # print(device + branch['cnname'] +rom['miui'] + 'check passed')
        elif rom['miui'] in rom['recovery']:
          i = 0
        else:
          print(device +'\t'+ branch['cnname'] +'\t'+rom['miui'] +'\t'+ 'check failed')
