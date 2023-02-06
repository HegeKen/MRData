import requests
import json
import re
# import random
import time
# from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
regions = ["global","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","rs","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]

for region in regions:
  if (region == "rs"):
    url = "https://ams-api.buy.mi.com/bbs/api/rs/phone/getlinepackagelist"
  else:
    url = "https://sgp-api.buy.mi.com/bbs/api/"+region+"/phone/getlinepackagelist"
  response = requests.get(url, headers=headers)
  content = response.content.decode("utf8")
  t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  print(t+"\t"+url)
  if (response.status_code != 404):
    regex = r'bigota.d.miui.com/V.*?._images_.*?.tgz'
    matches = re.finditer(regex, content, re.MULTILINE)
    for match in matches:
      fastboot = match.group().split('/')[2]
      codename = fastboot.split('_')[0]
      checker = fastboot.split('_')[1]
      if codename == 'cannong':
        codename = 'cannon'
      else:
        i = 0
      if checker == 'c3l2':
        codename = 'dandelion_c3l2'
      elif checker == 'p':
        codename = codename+"_p"
      else:
        i = 0
      devicedata = open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8')
      devdata = json.loads(devicedata.read())
      if fastboot in devdata.__str__():
        i = 0
      else:
        filename = "static/data/updater/MGCFab.txt"
        file = open(filename, "a", encoding='utf-8')
        file.writelines(fastboot+"\n")
        print(codename+"处发现疑似一条更新内容,包名："+fastboot)
  else:
    i = 0
