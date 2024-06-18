import common

urls = []
def chekc_url_exits(url):
  if url in urls:
    i = 0
  else:
    urls.append(url)

def genlink(codename, code, btag, region, carriers):
  base_url = 'https://update.miui.com/updates/miota-fullrom.php?d='

  if region == 'cn':
    if not carriers:
      url = base_url + code + '&b=' + btag + '&r=' + region + '&n='
      chekc_url_exits(url)
    else:
      for carrier in carriers:
        url = base_url + code + '&b=' + btag + '&r=' + region + '&n=' + carrier
        chekc_url_exits(url)
  elif region == 'global':
    url = base_url + code + '&b=' + btag + '&r=' + region + '&n='
    chekc_url_exits(url)
  else:
    url = base_url + code + '&b=' + btag + '&r=' + region + '&n='
    chekc_url_exits(url)
    if "_global" in code and codename not in ["pissarroin","angelica","cannon","sweet","camellia"]:
      url = base_url + code + '&b=' + btag + '&r=' + code.split(codename+"_")[1].split("_global")[0] + '&n='
      chekc_url_exits(url)
    else:
      i = 0
    url = base_url + code + '&b=' + btag + '&r=eea&n='
    chekc_url_exits(url)
    url = base_url + code + '&b=' + btag + '&r=global' + '&n='
    chekc_url_exits(url)

base_url = 'https://update.miui.com/updates/miota-fullrom.php?d='
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
  print("\r"+url+"                ",end="")
  common.getFastboot(url)
