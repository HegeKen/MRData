import requests
import json
import re


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
base_api = "https://sgp-api.buy.mi.com/bbs/api/"
ahome = "/phone/getdevicelist?phone_id="
regions = ["global","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","rs","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]


filename = "static/data/updater/crawler.json"
devices = json.loads(open(filename, 'r', encoding='utf-8').read())["MGC"]
for device in devices:
  id = device["id"]
  for region in regions:
    if (region == "rs"):
      url = "https://ams-api.buy.mi.com/bbs/api/rs/phone/getdevicelist?phone_id=" + str(id)
    else:
      url = base_api + region + ahome + str(id)
    print("\r"+url+"       ",end="")
    response = requests.get(url, headers=headers)
    if (response.status_code != 404):
      content = response.content.decode("utf8")
      regex = r'https://bigota.d.miui.com/(.*?).*?.\.zip'
      matches = re.finditer(regex, content, re.MULTILINE)
      for match in matches:
        rom_url = match.group()
        recovery = rom_url.split('/')[4]
        ver = rom_url.split('/')[3]
        mlen = len(device["codes"])
        i = 0
        for model in device["codes"]:
          devicedata = open("static/data/data/devices/"+model+".json", 'r', encoding='utf-8')
          devdata = json.loads(devicedata.read())
          devicename = devdata["cnname"]
          devicecode = devdata["codename"]
          if recovery in devdata.__str__():
            i = i - 1
          else:
            i = i + 1
        if i == mlen:
          print(recovery+"\t"+url)
        else:
          break
