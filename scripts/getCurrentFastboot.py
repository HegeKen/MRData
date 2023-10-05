import requests
import json
from sys import platform
import common

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
for device in common.currentStable:
  if platform == "win32":
    devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  for branch in devdata["branches"]:
    code = branch["code"]
    if code == "":
      print("请修补机型： "+device+"文件中未指定的区域代码\n")
    else:
      i = 0
    btag = branch["btag"]
    region = branch["region"]
    carriers = branch["carrier"]
    if region == "cn":
      if len(carriers)==0:
        url = base_url+code+"&b="+btag+"&r="+region+"&n="
        print("\r"+url+"                                   ",end="")
        common.getFastboot(url)
      else:
        for carrier in carriers:
          url = base_url+code+"&b="+btag+"&r="+region+"&n="+carrier
          print("\r"+url+"                                   ",end="")
          common.getFastboot(url)
    elif region == "global":
      url = base_url+code+"&b="+btag+"&r="+region+"&n="
      print("\r"+url+"                                   ",end="")
      common.getFastboot(url)
    else:
      url = base_url+code+"&b="+btag+"&r="+region+"&n="
      print("\r"+url+"                                   ",end="")
      common.getFastboot(url)
      print("\r"+url+"                                   ",end="")
      url = base_url+code+"&b="+btag+"&r=global"+"&n="
      common.getFastboot(url)
