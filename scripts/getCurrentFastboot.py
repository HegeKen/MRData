import requests
import json
from sys import platform
import common


base_url = 'https://update.miui.com/updates/miota-fullrom.php?d='
for device in common.currentStable:
  if platform == 'win32':
    devdata = json.loads(open('static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open('/sdcard/Codes/NuxtMR/static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  for branch in devdata['branches']:
    code = branch['code']
    if code == '':
      print('请修补机型： '+device+'文件中未指定的区域代码\n')
    else:
      i = 0
    btag = branch['btag']
    region = branch['region']
    carriers = branch['carrier']
    if region == 'cn':
      if len(carriers)==0:
        print('\r'+base_url+code+'&b='+btag+'&r='+region+'&n='+'                                   ',end='')
        common.getFastboot(base_url+code+'&b='+btag+'&r='+region+'&n=')
      else:
        for carrier in carriers:
          print('\r'+base_url+code+'&b='+btag+'&r='+region+'&n='+carrier+'                                   ',end='')
          common.getFastboot(base_url+code+'&b='+btag+'&r='+region+'&n='+carrier)
    elif region == 'global':
      print('\r'+base_url+code+'&b='+btag+'&r='+region+'&n='+'                                   ',end='')
      common.getFastboot(base_url+code+'&b='+btag+'&r='+region+'&n=')
    else:
      print('\r'+base_url+code+'&b='+btag+'&r='+region+'&n='+'                                   ',end='')
      common.getFastboot(base_url+code+'&b='+btag+'&r='+region+'&n=')
      print('\r'+base_url+code+'&b='+btag+'&r='+code.split('_global')[0]+'&n='+'                                   ',end='')
      print('\r'+base_url+code+'&b='+btag+'&r=eea&n='+'                                   ',end='')
      common.getFastboot(base_url+code+'&b='+btag+'&r=eea&n=')
      common.getFastboot(base_url+code+'&b='+btag+'&r='+code.split('_global')[0]+'&n=')
      print('\r'+base_url+code+'&b='+btag+'&r=global'+'&n='+'                                   ',end='')
      common.getFastboot(base_url+code+'&b='+btag+'&r=global'+'&n=')
