import requests
import json
from sys import platform

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
headers = {"Connection": "close"}
domains = ["https://sgp-api.buy.mi.com/bbs/api/","https://ams-api.buy.mi.com/bbs/api/"]
params = "/phone/getlinepackagelist"
regions = ["global","rs","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]



def getFastboot(region):
  for domain in domains:
    url = domain+region+params
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    if (response.status_code != 404):
      packages = json.loads(content)["data"]
      if packages == None:
        i = 0
      else:
        for package in packages:
          fastboot = package["package_url"].split('/')[4]
          flag = package["package_url"].split('/')[3][-6:]
          if platform == "win32":
            flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
          else:
            flags = json.loads(open("/sdcard/Codes/NuxtMR/static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
          if flag in flags:
            if platform == "win32":
              devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
            else:
              devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
            if fastboot in devdata:
              print("\r"+url+"      ",end="")
            else:
              print("发现未收录版本")
              if platform == "win32":
                file = open("static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
              else:
                file = open("/sdcard/Codes/NuxtMR/static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
              file.write(fastboot+"\n")
              file.close()
          else:
            print("发现未收录机型以及版本")
            if platform == "win32":
              file = open("static/data/script/2023NewROMFlags.txt", "a", encoding='utf-8')
            else:
              file = open("/sdcard/Codes/NuxtMR/static/data/script/2023NewROMFlags.txt", "a", encoding='utf-8')
            file.write(flag +"\t"+ fastboot+"\n")
            file.close()
    else:
      i = 0



for region in regions:
  getFastboot(region)
