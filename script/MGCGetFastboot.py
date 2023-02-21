import requests
import json
import time

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
domains = ["https://sgp-api.buy.mi.com/bbs/api/","https://ams-api.buy.mi.com/bbs/api/"]
params = "/phone/getlinepackagelist"
regions = ["bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","rs","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]



def getFastboot(region):
  for domain in domains:
    url = domain+region+params
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    if (response.status_code != 404):
      packages = json.loads(content)["data"]
      if packages == None:
        i = 0
      else:
        for package in packages:
          fastboot = package["package_url"].split('/')[4]
          flag = package["package_url"].split('/')[3][-6:]
          flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
          if flag in flags:
            devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
            if fastboot in devdata:
              print("\r"+url+"      ",end="")
            else:
              print("发现未收录版本")
              file = open("static/data/script/MGC/MGCGetFastboot.txt", "a", encoding='utf-8')
              file.write(fastboot+"\n")
              file.close()
          else:
            print("发现未收录机型以及版本")
            file = open("static/data/script/MGC/MGCFlags.txt", "a", encoding='utf-8')
            file.write(flag +"\t"+ fastboot+"\n")
            file.close()
    else:
      i = 0





getFastboot("global")
# time.sleep(60)

for region in regions:
  getFastboot(region)
