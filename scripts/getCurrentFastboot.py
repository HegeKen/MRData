import common
from datetime import datetime

urls = []
def chekc_url_exits(url):
  if url in urls:
    i = 0
  else:
    urls.append(url)

def genlink(codename, code, btag, region, carriers):
  base_url = 'https://update.intl.miui.com/updates/miota-fullrom.php?d='
  if not carriers:
    url = base_url + code + '&b=' + btag + '&r=' + region + '&n='
    chekc_url_exits(url)
  else:
    for carrier in carriers:
      url = base_url + code + '&b=' + btag + '&r=' + region + '&n=' + carrier
      chekc_url_exits(url)

base_url = 'https://update.intl.miui.com/updates/miota-fullrom.php?d='
for device in common.currentStable:
  devdata = common.loadJson(device)
  codename = devdata["codename"]
  for branch in devdata['branches']:
    code = branch['code']
    if code == '':
      print('请修补机型： ' + device + '文件中未指定的区域代码\n')
    else:
      i = 0
    btag = branch['btag']
    region = branch['region']
    carriers = branch['carrier']
    genlink(codename, code, btag, region, carriers)

for url in urls:
  print("\r",datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\t'+url+"                ",end="")
  common.getFastboot(url)
