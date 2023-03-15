import json
import sqlite3

rerions = ["China","Taiwan"]
devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["MDdevices"]
for all in all_devices:
  device = all["code"]
  conn = sqlite3.connect('static/data/script/MiFlashPro/China/download.db3')
  c = conn.cursor()
  query = """SELECT dl_rom_name, ver_name from download_storage WHERE model LIKE '""" + device+"%'"
  cursor = c.execute(query)
  for row in cursor:
    if ".zip" in row[0]:
      checker = row[0].split('_')[1]
      devices = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"]
      if checker in devices.__str__():
        codename = devices[checker]
      else:
        # print("发现一条新数据")
        filename = "static/data/script/MiFlashPro/MiFlashProFlag.txt"
        file = open(filename, "a", encoding='utf-8')
        file.write(checker+"\n")
        file.close()
      # print(checker)
      devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read()).__str__()
      if row[0] in devdata:
        i = 0
      else:
        print("发现一条新数据")
        filename = "static/data/script/MiFlashPro/MiFlashPro.txt"
        file = open(filename, "a", encoding='utf-8')
        file.write(row[0]+"\n")
        file.close()
    elif ".tgz" in row[0]:
      checker = row[1]
      if "DEV" in checker:
        if row[0].split('_')[1] == "48m":
          codename = row[0].split('_')[0]+"_48m"
        else:
          codename = row[0].split('_')[0]
      else:
        if checker[0] == "V":
          i = 0
          checker = checker[-6:]
          devices = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
          if checker in devices.__str__():
            codename = devices[checker]
          else:
            print(checker + "\t"+row[0])
            filename = "static/data/script/MiFlashPro/MiFlashProFlag.txt"
            file = open(filename, "a", encoding='utf-8')
            file.write(checker + "\t"+row[0]+"\n")
            file.close()
        else:
          if row[0].split('_')[1] == "48m":
            codename = row[0].split('_')[0]+"_48m"
          elif row[0].split('_')[1] == "plus":
            codename = row[0].split('_')[0]+"_plus"
          elif row[0].split('_')[1] == "xhdpi":
            codename = row[0].split('_')[0]+"_xhdpi"
          elif row[0].split('_')[1] == "pro":
            codename = row[0].split('_')[0]+"_pro"
          elif row[0].split('_')[1] == "lte":
            codename = row[0].split('_')[0]+"_lte_ct"
          else:
            codename = row[0].split('_')[0]
        devdata = json.loads(open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8').read()).__str__()
        if row[0] in devdata:
          i = 0
        else:
          print("发现一条新数据")
          filename = "static/data/script/MiFlashPro/MiFlashPro.txt"
          file = open(filename, "a", encoding='utf-8')
          file.write(row[0]+"\n")
    else:
      print(row[0])

devlist.close()
