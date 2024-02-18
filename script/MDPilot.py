import requests
import json
from bs4 import BeautifulSoup
import time
from sys import platform

branches = ["beta","pilot"]
if platform == "win32":
  devlist = open("public/MRdata/script/crawler.json", 'r', encoding='utf-8')
else:
  devlist = open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["MDcurrent"]
for all in all_devices:
  codename = all["code"]
  for branch in branches:
    url = "https://miuidownload.com/miui/"+codename+"/"+branch+"/"
    print("\r"+url+"              ",end="")
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content,'lxml')
    lists = soup.find_all("a", attrs={"class" :"downloadbutton"})
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
              fine = "public/MRdata/data/devices/"+codename+".json"
            else:
              fine = "/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+codename+".json"
            devicedata = open(fine, 'r', encoding='utf-8')
            devdata = json.loads(devicedata.read())
            if packname in devdata.__str__():
              i = 0
            else:
              t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
              print("\n"+t+"\t"+url+"     发现尚未收录本版",end="")
              if platform == "win32":
                filename = "public/MRdata/script/2023NewROMs.txt"
              else:
                filename = "/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt"
              file = open(filename, "a", encoding='utf-8')
              file.write(packname+"\n")
              file.close()
            devicedata.close()
    response.close()
devlist.close()
