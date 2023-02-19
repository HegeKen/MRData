import sqlite3
import json



devlist = open("static/data/updater/devices.json", 'r', encoding='utf-8')
all_devices = json.loads(devlist.read())["devices"]
for all in all_devices:
  device = all["code"]
  conn = sqlite3.connect('static/data/updater/cn.db3')
  c = conn.cursor()
  query = """SELECT model,url,ver_name,dl_rom_name,android_ver from download_storage WHERE model LIKE '""" + device+"%'"
  cursor = c.execute(query)
  for row in cursor:
    codename = row[0].split('_')[0]
    if codename == "camellian":
      codename == "camellia"
    else:
      i = 0
    if len(row[0].split('_')) >=2:
      checker = row[0].split('_')[1]
      if checker == '48m':
        codename = "picasso_48m"
      elif checker == 'c3l2':
        codename = "dandelion_c3l2"
      elif checker == 'pro':
        codename = row[0].split('_')[0]+"_pro"
      else:
        i = 0
      fread = open("static/data/data/devices/"+codename+".json", 'r', encoding='utf-8')
      data = json.loads(fread.read())
      if row[3] in data.__str__():
        i= 0
      else:
        filename = "static/data/updater/MiFlashPro.txt"
        file = open(filename, "a", encoding='utf-8')
        file.writelines(row[3]+"\n")
        file.close()
        print(row[0]+"发现疑似一条更新内容")
      fread.close()
devlist.close()
