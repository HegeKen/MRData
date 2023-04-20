from selenium import webdriver
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import json
import time


options = EdgeOptions()
options.use_chromium = True
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\112.0.1722.48\msedge.exe"
driver = Edge(options=options, executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\112.0.1722.48\msedgedriver.exe")

# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# https://msedgewebdriverstorage.z22.web.core.windows.net/
# https://mifirmware.com/xiaomi-software-update/
# https://mifirmware.com/xiaomi-miui-14/
# https://mifirmware.com/xiaomi-firmware/
# https://mifirmware.com/firmware/
driver.get("https://mifirmware.com/xiaomi-firmware/")
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
      flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
      if flag in flags:
        recode = flags[flag]
      else:
        print(flag)
    devdata = json.loads(open("static/data/data/devices/"+recode+".json", 'r', encoding='utf-8').read()).__str__()
    if pack_name in devdata:
      i = 0
    else:
      print("发现未收录版本")
      file = open("static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
      file.write(pack_name+"\n")
      file.close()
  elif ".tgz" in link:
    pack_name = link.split('/')[4]
    flag = link.split('/')[3][-6:]
    flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
    if flag in flags:
      devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
      if pack_name in devdata:
        i = 0
      else:
        print("发现未收录版本")
        file = open("static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
        file.write(pack_name+"\n")
        file.close()
    else:
      print("发现未收录机型以及版本")
      file = open("static/data/script/2023NewROMFlags.txt", "a", encoding='utf-8')
      file.write(flag +"\t"+ pack_name+"\n")
      file.close()
  else:
    i = 0
