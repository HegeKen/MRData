import requests
import json
import common
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess
from sys import platform

subprocess.run(["cls"] if platform == "win32" else ["clear"])
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
headers = {'Connection': 'close'}
domains = ['https://sgp-api.buy.mi.com/bbs/api/','https://ams-api.buy.mi.com/bbs/api/']
params = '/phone/getlinepackagelist'
regions = ['global','rs','bd','id','my','pk','ph','tr','vn','th','de','es','fr',
           'it','pl','uk','ru','ua','mie','br','co','mx','pe','cl','ng','eg']



re = "https://sgp-api.buy.mi.com/bbs/api/global/phone/getphonelist"

urls = []
for region in regions:
  for domain in domains:
    url = domain+region+params
    if url in urls:
      continue
    else:
      urls.append(url)

for url in urls:
  session = requests.Session()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
  session.mount('http://', HTTPAdapter(max_retries=retries))
  session.mount('https://', HTTPAdapter(max_retries=retries))
  print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\t'+url+"      ",end="")
  try:
    response = session.post(url, headers=headers, timeout=(5, 10))
    content = response.content.decode('utf8') 
    if (response.status_code != 404):
      packages = json.loads(content)['data']
      if packages == None or packages == "null":
        i = 0
      else:
        for package in packages:
          fastboot = package['package_url'].split('/')[4].split('?')[0]
          common.checkExist(fastboot)
  except requests.exceptions.RequestException as e:
    i = 0
  session.close()

# ids=[]
# for region in regions:
#   for domain in domains:
#     url = domain+region+"/phone/getphonelist"
#     response = requests.get(url, headers=headers)
#     content = response.content.decode('utf8')
#     if (response.status_code != 404):
#       packages = json.loads(content)['data']['phone_data']['phone_list']
#       if packages == None:
#         i = 0
#       else:
#         for id in packages:
#           if id['id'] in ids:
#             i = 0
#           else:
#             ids.append(id['id'])
# print(ids)
# response.close()