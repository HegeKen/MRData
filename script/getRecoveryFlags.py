import json
from sys import platform

# devlist = json.loads(open("static/data/data/getFlags.json", 'r', encoding='utf-8').read())["full"]
if platform == "win32":
  devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
else:
  devlist = open("/sdcard/Codes/NuxtMR/static/data/script/crawler.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["MDcurrent"]
for device in all_devices:
  codename = device["code"]
  if platform == "win32":
    devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    for rom in branch["links"]:
      if rom["recovery"] == '':
        i = 0
      else:
        flag = rom["recovery"].split('_')[1]
        print(flag)
        if platform == "win32":
          fine = "static/data/script/Flags.json"
        else:
          fine = "/sdcard/Codes/NuxtMR/static/data/script/Flags.json"
        all_flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"].__str__()
        if flag in all_flags:
          i = 0
        else:
          if platform == "win32":
            file = open("static/data/script/Flags.json", "a", encoding='utf-8')
          else:
            file = open("/sdcard/Codes/NuxtMR/static/data/script/Flags.json", "a", encoding='utf-8')
          file.write("\""+flag+"\":\""+codename+"\",\n")
          file.close()

