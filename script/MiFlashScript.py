import requests
import json
from sys import platform

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
# regions = ["cn","tw","global","rs","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]
regions = ["cn","tw","global","eea","ru","in","id","jp","tr",""]
carriers = ["","chinatelecom","chinaunicom","chinamobile"]
branches = ["F","X"]
# branches = ["F"]
headers = {"user-agent": "XiaomiPCSuite"}
headers = {"Connection": "close"}
if platform == "win32":
  devices = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["MiFlashProCurrent"]
else:
  devices = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["MiFlashProCurrent"]

for device in devices:
  checkers = device["checkers"]
  for checker in checkers:
    for region in regions:
      if region == "cn":
        for branch in branches:
          for carrier in carriers:
            url = base_url+checker+"&b="+branch+"&r=cn&n="+carrier
            print("\r"+url+"                 ",end="")
            response = requests.post(url, headers=headers)
            if (response.status_code == 200):
              content = response.content.decode("utf8")
              if content == "":
                i = 0
              else:
                data = json.loads(content)["LatestFullRom"]
                if len(data)>0:
                  if platform == "win32":
                    devdata = json.loads(open("public/MRdata/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
                  else:
                    devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
                  if data["filename"] in devdata:
                    i= 0
                  else:
                    print("发现一条新数据")
                    if platform == "win32":
                      filename = "public/MRdata/script/2023NewROMs.txt"
                    else:
                      filename = "/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt"
                    file = open(filename, "a", encoding='utf-8')
                    file.write(data["filename"]+"\n")
                    file.close()
                else:
                  i = 0
            else:
              i = 0
            response.close()
      else:
        url = base_url+checker+"&b=F&r="+region+"&n="
        print("\r"+url+"                 ",end="")
        response = requests.post(url, headers=headers)
        if (response.status_code == 200):
          content = response.content.decode("utf8")
          if content == "":
            i = 0
          else:
            data = json.loads(content)["LatestFullRom"]
            if len(data)>0:
              if platform == "win32":
                devdata = json.loads(open("public/MRdata/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
              else:
                devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
              if data["filename"] in devdata:
                i= 0
              else:
                print("发现一条新数据")
                if platform == "win32":
                  filename = "public/MRdata/script/2023NewROMs.txt"
                else:
                  filename = "/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt"
                file = open(filename, "a", encoding='utf-8')
                file.write(data["filename"]+"\n")
                file.close()
            else:
              i = 0
        else:
          i = 0
        response.close()
