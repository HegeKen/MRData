import sqlite3
import common


conn = sqlite3.connect('static/data/script/MiFlashPro/download.db3')
c = conn.cursor()
query = """SELECT dl_rom_name from download_storage"""
cursor = c.execute(query)
for row in cursor:
  common.checkExit(row[0])
