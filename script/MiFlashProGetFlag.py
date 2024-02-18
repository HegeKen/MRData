import json
import sqlite3

rerions = ["China","Taiwan"]
devlist = open("public/MRdata/script/crawler.json", 'r', encoding='utf-8')
all_Flags = json.loads(devlist.read())["MiFlashPro"].__str__()

conn = sqlite3.connect('public/MRdata/script/MiFlashPro/Taiwan/download.db3')
c = conn.cursor()
query = """SELECT model from download_storage"""
cursor = c.execute(query)
for row in cursor:
  if row[0] in all_Flags:
    i = 0
  else:
    print(row[0])
