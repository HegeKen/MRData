import json


devlist = json.loads(open("static/data/data/getFlags.json", 'r', encoding='utf-8').read())["full"]
for device in devlist:
  codename = device["code"]
  devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    for rom in branch["links"]:
      if rom["recovery"] == '':
        i = 0
      else:
        flag = rom["recovery"].split('_')[1]
        print(flag)
        fine = "static/data/script/Flags.json"
        allFlags = open(fine, 'r', encoding='utf-8').read().__str__()
        if flag in allFlags:
          i = 0
        else:
          file = open("static/data/script/Flags.json", "a", encoding='utf-8')
          file.write("\""+flag+"\":\""+codename+"\",\n")
          file.close()

