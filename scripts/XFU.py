import yaml
import requests
import common

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
           "Connection": "close"}

response = requests.get("https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/data/latest.yml", verify=False)
if (response.status_code == 200):
  content = response.content.decode("utf8")
  if content == "":
    i = 0
  else:
    data = yaml.safe_load(content)
    for link in data:
      package = link['link'].split('/')[4]
      common.checkExit(package)
