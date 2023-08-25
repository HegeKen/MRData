import requests
import json
from bs4 import BeautifulSoup
import time
from sys import platform

def getRom(codename):
  if platform == "win32":
    devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
  else:
    devlist = open("/sdcard/Codes/NuxtMR/static/data/script/crawler.json", 'r', encoding='utf-8')
  all_devices = json.loads(devlist.read())["MDbeta"]
  for all in all_devices:
    code = all["code"]
    if code==codename:
      cname = all["NameCn"]
      ename = all["NameEn"]
    else:
      i = 0
  url = "https://miuidownload.com/miui/" +codename+"/beta/"
  t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  print("\r"+t+"\t"+url+"     ",end="")
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
  headers = {"Connection": "close"}
  response = requests.get(url, headers=headers)
  content = response.content.decode("utf8")
  soup = BeautifulSoup(content,'lxml')
  lists = soup.find_all("a", attrs={"class" :"downloadbutton"})
  for list in lists:
    rom_url = list.attrs['href']
    if(rom_url == ''):
      i = 0
    else:
      if "blockota" in rom_url:
        i = 0
      else:
        ver = rom_url.split('/')[3]
        recovery = rom_url.split('/')[4]
        android = recovery.split('_')[4].strip(".zip")
        vers = ["V14.0.23.8.21.DEV"]
        for v in vers:
          if v == ver:
            if platform == "win32":
              fine = "static/data/data/devices/"+codename+".json"
            else:
              fine = "/sdcard/Codes/NuxtMR/static/data/data/devices/"+codename+".json"
            devicedata = open(fine, 'r', encoding='utf-8')
            devdata = json.loads(devicedata.read())
            if recovery in devdata.__str__():
              i = 0
            else:
              print("尚未收录该本版,版本为："+v+"\t机型："+cname+"("+codename+")")
              if platform == "win32":
                filename = "static/data/script/MDBeta.json"
              else:
                filename = "/sdcard/Codes/NuxtMR/static/data/script/MDBeta.json"
              file = open(filename, "a", encoding='utf-8')
              datas = {'code':device,'NameCn':cname,'NameEn':ename,'miui': ver, 'android': android, 'recovery':recovery,'fastboot':""}
              person_json = json.dumps(datas,ensure_ascii=False)
              file.write(person_json+",")
              file.close()
            devicedata.close()
          else:
            i = 0
  devlist.close()
  response.close()



current = ["venus", "star", "renoir", "cupid", "zeus", "psyche", "mayfly", "daumier", "unicorn", "thor", "fuxi", "nuwa", "ishtar", "cetus",
           "odin", "zizhan", "nabu", "elish", "enuma", "dagu","pipa","liuqin", "mona", "zijin","pissarro", "xaga", "munch",
           "rubens", "matisse", "ingres", "diting", "mondrian", "socrates"]



for device in current:
  getRom(device)
