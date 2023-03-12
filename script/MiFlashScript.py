import requests
import json

# headers = {"user-agent": "XiaomiPCSuite"}
# url = "http://update.miui.com/updates/miota-fullrom.php?d=agate_cl_en_global&b=F&r=global&n="
# url = "http://update.miui.com/updates/miota-fullrom.php?d=alioth&b=F&r=cn"
# response = requests.post(url, headers=headers)
# content = response.content.decode("utf8")
# print(response.text)
# filename = json.loads(content)["LatestFullRom"]["filename"]
# print(filename)

base_url = "http://update.miui.com/updates/miota-fullrom.php?d="
# regions = ["cn","tw","global","rs","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]
regions = ["cn","tw","global","eea","ru","in","id","jp","tr"]
carriers = ["","chinatelecom"]
branches = ["F","X"]
# branches = ["F"]
headers = {"user-agent": "XiaomiPCSuite"}
devices = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["MiFlashProCurrent"]

for device in devices:
  checkers = device["checkers"]
  for checker in checkers:
    for region in regions:
      if region == "cn":
        for branch in branches:
          for carrier in carriers:
            url = base_url+checker+"&b="+branch+"&r=cn&n="+carrier
            print("\r"+url+"                 ",end="")
            response = requests.post(url, headers=headers)
            if (response.status_code == 200):
              content = response.content.decode("utf8")
              if content == "":
                i = 0
              else:
                data = json.loads(content)["LatestFullRom"]
                if len(data)>0:
                  devdata = json.loads(open("static/data/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
                  if data["filename"] in devdata:
                    i= 0
                  else:
                    print("发现一条新数据")
                    filename = "static/data/script/MiFlashPro/MiFlashPro.txt"
                    file = open(filename, "a", encoding='utf-8')
                    file.write(data["filename"]+"\n")
                    file.close()
                else:
                  i = 0
            else:
              i = 0
            response.close()
      else:
        url = base_url+checker+"&b=F&r="+region+"&n="
        print("\r"+url+"                 ",end="")
        response = requests.post(url, headers=headers)
        if (response.status_code == 200):
          content = response.content.decode("utf8")
          if content == "":
            i = 0
          else:
            data = json.loads(content)["LatestFullRom"]
            if len(data)>0:
              devdata = json.loads(open("static/data/data/devices/"+device["codename"]+".json", 'r', encoding='utf-8').read()).__str__()
              if data["filename"] in devdata:
                i= 0
              else:
                print("发现一条新数据")
                filename = "static/data/script/MiFlashPro/MiFlashPro.txt"
                file = open(filename, "a", encoding='utf-8')
                file.write(data["filename"]+"\n")
                file.close()
            else:
              i = 0
        else:
          i = 0
        response.close()
