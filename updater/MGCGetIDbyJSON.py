import requests
import json
import time


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
base_api = "https://sgp-api.buy.mi.com/bbs/api/"
ahome = "/phone/getphonelist"
regions = ["global", "bd", "id", "my", "pk", "ph", "tr", "vn", "th", "de", "es", "fr",
           "it", "pl", "rs", "uk", "ru", "ua", "mie", "br", "co", "mx", "pe", "cl", "ng", "eg"]

for region in regions:
  if (region == "rs"):
    url = "https://ams-api.buy.mi.com/bbs/api/rs/phone/getphonelist"
  else:
    url = url = base_api + region + ahome
  response = requests.get(url, headers=headers)
  content = response.content.decode("utf8")
  did = json.loads(content)
  ids = json.dumps(json.loads(open("static/data/updater/crawler_full.json", 'r', encoding='utf-8').read())["MGC"], indent=2, ensure_ascii=False)
  for id in did["data"]["phone_data"]["phone_list"]:
    if id["id"] in ids:
     i = 0
    else:
      print(id["id"])
      file = open("static/data/updater/MGCGetIDbyJSON.txt", "a", encoding='utf-8')
      file.write("机型ID:"+id["id"]+"\t链接:"+url+"\n")
      file.close()
