import requests
import json
import time

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
base_api = "https://sgp-api.buy.mi.com/bbs/api/"
ahome = "/phone/getdevicelist?phone_id="
regions = ["global", "bd", "id", "my", "pk", "ph", "tr", "vn", "th", "de", "es", "fr",
           "it", "pl", "rs", "uk", "ru", "ua", "mie", "br", "co", "mx", "pe", "cl", "ng", "eg"]
latest = 1900571
idrange = ["1700","1800","1900"]
start = "571"
end = "1000"
for id in range(int(start),int(end)):
  for ids in idrange:
    devid = int(ids)*1000 + id
    for region in regions:
      if (region == "rs"):
        url = "https://ams-api.buy.mi.com/bbs/api/rs/phone/getdevicelist?phone_id=" + str(devid)
      else:
        url = base_api + region + ahome + str(devid)
      response = requests.get(url, headers=headers)
      content = response.content.decode("utf8")
      did = json.loads(content)
      device_name = did["data"]["device_data"]["phone_name"]
      if (device_name != ""):
          filename = "static/data/updater/deviceIDs.txt"
          file = open(filename, "a", encoding='utf-8')
          file.write("机型ID:"+str(devid)+"\t机型名称:"+device_name+"\n")
          file.close()
          t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
          print(str(t)+"\t机型ID:"+str(devid)+"\t地区代码:"+region+"\t机型名称:"+device_name+"\t将该条数据存入文件")
      else:
          t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
          print(str(t)+"\t机型ID:"+str(devid)+"\t地区代码:"+region+"\t不存在机型数据")
      response.close()
