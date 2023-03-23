import requests
import json
import re
from bs4 import BeautifulSoup

def getFb(soup):
  regex = 'bigota.d.miui.com/V.*?._images_.*?.tgz'
  matches = re.finditer(regex, soup, re.MULTILINE)
  for match in matches:
    rom_url = match.group().split('?')[0]
    fastboot = rom_url.split('/')[2]
    codename = fastboot.split('_')[0]
    if codename == 'miui':
      i = 0
    else:
      ver = fastboot.split('_')[2]
      devicedata = open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8')
      devdata = json.loads(devicedata.read())
      if fastboot in devdata.__str__():
        i=0
      else:
        file = open("static/data/script/QQDoc.txt", "a", encoding='utf-8')
        file.write(fastboot+"\n")
        file.close()
        print("发现"+codename+"线刷包有新版本，版本号：->"+ver)
      devicedata.close()

def getRec(soup):
  regex = r'miui_.*?.zip'
  matches = re.finditer(regex, soup, re.MULTILINE)
  for match in matches:
    recovery = match.group()
    codename = recovery.split('_')[1].swapcase()
    ver = recovery.split('_')[2]
    devicedata = open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8')
    devdata = json.loads(devicedata.read())
    if recovery in devdata.__str__():
      i=0
    else:
      file = open("static/data/script/2023NewROMs.txt", "a", encoding='utf-8')
      file.write(recovery+"\n")
      file.close()
      print("发现"+codename+"卡刷包有新版本，版本号：->"+ver)
    devicedata.close()




url = "https://docs.qq.com/dop-api/opendoc?tab=BB08J2&_t=1673761065925&u=60faf5199d0e4c2a9dd346105a9729e6&noEscape=1&enableSmartsheetSplit=1&id=DRVh5eXVwY0RqVWJB&normal=1&outformat=1&startrow=0&endrow=60&wb=1&nowb=0&callback=clientVarsCallback&xsrf=58fba4d43fd69617&t=1675574100619"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
headers = {"Referer": "https://docs.qq.com/sheet/DRVh5eXVwY0RqVWJB?tab=BB08J2&_t=1673761065925&u=60faf5199d0e4c2a9dd346105a9729e6"}
headers = {"Connection": "close"}
response = requests.get(url, headers=headers)
if (response.status_code != 404):
  content = response.content.decode("utf8")
  soup = BeautifulSoup(content,'lxml')
  getRec(soup.__str__())
  getFb(soup.__str__())
else:
  print("访问失败")



