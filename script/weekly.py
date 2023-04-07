import requests
import json
import time
import re
from bs4 import BeautifulSoup


def findCBeta(vers):
  i = 0
  devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
  all_devices = json.loads(devlist.read())["MDdevices"]
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
              fwrite = open("static/data/script/Weekly.json", 'a', encoding='utf-8')
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
  devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
  all_devices = json.loads(devlist.read())["MDdevices"]
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
              fwrite = open("static/data/script/Weekly.json", 'a', encoding='utf-8')
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


vers = ["V14.0.23.4.2.DEV"]
findCBeta(vers)
