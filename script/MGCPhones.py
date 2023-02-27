import requests
import json
import time

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
base_api = "https://sgp-api.buy.mi.com/bbs/api/"
ahome = "/phone/getdevicelist?phone_id="
regions = ["global", "bd", "id", "my", "pk", "ph", "tr", "vn", "th", "de", "es", "fr", "it", "pl", "rs", "uk", "ru", "ua", "mie", "br", "co", "mx", "pe", "cl", "ng", "eg"]
domains = ["https://sgp-api.buy.mi.com/bbs/api/","https://ams-api.buy.mi.com/bbs/api/"]
devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
AllIds = json.loads(devlist.read())["Full"]
for region in regions:
  for domain in domains:
    url = domain+region+"/phone/getphonelist"
    response = requests.get(url, headers=headers)
    if (response.status_code != 404):
      content = response.content.decode("utf8")
      IDs = json.loads(content)["data"]["phone_data"]["phone_list_order_by_abc"]
      for id in IDs:
        if id["id"] in AllIds:
          i = 0
        else:
          print( id["id"])
    else:
      i = 0
    response.close()
