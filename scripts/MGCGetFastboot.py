import requests
import json
import common
from datetime import datetime

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
headers = {'Connection': 'close'}
domains = ['https://sgp-api.buy.mi.com/bbs/api/','https://ams-api.buy.mi.com/bbs/api/']
params = '/phone/getlinepackagelist'
regions = ['global','rs','bd','id','my','pk','ph','tr','vn','th','de','es','fr',
           'it','pl','uk','ru','ua','mie','br','co','mx','pe','cl','ng','eg']



def getFastboot(region):
  for domain in domains:
    url = domain+region+params
    print('\r'+url+'              ',end='')
    response = requests.get(url, headers=headers)
    content = response.content.decode('utf8')
    if (response.status_code != 404):
      packages = json.loads(content)['data']
      if packages == None:
        i = 0
      else:
        for package in packages:
          fastboot = package['package_url'].split('/')[4].split('?')[0]
          common.checkExist(fastboot)
    response.close()

urls = []
for region in regions:
  for domain in domains:
    url = domain+region+params
    if url in urls:
      continue
    else:
      urls.append(url)

for url in urls:
  print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\t'+url+"      ",end="")
  response = requests.get(url, headers=headers)
  content = response.content.decode('utf8')
  if (response.status_code != 404):
    packages = json.loads(content)['data']
    if packages == None:
      i = 0
    else:
      for package in packages:
        fastboot = package['package_url'].split('/')[4].split('?')[0]
        common.checkExist(fastboot)
  response.close()
