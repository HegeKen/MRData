from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import json
from sys import platform

# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# https://msedgewebdriverstorage.z22.web.core.windows.net/
# https://msedgedriver.azureedge.net/114.0.1823.67/edgedriver_win64.zip
# https://mifirmware.com/xiaomi-software-update/
# https://mifirmware.com/xiaomi-miui-14/
# https://mifirmware.com/xiaomi-firmware/

urls = ["https://mifirmware.com/xiaomi-software-update/","https://mifirmware.com/xiaomi-miui-14/","https://mifirmware.com/xiaomi-firmware/","https://mifirmware.com/xiaomi-software-update/","https://mifirmware.com/stable-beta/"]

options = Options()
# options.binary_location = r"C:\Users\Hege\AppData\Local\Microsoft\Edge SxS\Application\118.0.2047.0\msedge.exe"
driver = webdriver.Edge(options=options)
for url in urls:
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, "lxml")
  lists = soup.find_all("a", attrs={"data-content" :"Download"})
  for list in lists:
    link = list.attrs['href']
    if ".zip" in link:
      pack_name = link.split('/')[4]
      if "DEV" in link:
        recode = pack_name.split('_')[1].lower()
      else:
        flag = link.split('/')[3][-6:]
        if platform == "win32":
          flags = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
        else:
          flags = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
        if flag in flags:
          recode = flags[flag]
        else:
          print(flag)
      if platform == "win32":
        devdata = json.loads(open("public/MRdata/data/devices/"+recode+".json", 'r', encoding='utf-8').read()).__str__()
      else:
        devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+recode+".json", 'r', encoding='utf-8').read()).__str__()
      if pack_name in devdata:
        i = 0
      else:
        print("发现未收录版本")
        if platform == "win32":
          file = open("public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
        else:
          file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
        file.write(pack_name+"\n")
        file.close()
    elif ".tgz" in link:
      if "DEV" in link:
        i = 0
      else:
        pack_name = link.split('/')[4]
        flag = link.split('/')[3][-6:]
        if platform == "win32":
          flags = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
        else:
          flags = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
        if flag in flags:
          if platform == "win32":
            devdata = json.loads(open("public/MRdata/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
          else:
            devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
          if pack_name in devdata:
            i = 0
          else:
            print("发现未收录版本")
            if platform == "win32":
              file = open("public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
            else:
              file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
            file.write(pack_name+"\n")
            file.close()
        else:
          print("发现未收录机型以及版本")
          if platform == "win32":
            file = open("public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
          else:
            file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt", "a", encoding='utf-8')
          file.write(flag +"\t"+ pack_name+"\n")
          file.close()
    else:
      i = 0
