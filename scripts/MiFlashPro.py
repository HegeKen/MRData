import sqlite3
import common


# C:\Users\Hege\AppData\Roaming\Xiaomi\miflash_pro\Config
conn = sqlite3.connect('static/data/scripts/MiFlashPro/download.db3')
c = conn.cursor()
query = '''SELECT dl_rom_name from download_storage'''
cursor = c.execute(query)
for row in cursor:
  if 'OS' in row[0]:
    i = 0
  else:
    common.checkExit(row[0])
