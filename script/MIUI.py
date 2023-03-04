import requests
import json
from bs4 import BeautifulSoup
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/110.0.0.0"}
IDs = ["230","360","369","358","367","349","357","366","356","365","337","355","364","346","336","354","363","345","353","362","371","361","370","352","323","331","341","351","321","330","340","313","320","329","339","348","319","328","347","327","326","325","335","343","324","332","342","315","314","338","318","317","300","308","316","241","309"]

for id in IDs:
# for id in range(1,600):
  id = str(id)
  print("\r"+id+"    ",end="")
  url = "https://www.miui.com/getrom.php?r="+id+"&m=yes&app=true"
  response = requests.get(url, headers=headers)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content,'lxml')
    title = soup.find("title").text
    if title =="MIUI下载 - MIUI官网手机版":
      i = 0
    else:
      devname = soup.find("h3").text
      print(id+"\t机型名称："+devname)
      lists = soup.find_all("a", attrs={"class" :"link_down"})
      for list in lists:
        rom_url = list.attrs['href']
        if rom_url == '':
          i = 0
        else:
          REflags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"]
          recovery = rom_url.split('/')[4]
          checker = recovery.split('_')[1]
          if checker in REflags:
            devdata = json.loads(open("static/data/data/devices/"+REflags[checker]+".json", 'r', encoding='utf-8').read()).__str__()
            if recovery in devdata:
              i = 0
            else:
              print("发现一条新数据\tID:"+id)
              file = open("static/data/script/MIUI.txt", "a", encoding='utf-8')
              file.write(recovery+"\n")
              file.close()
          else:
              print("发现一条新判断符\tID:"+id)
              file = open("static/data/script/MIUIFlags.txt", "a", encoding='utf-8')
              file.write(checker+"\n")
              file.close()
  else:
    i = 0


