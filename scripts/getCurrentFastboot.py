import requests
import json
from sys import platform
import common

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
           "Connection": "close"}

def getFastboot(url):
  response = requests.post(url, headers=headers)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    if content == "":
      i = 0
    else:
      data = json.loads(content)["LatestFullRom"]
      if len(data)>0:
        common.checkExit(data["filename"])
      else:
        i = 0
  else:
    i = 0
  response.close()
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
        getFastboot(url)
      else:
        for carrier in carriers:
          url = base_url+code+"&b="+btag+"&r="+region+"&n="+carrier
          print("\r"+url+"                                   ",end="")
          getFastboot(url)
    elif region == "global":
      url = base_url+code+"&b="+btag+"&r="+region+"&n="
      print("\r"+url+"                                   ",end="")
      getFastboot(url)
    else:
      url = base_url+code+"&b="+btag+"&r="+region+"&n="
      print("\r"+url+"                                   ",end="")
      getFastboot(url)
      print("\r"+url+"                                   ",end="")
      url = base_url+code+"&b="+btag+"&r=global"+"&n="
      getFastboot(url)
