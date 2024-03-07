import os
from bs4 import BeautifulSoup
import json
import common


XFUpacks = []
FXUMisses = []
IHave = []

# directories = [
#   "D:\\Projects\\MIUIROMS\\XFU\\pages\\miui",
#   "D:\\Projects\\MIUIROMS\\XFU\\pages\\hyperos"
# ]
directory = "D:\\Projects\\MIUIROMS\\XFU\\pages\\miui"
# for directory in directories:
for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    print('\r'+file_path+"                                           ",end="")
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.findAll('span', {'id': 'filename'})
      for tag in span_tags:
        XFUpacks.append(tag.text)
        common.checkExist(tag.text)

for device in common.currentStable:
  devdata = json.loads(open('public/MRdata/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  for branch in devdata['branches']:
    if branch['show'] == '1':
      if "定制版" in branch['zh-cn'] or "EP" in branch['zh-cn'] or "政企" in branch['zh-cn']:
        i= 0
      else:
        for link in branch['links']:
          if link['recovery'] == '':
            i = 0
          else:
            IHave.append(link['recovery'])
          if link['fastboot'] == '':
            i = 0
          else:
            IHave.append(link['fastboot'])

for link in IHave:
  if link not in XFUpacks:
    if "OS1." in link:
      file = open('public/MRdata/scripts/XFUMisses_OS.txt', 'a', encoding='utf-8')
      file.write(link+'\n')
      file.close()
    else:
      file = open('public/MRdata/scripts/XFUMisses_UI.txt', 'a', encoding='utf-8')
      file.write(link+'\n')
      file.close()