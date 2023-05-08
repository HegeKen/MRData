import requests
import json
import time
from bs4 import BeautifulSoup
from sys import platform

# miuimenubutton
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
headers = {"Connection": "close"}
if platform == "win32":
  devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
else:
  devlist = open("/sdcard/Codes/NuxtMR/static/data/script/crawler.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["MDcurrent"]
for all in all_devices:
  codename = all["code"]
  print("正在完成"+codename+"机型")
  response = requests.get("https://miuidownload.com/miui/"+codename+"/", headers=headers)
  content = response.content.decode("utf8")
  soup = BeautifulSoup(content,'lxml')
  branches = soup.find_all("a", attrs={"class" :"miuimenubutton"})
  if len(branches) == 0 :
    i = 0
  else:
    for branch in branches:
      new_url = "https://miuidownload.com"+branch.attrs['href']+"/"
      bresp = requests.get("https://miuidownload.com/miui/"+codename+"/", headers=headers)
      bcon = bresp.content.decode("utf8")
      bsoup = BeautifulSoup(content,'lxml')
      lists = bsoup.find_all("a", attrs={"class" :"downloadbutton"})
      if len(lists) == 0 :
        i = 0
      else:
        for list in lists:
          rom_url = list.attrs['href']
        if(rom_url == ''):
           i = 0
        else:
          if "blockota" in rom_url:
            i = 0
          else:
            packname = rom_url.split('/')[4]
            if platform == "win32":
              fine = "static/data/data/devices/"+codename+".json"
            else:
              fine = "/sdcard/Codes/NuxtMR/static/data/data/devices/"+codename+".json"
            devicedata = open(fine, 'r', encoding='utf-8')
            devdata = json.loads(devicedata.read())
            if packname in devdata.__str__():
              i = 0
            else:
              print("尚未收录该本版\t"+codename+"\t"+packname)
              if platform == "win32":
                filename = "static/data/script/2023NewROMs.txt"
              else:
                filename = "/sdcard/Codes/NuxtMR/static/data/script/2023NewROMs.txt"
              file = open(filename, "a", encoding='utf-8')
              file.write(packname+"\n")
              file.close()
      bresp.close()
  response.close()
