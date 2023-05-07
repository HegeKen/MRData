import requests
import json



devices = ["ishtar","mondrian"]
base_url = "http://update.miui.com/updates/miota-fullrom.php?d="
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
           "Connection": "close"}

for device in devices:
  dataurl = "https://data.miuier.com/data/devices/"+device+".json"
  mrdata = requests.get(dataurl)
  devdata = json.loads(mrdata.text)
  # devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  for branch in devdata["branches"]:
    code = branch["code"]
    btag = branch["btag"]
    region = branch["region"]
    carriers = branch["carrier"]
    if len(carriers)==0:
      i = 0
    else:
      for carrier in carriers:
        url = base_url+code+"&b="+btag+"&r="+region+"&n="+carrier
        response = requests.post(url, headers=headers)
        if (response.status_code == 200):
          content = response.content.decode("utf8")
          if content == "":
            i = 0
          else:
            data = json.loads(content)["LatestFullRom"]
            if len(data)>0:
              if data["filename"] in devdata.__str__():
                i= 0
              else:
                print("发现一条新数据\t"+data["filename"])
                filename = "static/data/script/2023NewROMs.txt"
                file = open(filename, "a", encoding='utf-8')
                file.write(data["filename"]+"\n")
                file.close()
            else:
              i = 0
        else:
          i = 0
        response.close()

