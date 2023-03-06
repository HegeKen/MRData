import json

devices = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["MDdevices"]
for device in devices:
  codename = device["code"]
  filename = "static/data/script/MiFlashPro.txt"
  file = open(filename, "a", encoding='utf-8')
  file.write("{\"codename\":\""+codename+"\",\"checkers\": [")
  file.close()
  devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    links = branch["links"]
    for link in links:
      fastboot = link["fastboot"]
      if "_images" in fastboot:
        checker = fastboot.split("_images")[0]
        filename = "static/data/script/MiFlashPro.txt"
        file = open(filename, "a", encoding='utf-8')
        file.write("\""+checker+"\",")
        file.close()
      else:
        i = 0
  filename = "static/data/script/MiFlashPro.txt"
  file = open(filename, "a", encoding='utf-8')
  file.write("]},")
  file.close()
