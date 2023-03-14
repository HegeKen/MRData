import requests
import json


base_url = "http://update.miui.com/updates/miota-fullrom.php?d="
carriers = ["","chinatelecom"]
# branches = ["F","X"]
branches = ["X"]
headers = {"user-agent": "XiaomiPCSuite"}
headers['account.passtoken'] = ""
headers['account.uid'] = ""
devices = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["MDbeta"]

for device in devices:
  for carrier in carriers:
    codename = device["code"]
    url = base_url+codename+"&b=X&r=cn&n="+carrier
    response = requests.post(url, headers=headers)
    if (response.status_code == 200):
      content = response.content.decode("utf8")
      print(content)
    else:
      i = 0
