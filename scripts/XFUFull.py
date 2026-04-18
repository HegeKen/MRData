import os
import common
import chardet # type: ignore
from bs4 import BeautifulSoup

# directories = [
#   "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\miui",
#   "D:\\Projects\\MIUIROMS\\XFUOrigin\\pages\\hyperos"
# ]

directories = [
  "../Sources/xmfirmwareupdater.github.io/pages/miui",
  "../Sources/xmfirmwareupdater.github.io/pages/hyperos"
]

false_packs = [
  'laurel_sprout_eea_global_images_V12.0.1.0.RFQEUXM_20201227.0000.00_11.0_4d92859652',
  'laurel_sprout_global_images_V12.0.2.0.RFQMIXM_20201226.0000.00_11.0_9a673f1503',
  '44edb6fd7214022224e0a6ba8eb8a067362c0fe7.zip',
  'OS1.0.4.0.UNKCNXMmiui_VERMEER_OS1.0.4.0.UNKCNXM_c3235c755f_14.0.zip'
]
for directory in directories:
  for root, dirs, files in os.walk(directory):
    for file in files:
      file_path = os.path.join(root, file)
      with open(file_path, 'rb') as f:
        raw_content = f.read()
        result = chardet.detect(raw_content)
        encoding = result['encoding']
        if encoding is None:
          encoding = 'utf-8'
        content = raw_content.decode(encoding, errors='replace')
        soup = BeautifulSoup(content, 'lxml')
        span_tags = soup.find_all('span', {'id': 'filename'})
        for tag in span_tags:
          if tag.text in false_packs:
            continue
          else:
            common.checkExist(tag.text)