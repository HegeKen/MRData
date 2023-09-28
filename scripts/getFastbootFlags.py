import json
from sys import platform
import common


for device in common.fullDevices:
  codename = device
  if platform == "win32":
    devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    for rom in branch["links"]:
      if rom["fastboot"] == '':
        i = 0
      else:
        if ".tgz" in rom["fastboot"]:
          flag = rom["fastboot"].split('_images')[0]
          if flag in common.flags:
            i = 0
          else:
            if platform == "win32":
              file = open("static/data/scripts/Flags.json", "a", encoding='utf-8')
            else:
              file = open("/sdcard/Codes/NuxtMR/static/data/scripts/Flags.json", "a", encoding='utf-8')
            file.write("\""+flag+"\":\""+codename+"\",\n")
            file.close()
        elif ".exe" in rom["fastboot"]:
          flag = rom["fastboot"].split('_')[1]
          if flag in common.flags:
            i = 0
          else:
            if platform == "win32":
              file = open("static/data/scripts/Flags.json", "a", encoding='utf-8')
            else:
              file = open("/sdcard/Codes/NuxtMR/static/data/scripts/Flags.json", "a", encoding='utf-8')
            file.write("\""+flag+"\":\""+codename+"\",\n")
            file.close()
