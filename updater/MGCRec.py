import requests
import json
import re
import random
import os
import time

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
base_api = "https://sgp-api.buy.mi.com/bbs/api/"
ahome = "/phone/getdevicelist?phone_id="
regions = ["global","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","rs","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]


with open('static/data/updater/global.json', 'r', encoding='utf8')as devices:
  all_devices = json.load(devices)
  devices_data = all_devices["full"]
  for device in devices_data:
    devicedata = open("static/data/data/devices/"+device["code"]+".json", 'r', encoding='utf-8')
    devdata = json.loads(devicedata.read())
    devicename = devdata["cnname"]
    devicecode = devdata["codename"]
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print('\r'+t+"\t"+devicename+"("+devicecode+")")
    ids = device["gid"]
    for region in regions:
      for id in ids:
        if (region == "rs"):
          url = "https://ams-api.buy.mi.com/bbs/api/rs/phone/getdevicelist?phone_id=" + str(id)
        else:
          url = base_api + region + ahome + str(id)
        response = requests.get(url, headers=headers)
        if (response.status_code != 404):
          content = response.content.decode("utf8")
          regex = r'https://bigota.d.miui.com/(.*?).*?.\.zip'
          matches = re.finditer(regex, content, re.MULTILINE)
          for match in matches:
            rom_url = match.group()
            recovery = rom_url.split('/')[4]
            ver = rom_url.split('/')[3]
            pr = random.randint(1,2)
            if recovery in devdata.__str__():
              slist = ["─", "│"]
              print('\r'+slist[pr%2], end="")
            else:
              filename = "static/data/updater/MGCRec.txt"
              file = open(filename, "a", encoding='utf-8')
              file.writelines(id+"("+devicename+")\t"+rom_url+"\n")
              print("\n在"+id+"("+devicename+")处发现疑似一条更新内容,机型名称"+devicename+"\t版本："+ver)
        response.close()
