import requests
import json
import time
import re
from bs4 import BeautifulSoup


def findCBeta(vers):
  i = 0
  devlist = open("static/data/updater/devices.json", 'r', encoding='utf-8')
  all_devices = json.loads(devlist.read())["devices"]
  for all in all_devices:
    device = all["code"]
    cname = all["NameCn"]
    ename = all["NameEn"]
    fread = open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8')
    data = json.loads(fread.read())
    branches = data["branches"]
    for branch in branches:
      if branch["branch"] == "cnmp":
        for rom in branch["links"]:
          for ver in vers:
            if rom["miui"]==ver:
              fwrite = open("static/data/updater/getWeekly.json", 'a', encoding='utf-8')
              datas = {'code':device,'NameCn':cname,'NameEn':ename,'miui': ver, 'android': rom["android"], 'recovery':rom["recovery"],'fastboot':rom["fastboot"]}
              person_json = json.dumps(datas,ensure_ascii=False)
              fwrite.write(person_json+",")
              fwrite.close()
            else:
              i = i+1
      else:
        i = i+1
    fread.close()
  devlist.close()

def findGBeta(vers):
  i = 0
  devlist = open("static/data/updater/devices.json", 'r', encoding='utf-8')
  all_devices = json.loads(devlist.read())["devices"]
  for all in all_devices:
    device = all["code"]
    cname = all["NameCn"]
    ename = all["NameEn"]
    fread = open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8')
    data = json.loads(fread.read())
    branches = data["branches"]
    for branch in branches:
      if branch["branch"] == "mgbb":
        for rom in branch["links"]:
          for ver in vers:
            if rom["miui"]==ver:
              print(rom["recovery"])
              fwrite = open("static/data/updater/getWeekly.json", 'a', encoding='utf-8')
              datas = {'code':device,'NameCn':cname,'NameEn':ename,'miui': ver, 'android': rom["android"], 'recovery':rom["recovery"],'fastboot':rom["fastboot"]}
              person_json = json.dumps(datas,ensure_ascii=False)
              fwrite.write(person_json+",")
              fwrite.close()
            else:
              i = i+1
      else:
        i = i+1
    fread.close()
  devlist.close()


vers = ["V13.1.22.9.5.DEV","V13.1.22.9.7.DEV","V13.1.22.9.9.DEV"]
findCBeta(vers)
