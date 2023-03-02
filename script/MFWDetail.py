import requests
from bs4 import BeautifulSoup
import json

def getDetail(url):
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
  response = requests.get(url, headers=headers)
  if (response.status_code != 404):
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content,'lxml')
    lists = soup.find_all("a", attrs={"class" :"elementor-button-link"})
    if len(lists) == 0 :
      i = 0
    else:
      for list in lists:
        rom_url = list.attrs['href']
        packname = rom_url.split('/')[4]
        flag = rom_url.split('/')[3][-6:]
        flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
        if ".zip" in rom_url:
          if flag in flags:
            devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
            if packname in devdata:
              i = 0
            else:
              print("发现未收录版本")
              file = open("static/data/script/MFW/MFWGetRec.txt", "a", encoding='utf-8')
              file.write(packname+"\n")
              file.close()
          else:
            print("发现未收录机型以及版本")
            file = open("static/data/script/MFW/MFWFlags.txt", "a", encoding='utf-8')
            file.write(flag +"\t"+ packname+"\n")
            file.close()
        elif ".tgz" in rom_url:
          if flag in flags:
            devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
            if packname in devdata:
              i = 0
            else:
              print("发现未收录版本")
              file = open("static/data/script/MFW/MFWGetFab.txt", "a", encoding='utf-8')
              file.write(packname+"\n")
              file.close()
          else:
            print("发现未收录机型以及版本")
            file = open("static/data/script/MFW/MFWFlags.txt", "a", encoding='utf-8')
            file.write(flag +"\t"+ packname+"\n")
            file.close()
        else:
         i = 0
  response.close()


links = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["MFWList"]
for link in links:
  url = "https://mifirmware.com/" + link + "/"
  getDetail(url)
