import json


devlist = json.loads(open("static/data/data/getFlags.json", 'r', encoding='utf-8').read())["full"]
for device in devlist:
  codename = device["code"]
  devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    if branch["branch"] == "cnmp":
      i = 0
    elif branch["branch"] == "cnma":
      i = 0
    elif branch["branch"] == "mgbb":
      i = 0
    elif branch["branch"] == "cnmt":
      i = 0
    elif branch["branch"] == "ctse":
      i = 0
    elif branch["branch"] == "cuse":
      i = 0
    elif branch["branch"] == "litese":
      i = 0
    elif branch["branch"] == "msap":
      i = 0
    # elif branch["branch"] == "cnmt":
    #   i = 0
    # elif branch["branch"] == "cnmt":
    #   i = 0
    # elif branch["branch"] == "cnmt":
    #   i = 0

    else:
      for rom in branch["links"]:
        flag = rom["miui"][-6:]
        short_flag = rom["miui"][-6:-4]
        print(short_flag)
        file = open("static/data/script/Flags.json", "a", encoding='utf-8')
        file.write("\""+flag+"\":\""+codename+"\",\n")
        file.close()
        file = open("static/data/script/FlagsShort.json", "a", encoding='utf-8')
        file.write("\""+short_flag+"\":\""+codename+"\",\n")
        file.close()

