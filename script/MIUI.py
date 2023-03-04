import requests
import json
from bs4 import BeautifulSoup
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/110.0.0.0"}
IDs = ["300","308","313","319","320","321","323","324","325","326","327","328","331","335","336","337","338","340","343","345","346","348","349","351","353","355","356","360","361","363","364","367","369"]
for id in IDs:
# for id in range(600,1000):
  id = str(id)
  url = "https://www.miui.com/getrom.php?r="+id+"&m=yes&app=true"
  print("\r"+id+"    "+url,end="")
  response = requests.get(url, headers=headers)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content,'lxml')
    lists = soup.find_all("a", attrs={"class" :"link_down"})
    if len(lists) > 1:
      IDFile = open("static/data/script/MIUIIDFile.txt", "a", encoding='utf-8')
      IDFile.write("\""+id+"\",")
      IDFile.close()
      devname = soup.find("h3").text
      print(id+"\t机型名称："+devname)
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
  else:
    i = 0


