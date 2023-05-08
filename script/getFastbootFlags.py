import json
from sys import platform

# devlist = json.loads(open("static/data/data/getFlags.json", 'r', encoding='utf-8').read())["full"]
devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["MiFlashProCurrent"]
for device in all_devices:
  codename = device["codename"]
  devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    for rom in branch["links"]:
      if rom["fastboot"] == '':
        i = 0
      else:
        flag = rom["fastboot"].split('_images')[0]
        print(flag)
        if flag in device["checkers"]:
          i = 0
        else:
          file = open("static/data/script/Flags.json", "a", encoding='utf-8')
          file.write("\""+flag+"\",\n")
          file.close()

