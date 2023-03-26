import requests
import json
import time
from bs4 import BeautifulSoup


def checkExist(codename,package):
  devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read()).__str__()
  if package in devdata:
    i = 0
  else:
    print("发现未收录版本")
    file = open("static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
    file.write(package+"\n")
    file.close()


devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
devices = json.loads(devlist.read())["XiaomiRomCurrent"]
for device in devices:
  url = "https://xiaomirom.com/rom/"+device+"/"
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
  headers = {"Connection": "close"}
  response = requests.get(url, headers=headers)
  content = response.content.decode("utf8")
  soup = BeautifulSoup(content,'lxml')
  lists = soup.find_all("p")
  for list in lists:
    if ".zip" in list.text:
      packname = list.text.split(' |')[0]
      print("\r"+packname+"                                           ",end="")
      version = packname.split('_')[2]
      checker = packname.split('_')[1]
      flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"]
      if checker in flags:
        codename = flags[checker]
        checkExist(codename,packname)
      else:
        print("发现未收录机型以及版本")
        file = open("static/data/script/2023NewROMFlags.txt", "a", encoding='utf-8')
        file.write(checker +"\t"+ packname+"\n")
        file.close()
    elif ".tgz"in list.text:
      packname = list.text.split(' |')[0]
      print("\r"+packname+"                                           ",end="")
      version = packname.split('_images_')[1].split('_')[0]
      checker = packname.split('_images_')[1].split('_')[0][-6:]
      if version[0] == "V":
        if "DEV" in version:
          codename = packname.split('_')[0]
          checkExist(codename,packname)
        else:
          flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
          if checker in flags:
            codename = flags[checker]
            checkExist(codename,packname)
          else:
            print("发现未收录机型以及版本")
            file = open("static/data/script/2023NewROMFlags.txt", "a", encoding='utf-8')
            file.write(checker +"\t"+ packname+"\n")
            file.close()
      else:
        codename = packname.split('_')[0]
        checkExist(codename,packname)
    else:
      i = 0
  response.close()
  time.sleep(3)
