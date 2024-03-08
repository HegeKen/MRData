import os
from bs4 import BeautifulSoup
import common

directories = [
  "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\miui",
  "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\hyperos"
]
directory = "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\miui"
# for directory in directories:
for root, dirs, files in os.walk(directory):
  for file in files:
    file_path = os.path.join(root, file)
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()
      soup = BeautifulSoup(content, 'lxml')
      span_tags = soup.findAll('span', {'id': 'filename'})
      for tag in span_tags:
        common.checkExist(tag.text)