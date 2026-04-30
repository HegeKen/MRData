import common
import requests
import json
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
headers = {'Connection': 'close'}
domains = ['https://sgp-api.buy.mi.com/bbs/api/','https://ams-api.buy.mi.com/bbs/api/']
params = '/phone/getlinepackagelist'
regions = ['global','rs','bd','id','my','pk','ph','tr','vn','th','de','es','fr',
           'it','pl','uk','ru','ua','mie','br','co','mx','pe','cl','ng','eg']

re = "https://sgp-api.buy.mi.com/bbs/api/global/phone/getphonelist"

response = requests.get(re, headers=headers)
content = response.content.decode("utf8")
data = json.loads(content)
for device in data['data']['phone_data']['default'][0]['id_list']:
  if device in common.CurrentIDS:
    continue
  else:
    print(device)