import requests
import json
from bs4 import BeautifulSoup

branches = ["beta","pilot"]
devlist = open("static/data/updater/global.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["full"]
for all in all_devices:
  codename = all["code"]
  for branch in branches:
    url = "https://miuidownload.com/miui/"+codename+"/"+branch+"/"
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
          print("未查询到刷机包数据\t机型代号："+codename+"\t链接："+url)
        else:
          if "blockota" in rom_url:
            i = 0
          else:
            packname = rom_url.split('/')[4]
            fine = "static/data/data/devices/"+codename+".json"
            devicedata = open(fine, 'r', encoding='utf-8')
            devdata = json.loads(devicedata.read())
            if packname in devdata.__str__():
              i = 0
            else:
              print("尚未收录该本版")
              filename = "static/data/updater/MDPilot.txt"
              file = open(filename, "a", encoding='utf-8')
              file.write(packname+"\n")
              file.close()
    response.close()
devlist.close()
