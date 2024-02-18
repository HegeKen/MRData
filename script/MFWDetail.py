import requests
from bs4 import BeautifulSoup
import json
from sys import platform

# https://mifirmware.com/firmware/
def getDetail(url):
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
  headers = {"Connection": "close"}
  domains = ["bigota.d.miui.com","hugeota.d.miui.com"]
  response = requests.get(url, headers=headers)
  print("\r"+url+"                                           ",end="")
  if (response.status_code != 404):
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content,'lxml')
    lists = soup.find_all("a", attrs={"class" :"elementor-button-link"})
    if len(lists) == 0 :
      i = 0
    else:
      for list in lists:
        rom_url = list.attrs['href']
        if rom_url.split('/')[2] in domains:
          packname = rom_url.split('/')[4].strip('||Download')
          checker = packname.split('_')[1]
          flag = rom_url.split('/')[3][-6:]
          if platform == "win32":
            FBflags = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
            REflags = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"]
          else:
            FBflags = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
            REflags = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"]
          if "blockota" in packname:
            i = 0
          elif "DEV" in packname:
            i = 0
          else:
            if ".zip" in rom_url:
              if checker in REflags:
                if platform == "win32":
                  devdata = json.loads(open("public/MRdata/data/devices/"+REflags[checker]+".json", 'r', encoding='utf-8').read()).__str__()
                else:
                  devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+REflags[checker]+".json", 'r', encoding='utf-8').read()).__str__()
                if packname in devdata:
                  i = 0
                else:
                  print("发现未收录版本")
                  if platform == "win32":
                    file = open("public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
                  else:
                    file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
                  file.write(packname+"\n")
                  file.close()
              else:
                print("发现未收录机型以及版本")
                if platform == "win32":
                  file = open("public/MRdata/script/2023NewROMFlags.txt", "a", encoding='utf-8')
                else:
                  file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMFlags.txt", "a", encoding='utf-8')
                file.write(checker +"\t"+ packname+"\n")
                file.close()
            elif ".tgz" in rom_url:
              if flag in FBflags:
                if platform == "win32":
                  devdata = json.loads(open("public/MRdata/data/devices/"+FBflags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
                else:
                  devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+FBflags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
                if packname in devdata:
                  i = 0
                else:
                  print("发现未收录版本")
                  if platform == "win32":
                    file = open("public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
                  else:
                    file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
                  file.write(packname+"\n")
                  file.close()
              else:
                print("发现未收录机型以及版本")
                if platform == "win32":
                  file = open("public/MRdata/script/2023NewROMFlags.txt", "a", encoding='utf-8')
                else:
                  file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMFlags.txt", "a", encoding='utf-8')
                file.write(flag +"\t"+ packname+"\n")
                file.close()
            else:
              i = 0
        else:
          i = 0
  response.close()

if platform == "win32":
  links = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["MFWCurrent"]
else:
  links = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["MFWCurrent"]
for link in links:
  url = "https://mifirmware.com/" + link + "/"
  getDetail(url)
