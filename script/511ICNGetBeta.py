import requests
import json
from bs4 import BeautifulSoup
import re
import time

headers = {"user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 Edg/110.0.0.0"}
headers['Referer']= "http://miui.511i.cn/?index=rom_list"
url = "http://miui.511i.cn/?index=rom_list"
current = ["UMI","CMI", "CAS", "VANGOGH", "THYME", "VENUS", "STAR", "RENOIR","LISA", "CUPID", "ZEUS", "PSYCHE", "DAUMIER",
           "MAYFLY", "UNICORN", "THOR", "FUXI", "NUWA", "CETUS", "ODIN", "ZIZHAN", "NABU", "ELISH", "ENUMA","DAGU", "MONA", "ZIJIN", "ZIYI","CHOPIN",
           "EVERGO",
           "PISSARRO", "XAGA", "SUNSTONE", "RUBY", "REDWOOD", "APOLLO", "ALIOTH", "HAYDN", "ARES",
           "MUNCH", "RUBENS", "MATISSE", "INGRES", "DITING", "MONDRIAN", "SOCRATES", "REMBRANDT",]
branches = ["0", "1", "1b"]

st = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
for device in current:
    payload = (('dh', device), ('lx', '1b'))
    response = requests.post(url, data=payload, headers=headers, timeout=10)
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content, 'lxml')
    lists = soup.find_all("a")
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t+"\t机型："+device+"\t分支："+'1b')
    for list in lists:
      rom_url = list.attrs['href']
      regex = r'miui_.*?.zip'
      matches = re.finditer(regex, rom_url, re.MULTILINE)
      for match in matches:
        codename = device.lower()
        recovery = match.group()
        android = recovery.split('_')[4].strip(".zip")
        ver = recovery.split('_')[2]
        devicedata = open("static/data/data/devices/" + codename+".json", 'r', encoding='utf-8')
        devdata = json.loads(devicedata.read())
        if recovery in devdata.__str__():
          i = 0
        else:
          devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
          all_devices = json.loads(devlist.read())["MDbeta"]
          for all in all_devices:
            code = all["code"]
            if code==device.lower():
              cname = all["NameCn"]
              ename = all["NameEn"]
              datas = {'code':device.lower(),'NameCn':cname,'NameEn':ename,'miui': ver, 'android': android, 'recovery':recovery,'fastboot':""}
              file = open("static/data/script/511ICNGetBeta.json","a", encoding='utf-8')
              person_json = json.dumps(datas, ensure_ascii=False)
              file.write(person_json+",")
              file.close()
              print("\r"+recovery+"                              ")
              devicedata.close()
            else:
              i = 0
    response.close
      # time.sleep(2)
et = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(st + "\t" + et)
